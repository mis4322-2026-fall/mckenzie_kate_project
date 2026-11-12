# Movie Finder — System Design

## 1. Design baseline

**Student:** Kate McKenzie · **Proposal:** [01-proposal.md](01-proposal.md), November 11, 2026. This is a proposed design, not completed work.

Movie Finder helps users choose movies and save them to private watchlists. **Scope change:** TMDb replaces the original CSV/local movie catalog. SQLite stores accounts and saved entries. Genre browsing matches ALL selected genres. Registration, popular movies, posters and watchlists are required. Rating/runtime/year filters, trailers, streaming, personal ratings and custom/personalized recommendations are excluded.

Retain active FR-01, FR-03, FR-04, FR-06, FR-08, FR-09, FR-10, FR-11, FR-12, FR-16 and FR-17. FR-07 remains Later for TV shows/interface polish. FR-02, FR-05 and FR-13–FR-15 remain retired; IDs are not reused.

## 2. System context

### Movie Finder — System Architecture

```mermaid
flowchart LR
    Browser["Browser<br/>HTML, CSS and Django templates"]
    Django["Django backend<br/>URLs, views and forms<br/>Authentication and session checks"]
    TMDb["TMDb API<br/>Popular movies, search, genres, details,<br/>ratings, recommendations and poster references"]
    SQLite[("SQLite database<br/>Users, sessions and private watchlists<br/>Saved TMDb IDs and title snapshots")]

    Browser -->|"Page and form requests"| Django
    Django -->|"Rendered HTML and messages"| Browser
    Django -->|"Authenticated API requests"| TMDb
    TMDb -->|"Movie data or API errors"| Django
    Django -->|"Account and watchlist queries"| SQLite
    SQLite -->|"Account, session and saved-entry records"| Django

    classDef frontend fill:#eff6ff,stroke:#2563eb,color:#172554;
    classDef backend fill:#ecfdf5,stroke:#15803d,color:#14532d;
    classDef external fill:#faf5ff,stroke:#7e22ce,color:#581c87;
    classDef database fill:#fff7ed,stroke:#c2410c,color:#7c2d12;
    class Browser frontend;
    class Django backend;
    class TMDb external;
    class SQLite database;
```

Django checks requests/login and returns HTML/CSS pages. TMDb supplies movies and posters; SQLite stores accounts, sessions and private watchlists. Saved titles remain available during API outages, but discovery may not.

## 3. Data model

### Movie Finder — Data Model (ERD)

```mermaid
erDiagram
    USER ||--o{ WATCHLIST_ENTRY : owns

    USER {
        int id PK "Django account ID"
        string username UK "Unique username"
        string password "Django-managed password hash"
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }

    WATCHLIST_ENTRY {
        int id PK "Saved-entry ID"
        int user_id FK "USER.id; owner; CASCADE on user deletion"
        int tmdb_movie_id "Positive external ID; unique together with user_id"
        string title_snapshot "Required; maximum 500 characters"
        datetime saved_at "Automatic saved timestamp"
    }

    %% Each entry belongs to exactly one user; a user can have zero or many entries.
    %% Database constraint: UNIQUE(user_id, tmdb_movie_id), not uniqueness of either field alone.
```

One user owns many saved entries; each entry belongs to one user. Movies remain in TMDb, not a local movie table.

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|
| User | id, username | Built-in ID, CharField | Required/automatic ID | Unique | Owns entries |
| User | password | Built-in CharField | Required | Django hash/validators | Never plain text |
| User | active/staff/superuser flags | Built-in BooleanFields | Django defaults | Permission checks | Admin access |
| WatchlistEntry | id | BigAutoField | Automatic | Unique | Entry ID |
| WatchlistEntry | user | ForeignKey | Required | Current user | CASCADE on user deletion |
| WatchlistEntry | tmdb_movie_id | PositiveIntegerField | Required | Unique with user; valid movie | External ID |
| WatchlistEntry | title_snapshot | CharField(500) | Required | Nonblank | Readable during outages |
| WatchlistEntry | saved_at | DateTimeField | Automatic timestamp | Server-set | Removed with entry |

The unique user/movie pair prevents duplicate saves. Removing one save affects neither other users nor TMDb.

## 4. Pages and actions

Welcome, registration and login are public; all other pages require login. GET reads data. Account and watchlist changes use POST with Django's CSRF protection against forged submissions.

| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|
| FR-17 | `/` | GET welcome | None | `welcome.html`; account links |
| FR-08, FR-04 | `/accounts/register/` | GET/POST register | Unique username; valid matching passwords | `registration/register.html`; errors or automatic login/dashboard |
| FR-01, FR-04, FR-09 | `/accounts/login/` | GET/POST login | Valid credentials | `registration/login.html`; dashboard/error |
| FR-01 | `/accounts/logout/` | POST logout | Session/CSRF | Welcome; session ended |
| FR-09, FR-12 | `/dashboard/` | GET popular movies | API response | `dashboard.html`; cards/navigation |
| FR-10, FR-04 | `/movies/search/?q=...` | GET search | Trim; nonblank, max 200 characters | `movies/search.html`; results/message |
| FR-16, FR-04 | `/movies/browse/?genre=...` | GET browse | One or more valid IDs; ALL matching | `movies/browse.html`; results/message |
| FR-11, FR-04 | `/movies/surprise/` | GET random/Try Again | Valid candidate set | Details or `movies/surprise.html` message |
| FR-03, FR-12 | `/movies/<tmdb_id>/` | GET details | Valid movie ID | `movies/detail.html`; fields, Save/related controls |
| FR-10 | `/movies/<tmdb_id>/recommendations/` | GET related movies | Valid ID | `movies/recommendations.html` |
| FR-06, FR-01 | `/watchlist/` | GET saved movies | Current owner only | `watchlist/list.html` |
| FR-06, FR-04 | `/watchlist/add/` | POST save | CSRF; server-valid movie/title | Redirect with saved/error feedback |
| FR-06, FR-01 | `/watchlist/<entry_id>/remove/` | POST remove | CSRF; entry belongs to user | Remove/redirect or not-found |

Forms have clear labels/errors, templates display text safely, and pages provide home navigation. Posters use placeholders when missing; all movie pages handle API failures.

## 5. Main user flow

### Movie Finder — Main User Flow

```mermaid
flowchart TD
    subgraph Access["1. Account access"]
        WF_start(["START — Open Movie Finder"])
        WF_welcome["Public Welcome Page"]
        WF_account{"Log in or create account?"}
        WF_login["Log In"]
        WF_register["Create Account"]
        WF_validate["Django validates submitted information"]
        WF_valid{"Information valid?"}
        WF_error["Show form error<br/>Retry selected account form"]
        WF_session["Authenticate user<br/>Create Django session"]

        WF_start --> WF_welcome --> WF_account
        WF_account -->|"Log in"| WF_login
        WF_account -->|"Create account"| WF_register
        WF_login --> WF_validate
        WF_register --> WF_validate
        WF_validate --> WF_valid
        WF_valid -->|"No"| WF_error
        WF_valid -->|"Yes"| WF_session
    end

    WF_home["Protected dashboard<br/>Popular movies"]
    WF_choice{"Choose an action"}
    WF_session --> WF_home --> WF_choice

    subgraph Discovery["2. Movie discovery and details"]
        WF_search["Search Movies<br/>Enter title"]
        WF_browse["Browse Genres<br/>Match ALL selected genres"]
        WF_random["Surprise Me<br/>Random candidate"]
        WF_request["Django retrieves movies from TMDb"]
        WF_found{"Request succeeds<br/>and results available?"}
        WF_missing["Helpful error or no-results message<br/>Retry or return home"]
        WF_results["Show results<br/>Select a movie"]
        WF_details["Movie Details<br/>Poster or placeholder, title,<br/>genres, rating and description"]
        WF_next{"Choose next action"}
        WF_save["Save to my watchlist<br/>Prevent duplicate saves"]
        WF_related["TMDb recommendations<br/>Continue results and details flow"]
        WF_again["Try Again<br/>Repeat random selection"]
        WF_back(["Return to dashboard"])

        WF_search --> WF_request
        WF_browse --> WF_request
        WF_random --> WF_request
        WF_request --> WF_found
        WF_found -->|"No"| WF_missing
        WF_found -->|"Yes"| WF_results
        WF_results --> WF_details --> WF_next
        WF_next -->|"Save movie"| WF_save
        WF_next -->|"Related movies"| WF_related
        WF_next -->|"Another random pick"| WF_again
        WF_next -->|"Home"| WF_back
    end

    subgraph Watchlist["3. Private watchlist"]
        WF_watch["My Watchlist<br/>Only my SQLite entries"]
        WF_wa{"Choose saved-movie action"}
        WF_open(["Open Movie Details"])
        WF_remove["Remove only my saved entry<br/>Show updated or empty list"]
        WF_watch --> WF_wa
        WF_wa -->|"Open"| WF_open
        WF_wa -->|"Remove"| WF_remove
    end

    WF_logout["Log Out<br/>End Django session"]
    WF_end(["Public welcome or login<br/>Protected access requires sign-in again"])
    WF_choice -->|"Title search"| WF_search
    WF_choice -->|"Genre browsing"| WF_browse
    WF_choice -->|"Random discovery"| WF_random
    WF_choice -->|"My Watchlist"| WF_watch
    WF_choice -->|"Log out"| WF_logout
    WF_logout --> WF_end

    %% Retry, home, details, recommendations and Try Again labels are continuation points.
    %% They avoid long return arrows; every protected request still checks login and ownership.
    classDef process fill:#eff6ff,stroke:#2563eb,color:#172554;
    classDef decision fill:#f8fafc,stroke:#475569,color:#0f172a;
    classDef error fill:#fff7ed,stroke:#c2410c,color:#7c2d12;
    classDef key fill:#ecfdf5,stroke:#15803d,color:#14532d;
    class WF_login,WF_register,WF_validate,WF_welcome,WF_search,WF_browse,WF_random,WF_request,WF_results,WF_details,WF_save,WF_related,WF_again,WF_watch,WF_remove,WF_logout process;
    class WF_account,WF_valid,WF_choice,WF_found,WF_next,WF_wa decision;
    class WF_error,WF_missing error;
    class WF_start,WF_session,WF_home,WF_end,WF_open,WF_back key;
```

Login/registration leads to the dashboard. Users discover movies, open details, save/remove entries or log out. Error paths allow retry; rounded continuation nodes avoid crossing return arrows.

## 6. Access and login

| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|
| Visitor | Welcome/register/login | No protected pages |
| Signed-in user | Movie discovery and own watchlist | Only their saved entries |
| Active superuser | Django Admin users/registered entries | Separate admin permissions |

Use Django forms, password hashing and sessions. Valid registration automatically logs the user in and opens the dashboard; valid login does the same. Invalid information shows errors.

Every protected view checks login, even for direct URLs. Watchlist queries use `request.user`, not a submitted owner. Only owner-checked POST requests save/remove entries; GET cannot change them. POST logout ends the session, so protected pages require login again.

Create local demo accounts with interactive Django tools, then ordinary fictional accounts for privacy checks. Keep credentials/database files out of Git. Admin login alone does not satisfy the required user-facing login and protected dashboard.

## 7. Integrations and configuration

| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|
| Python/Django | Backend/pages/authentication | [Django](https://docs.djangoproject.com/en/stable/), [Python](https://docs.python.org/3/) | `DJANGO_SECRET_KEY`; local debug/host settings if used | Accounts work without TMDb |
| SQLite | Accounts/sessions/watchlists | [SQLite notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) | None required | Saved titles remain local |
| TMDb/images | Popular/search/genres/details/related movies/posters | [API](https://developer.themoviedb.org/docs/getting-started), [Authentication](https://developer.themoviedb.org/docs/authentication-application), [Images](https://developer.themoviedb.org/docs/image-basics) | `TMDB_READ_ACCESS_TOKEN` | 10-second timeout, helpful errors, placeholders; fictional test responses |

When a user searches or browses, the Django view validates the input and sends an HTTPS request through a shared TMDb helper. The helper reads the response, and the view passes movie information to a template. The browser receives a finished page, not the API credentials. Requests cover popular movies, title search, genres, details, recommendations and poster information.

The planned TMDb credential is a server-side read-access token stored in `TMDB_READ_ACCESS_TOKEN`. Keep it and Django's secret key out of templates, JavaScript, Git and error messages. Document environment setup during implementation.

Use a proposed 10-second timeout. Empty responses produce a no-results message; timeouts, denied access or malformed responses produce a service-unavailable message with retry/home navigation. Missing posters use placeholders, and missing ratings/descriptions are labeled unavailable. Saved titles remain readable from SQLite during an outage. Validate a movie before saving a new entry. Access and usage checks are listed in section 11.

## 8. Outputs and business rules

Fictional examples: A has Comedy; B has Comedy/Family; C has Mystery.

| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|
| FR-09 | Popular movies | Display TMDb's popular list in provider order, removing duplicate movie IDs. Popularity and numeric rating are separate values. | A/B/B becomes A/B |
| FR-10 | Title search | Trim and validate the submitted title, then use TMDb's matching results. Select by movie ID because different movies can share a title. | Two same-title movies with different IDs remain selectable |
| FR-16 | ALL-selected genres | Require at least one valid genre. Every selected genre must be present; selecting more genres narrows the matches rather than combining unrelated results. | Comedy: A/B; Comedy + Family: B |
| FR-10 | Recommendations | Ask TMDb for recommendations for the selected ID. Preserve provider order, excluding the original movie and repeated IDs. No local storyline or user-history scoring. | For A, related A/B/B/C becomes B/C |
| FR-11 | Surprise Me/Try Again | Choose one movie randomly from unique valid candidates in a bounded popular response. Try Again requests another selection; immediate repeats are allowed. | A/B/C: 1-in-3 each within that set, not the full TMDb catalog |
| FR-03, FR-12 | Movie details | Show poster/placeholder, title, genres, numeric rating with its verified scale, and description on a separate page. Never invent missing information. | Missing rating says unavailable |
| FR-06 | Private watchlist | Save a validated TMDb ID/title under the signed-in user's account. Enforce one entry per user/movie; list newest first. Owner-checked POST removal affects only that entry. Entries survive restart. | Saving twice leaves one entry; another user's save is unchanged |
| FR-04 | Helpful messages | Distinguish invalid input, empty matches, missing information and service failures so the user knows whether to change the search or retry later. | Failed API request is not “no matches” |

## 9. Build increments

The table is in implementation order: INC-01 → INC-02 → INC-03 → INC-06 → INC-04 → INC-05. Watchlists follow API details so persistence is demonstrated early. Existing IDs and their requirement mappings are unchanged; IDs identify work, not sequence numbers.

| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|
| INC-01 | Django/SQLite login foundation | FR-01, FR-17; foundation FR-09 | Welcome/login/protected dashboard/logout | AC-02, AC-04, AC-42; foundation AC-01, AC-03 |
| INC-02 | Registration/automatic login | FR-08, FR-01, FR-09 | Form/session/layout | AC-15, AC-16; account AC-01 |
| INC-03 | Popular/search/details/posters | FR-09, FR-10, FR-03, FR-12, FR-04, FR-01 | API helper/cards/details | AC-01, AC-20, AC-23, AC-28, AC-41; portions AC-07, AC-08, AC-17, AC-40, AC-43 |
| INC-06 | Private watchlists | FR-06, FR-01, FR-03, FR-04, FR-09 | Model/migration/save/list/remove | AC-37–AC-39; watchlist portions AC-03, AC-07, AC-17, AC-40 |
| INC-04 | Genres/recommendations | FR-16, FR-10, FR-03, FR-12, FR-04, FR-01 | Browse/related pages | AC-19, AC-21, AC-33–AC-36; portions AC-07, AC-08, AC-40, AC-43 |
| INC-05 | Surprise Me/Try Again | FR-11, FR-03, FR-04, FR-01 | Random view/details | AC-24–AC-27; portions AC-07, AC-40 |

**November 18:** Complete INC-01 before movie features. Prove valid login, invalid-login rejection, protected access, anonymous denial/redirect and logout ending access. Required screenshots: sign-in, protected page after login, and restricted access after logout. Use a runnable Django/SQLite project, not admin login alone.

**Later targets:** Registration/API details November 22; watchlists November 24; genres/recommendations November 27; random discovery November 30. Complete full shared criteria by December 3; reserve December 4–7 for fixes and the video. API access is needed before INC-03.

## 10. Verification and delivery plan

Use fictional accounts and controlled API responses for repeatable Django tests. Browser checks confirm visible behavior; a separate live check confirms TMDb access. Record actual outcomes in the build log.

| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|
| AC-01, AC-02, AC-03, AC-04, AC-27, AC-42 | Valid/invalid accounts; anonymous visitor | Log in, request every protected route directly, log out/revisit, open welcome | Valid dashboard access; invalid/anonymous requests denied; logout ends session; welcome stays public | Django access/session tests and browser sequence; full dashboard checked after movie features |
| AC-15, AC-16 | Unused/duplicate username; matching, mismatched or rejected passwords | Register | Valid registration creates one account and automatically opens authenticated dashboard; invalid forms create none | Form, account-count and session tests |
| AC-07, AC-17, AC-28, AC-41 | Popular/detail responses; absent/failed poster, missing fields or movie ID | Follow dashboard navigation and all detail entry paths | Required fields and links work; placeholders or honest unavailable/not-found messages appear | View/template tests plus browser image-load and navigation checks |
| AC-08, AC-20, AC-21 | Blank/unknown title; empty search, browse or related response | Submit requests | Blank input rejected before API call; appropriate no-results message; original details still accessible when recommendations are empty | Mocked form/view tests checking messages and calls |
| AC-19, AC-23, AC-36 | Same-title IDs; recommendation A/B/B for selected A | Select each match and request related movies | Selected ID used; B appears once; A excluded; recommendations come from TMDb | Mocked request/result assertions and browser sequence |
| AC-24, AC-25, AC-26 | A/B/C candidates, one candidate and empty set | Surprise Me/Try Again | One eligible movie or helpful empty message; another selection request; repeats allowed | Control random choice in tests; verify candidate membership and retry behavior |
| AC-33, AC-34, AC-35 | Comedy; Comedy + Family; empty/invalid IDs | Browse each selection | A/B for Comedy, only B for both; invalid submission rejected before API call | Request-parameter and result tests; confirm live ALL semantics in AC-43 |
| AC-37, AC-38, AC-39 | Two users independently save B | Save twice, restart, attempt cross-user access/removal, remove own entry, try GET mutation | One persistent save per user/movie; only owner's entry visible/removable; GET cannot mutate | Database/ownership/CSRF tests and same-database restart check |
| AC-40 | Timeout, authorization error, rate limit or malformed response; saved title exists | Request affected movie features and watchlist | Helpful service error without secrets; saved titles remain visible | Mocked failure tests; distinguish failure from empty data |
| AC-43 | Secure, permitted TMDb setup | Live popular, search, details, recommendations and ALL-genres requests | Real responses render or honestly show empty data; endpoint behavior and attribution recorded | Separate live integration checklist; fictional responses cannot satisfy this check |

Run Django system/migration/feature checks and record actual results. Sample responses do not prove live access; keep secrets out of evidence.

**December 7 video:** Show welcome/accounts/dashboard (FR-17, FR-08, FR-01, FR-09), search/details/recommendations/posters (FR-10, FR-03, FR-12), ALL genres (FR-16), Surprise Me (FR-11), private saves/removal/persistence (FR-06), an error (FR-04), and logout/protected access. Explain the diagrams and design choices. Supporting tests cover edge cases. Label simulated errors; record timestamps/link. Hosting is not required.

## 11. Decisions, risks, and student explanation

| Decision / Open risk | Reason or response |
|---|---|
| Django | Built-in forms, templates, authentication and database tools keep the full-stack application in one Python project. This avoids a separate frontend framework or custom login system. |
| SQLite | A local database file is sufficient for course accounts and watchlists and does not require running another database server. User relationships and uniqueness rules support private, persistent saves. |
| TMDb | Supplies movie information, posters and recommendations without preparing a CSV catalog or writing a ranking algorithm. The tradeoff is dependence on external access and changing data. |
| API access and terms | Before API work, use [TMDb documentation](https://developer.themoviedb.org/docs/getting-started) to confirm credentials, costs, limits, attribution, image use and permitted title storage. If access is blocked, discuss the scope rather than silently change the source. |
| Missing or changing information | Confirm rating scale and ALL-genre syntax; use timeouts/placeholders. Stable sample-response tests check local behavior; AC-43 checks live integration separately. |
| Watchlist privacy and duplicates | Set ownership from the session, filter queries by user, enforce unique saves and test access with two accounts. |
| Schedule and review | Finish the November 18 foundation first; keep later features within the six increments. Confirm compatible Python/Django versions, inspect GitHub diagrams and record instructor feedback. No removed feature is restored. |

**Student explanation — draft to personalize:** A search goes from the browser to a Django view, which checks login/input and asks TMDb for movies. A template displays the response. SQLite links each saved movie ID/title to its user's account, so authentication keeps watchlists private. Django's forms, templates and login tools fit a Python course project; SQLite provides persistence without another database service. TMDb supplies movie information instead of a CSV catalog.

Before submitting, personalize this explanation and review the diagrams. API access/terms and instructor review remain open.
