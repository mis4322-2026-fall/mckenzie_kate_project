# System Design

## 1. Design baseline
- Project: Movie Finder — Kate McKenzie
- Proposal: [01-proposal.md](01-proposal.md), revised November 11, 2026
- Status: Draft — all eleven sections written; student review and API verification remain pending; diagrams are embedded as rendered images. Not ready for build.
- Instructor feedback: None supplied; instructor review pending.

### November 11 scope revision

The proposal is the current scope authority. Python/Django, templates, HTML/CSS, built-in authentication, and SQLite remain. TMDb is now the required source for popular movies, title search, multi-genre browsing, movie details, posters, popularity, and available movie-based recommendations. It is no longer an optional enhancement. API access, current terms, costs, attribution, endpoint semantics, and rating scale remain unverified; nothing is implemented or tested.

SQLite stores users, sessions, and private watchlist entries, not a CSV movie catalog. Each saved entry is planned to contain a user reference, TMDb movie ID, minimal title snapshot, and saved timestamp, with a unique user/movie pair. A local Movie model is not required for discovery. Movie details and recommendations use TMDb IDs, not arbitrary title matches. The title snapshot keeps a watchlist readable during outages; it does not provide an offline movie database.

The public welcome page offers registration/login. All discovery, dashboard, details, and watchlist pages require sign-in. The dashboard shows popular movies plus title search, multi-genre browsing, Surprise Me, and My Watchlist navigation. Multiple genres use ALL matching, never ANY. Surprise Me samples a bounded popular-movie response; Try Again can repeat a movie. Details require poster or placeholder, title, genres, numeric rating, and description. Recommendation ordering is supplied by TMDb, not a custom genre/storyline ranking algorithm.

Removed: CSV download/import, SQLite discovery queries, minimum-rating/runtime/release-year filters, required runtime display, trailers/hover previews, streaming availability, personal ratings, watched status, and personalized recommendations. TV shows remain future work. Existing core registration, title search, and Surprise Me goals are retained rather than described as newly invented features.

### Traceability changes

- Retained/updated: FR-01, FR-03, FR-04, FR-08–FR-11. FR-06 (private watchlists) and FR-12 (posters) are now Must.
- Retired: FR-02; replaced by new FR-16 for multi-genre API browsing. FR-05 remains retired. FR-13–FR-15 are retired with trailers, streaming, and storyline scoring.
- New FR-17 defines the public welcome page. No retired ID is reassigned.
- Retired checks: AC-05, AC-06, AC-09, AC-13, AC-14, AC-18, AC-22, AC-29–AC-32; AC-10–AC-12 remain retired. The proposal lists retained checks and new AC-33–AC-43.

These changes supersede earlier diagrams and baseline notes about optional APIs and local movie filtering. Sections 2, 3, and 5 below contain the architecture, data model, and user workflow. All eleven sections now contain a draft against the revised proposal. The review items in section 11 remain open; planning text is not implementation evidence.

## 2. System context

### Movie Finder — System Architecture

Proposed architecture, not an implemented system.

![Movie Finder — System Architecture](diagrams/system-architecture.png)

[Full-size SVG](diagrams/system-architecture.svg) · [Editable Graphviz source](diagrams/system-architecture.dot)

TMDb supplies movie information, numeric ratings, popularity, and available movie-based recommendations. Posters load from its supplied image references. SQLite stores accounts, sessions, and saved movie references with a minimal title snapshot; it is not a local movie discovery catalog. During an API outage, saved titles remain readable, but current details and discovery may be unavailable. Django keeps API credentials server-side and converts errors into helpful messages. API access, current terms, attribution, and endpoint behavior remain unverified.

## 3. Data model

### Movie Finder — Data Model (ERD)

Proposed persistent entities. User is Django's built-in user model; the diagram lists relevant fields rather than every built-in field. Standard Django session tables are omitted for readability.

![Movie Finder — Data Model (ERD)](diagrams/data-model.png)

[Full-size SVG](diagrams/data-model.svg) · [Editable Graphviz source](diagrams/data-model.dot)

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|
| User | id | Built-in primary key | Automatic | Unique identifier | One user owns zero or more saved entries |
| User | username | Built-in CharField | Required | Django username validation; unique | No movie ownership implied |
| User | password | Built-in CharField | Required for password login | Django stores a hash; validate passwords through built-in forms | Never store plain-text passwords |
| User | is_active, is_staff, is_superuser | Built-in BooleanFields | Django defaults | Built-in authentication/admin checks | Staff/admin permissions do not make other users' watchlists public |
| WatchlistEntry | id | BigAutoField | Automatic | Unique primary key | Identifies one saved entry |
| WatchlistEntry | user | ForeignKey to settings.AUTH_USER_MODEL | Required | Set from request.user, not a submitted user ID | CASCADE: deleting a user removes their saved entries |
| WatchlistEntry | tmdb_movie_id | PositiveIntegerField | Required | Positive valid TMDb identifier; unique together with user | External reference, not a foreign key to a local Movie table |
| WatchlistEntry | title_snapshot | CharField(max_length=500) | Required | Nonblank, length validated | Minimal saved title, readable during API outages |
| WatchlistEntry | saved_at | DateTimeField(auto_now_add=True) | Automatic | Server-generated timestamp | Removed with its saved entry |

A database unique constraint on `(user, tmdb_movie_id)` prevents duplicate saves. Every normal watchlist view and removal query is filtered by `request.user`; another user's entry must not be readable or removable by changing an ID. Removing a saved entry leaves the account, other users' entries, and TMDb movie unchanged. Save/remove actions use CSRF-protected POST requests. No local Movie model, personal ratings, watched status, or movie-history table is planned.

## 4. Pages and actions

These are proposed local application routes, not TMDb endpoint URLs or implemented pages. Only the welcome, registration, and login pages are public. Django checks authentication on every other route, including direct requests. Movie IDs refer to TMDb; entry IDs refer to the current user's saved SQLite entries.

| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|
| FR-17 | Welcome `/` | GET: open website | No login or input required | `welcome.html`: introduction, Log In and Create Account links |
| FR-08, FR-04 | Register `/accounts/register/` | GET: show form; POST: create account | Unique username, password and confirmation; Django user-creation/password validators; CSRF protection | `registration/register.html`: field errors on failure. On success, automatically authenticate the user, create the Django session and redirect to `/dashboard/`, consistently with the proposal. |
| FR-01, FR-04, FR-09 | Login `/accounts/login/` | GET: show form; POST: sign in | Django authentication validates username/password; generic invalid-credentials message; CSRF protection | `registration/login.html`; successful login redirects to `/dashboard/`. No movie data is exposed before sign-in. |
| FR-01 | Logout `/accounts/logout/` | POST only: end session | Authenticated session; CSRF token; GET must not log the user out | Redirect to public welcome page. Protected routes require sign-in again. |
| FR-09, FR-12, FR-04 | Dashboard `/dashboard/` | GET: show popular movies and navigation | Login required; server-side request for popular TMDb movies | `dashboard.html`: popular cards, search bar, genre browsing, Surprise Me and My Watchlist. Show a readable message if popular data is unavailable; navigation remains usable. |
| FR-10, FR-12, FR-04 | Title search `/movies/search/?q=...` | GET: submit title or open search form | Trim surrounding spaces; require nonblank title when submitted; planned maximum 200 characters; do not assume exact title matching by TMDb | `movies/search.html`: selectable matches identified by TMDb ID, an empty-result message, or a validation/service error. Initial visit without a query shows the form. |
| FR-16, FR-12, FR-04 | Genre browsing `/movies/browse/?genre=...&genre=...` | GET: show genre choices and submit selections | Initial visit shows form; submitted browsing requires at least one genre. Validate each ID against the available TMDb genre list, remove repeated IDs, and request ALL selected genres. If the genre list cannot be retrieved, show an unavailable message. | `movies/browse.html`: selected choices, matching cards, or helpful validation/empty/API-error message. No rating, runtime or year filters. |
| FR-11, FR-03, FR-12, FR-04 | Surprise Me `/movies/surprise/` | GET: request one random movie; Try Again repeats the request | Login required; select from a bounded valid popular-movie candidate response. Empty candidates and API failures must be handled; immediate repeats are allowed. No saved records are changed. | On success redirect to `/movies/<tmdb_id>/` with a random-discovery context flag so Try Again can return here; otherwise `movies/surprise.html` displays the error and retry/home navigation. |
| FR-03, FR-12, FR-04 | Movie details `/movies/<tmdb_id>/` | GET: select a movie card or saved title | Positive movie ID; validate TMDb response; unknown ID produces a not-found message. A context flag may control Try Again visibility but must never control access or ownership. | `movies/detail.html`: poster/placeholder, title, genres, rating/scale, description, Save control, recommendation link, and dashboard navigation; Try Again for random discovery. Missing fields are honestly labeled. |
| FR-10, FR-12, FR-04 | Related movies `/movies/<tmdb_id>/recommendations/` | GET: request movie-based recommendations | Login required; validate source ID; use TMDb recommendation results without custom storyline scoring. Remove original and repeated movie IDs; distinguish empty responses from request failures. | `movies/recommendations.html`: related cards linking to details, or helpful empty/error message with a link back to the selected movie. |
| FR-06, FR-01 | My Watchlist `/watchlist/` | GET: view saved entries | Query SQLite by `request.user`; no submitted user ID selects the owner | `watchlist/list.html`: only my saved titles, detail links and Remove forms, or an empty-watchlist message. Title snapshots stay visible during TMDb outages; no API call is required just to list saved titles. |
| FR-06, FR-04 | Save movie `/watchlist/add/` | POST only: save movie | Login and CSRF required; positive submitted TMDb ID; obtain/validate the title server-side from TMDb rather than trusting a client title. Set owner from `request.user`; enforce unique user/movie pair. If the same movie is already saved, leave one entry and show an already-saved message. If new movie validation fails, do not create an incomplete entry. | Redirect to `/watchlist/` with saved/already-saved/error feedback. GET cannot create entries. |
| FR-06, FR-01 | Remove movie `/watchlist/<entry_id>/remove/` | POST only: remove my saved entry | Login and CSRF required; fetch by both entry ID and `request.user`. Unknown or another user's entry returns a generic not-found response without exposing its owner. | Delete only that entry and redirect to `/watchlist/`. Other users' entries remain intact; GET cannot remove entries. |

### Navigation and shared page behavior

- The dashboard links to the three discovery methods and My Watchlist; popular cards open details. Authenticated pages provide a dashboard link and a POST logout form.
- Search, browse and recommendation cards use a shared movie-card layout with title and poster/placeholder. Details supply the required full movie information. Watchlist rows can use their stored title snapshots without fetching every saved movie remotely.
- All forms have visible labels and helpful errors. Poster alternative text identifies the movie; a failed or absent image uses the same local placeholder. Templates escape movie text and user input.
- Read-only discovery uses GET. Registration, login, logout, saving and removal use CSRF-protected POST. Save/remove controls identify the movie or saved entry, never the acting user.
- TMDb failures leave a readable page with retry and dashboard links. No raw credential, traceback, or technical API response is displayed. Public welcome and local account pages do not depend on movie-service availability.

Registration automatically authenticates the new user and redirects to the protected dashboard, consistently with the revised proposal and flowchart. This is planned behavior, not an implemented feature. No new requirement IDs are introduced in this section.

## 5. Main user flow

### Movie Finder — Main User Flow

All steps are proposed. The rendered chart flows downward; short continuation notes replace long return arrows. All dashboard, discovery, details, and watchlist requests require login, even when a URL is entered directly.

![Movie Finder — Main User Flow](diagrams/main-user-flow.png)

[Full-size SVG](diagrams/main-user-flow.svg) · [Editable Graphviz source](diagrams/main-user-flow.dot)

**Account flow:** Successful registration automatically authenticates the new user and redirects to the protected dashboard. Valid login does the same. Invalid registration or login shows errors and allows retry without granting access. The proposal and design now use this same rule.

**Continuations:** Rounded continuation nodes describe navigation rather than separate application features. Retry returns to the selected account form. Try Again repeats the random-selection request; immediate repeats are allowed. A saved movie opens the same Details page used by discovery. Recommendation results use the same results/details flow. Return-home actions lead back to the protected dashboard. The chart avoids drawing those long return lines across other branches.

**Missing information:** Failed TMDb requests and empty results show helpful messages. An unavailable movie ID shows a not-found message rather than invented details. Missing posters use a placeholder; missing ratings/descriptions are labeled unavailable. Empty watchlists remain usable. These messages never expose credentials or tracebacks. No trailers, streaming availability, numeric filters, or release-year filters are included.

## 6. Access and login

This section plans access for FR-01, FR-06, FR-08, FR-09, and FR-17. Authentication proves which user is signed in; ownership checks determine which saved entries that user can access. Both checks happen on the server, not only in navigation links.

| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|
| Visitor — signed out | Open the public welcome page, create an account, or log in | Cannot access the dashboard, discovery, details, recommendations, random selection, or watchlist. Direct protected URL requests redirect to login or deny access. |
| Authenticated user | View popular movies, search, browse genres, request recommendations, use Surprise Me, view details, manage their watchlist, and log out | Every protected view checks the session. Saved entries are read, created, or removed only for `request.user`; a client cannot select another owner. |
| Administrator — active superuser for the course demo | Log in at `/admin/` to manage built-in users and registered WatchlistEntry records | Separate Django Admin access and model permissions. Administrative management can include all users' entries; ordinary application watchlist views remain owner-filtered even when an administrator uses them. No local movie catalog is administered. |

### Registration and sign-in

Use Django's built-in user model, UserCreationForm, authentication forms, and session framework. Registration validates a unique username and passwords entered twice, using Django's configured password validators. Django hashes passwords; the application never stores or compares plain-text passwords itself. Invalid registration shows field errors without creating an account.

Following the current flowchart and section 4, successful registration establishes a Django authenticated session and redirects to `/dashboard/`. Returning users sign in through Django's login view; valid credentials also redirect to the dashboard. Invalid credentials display a generic helpful error and do not grant access. This direct-to-dashboard registration behavior is now consistent in the proposal and design.

Account creation and login use CSRF-protected POST forms. Django manages session identifiers through its standard session middleware and cookies, with session records stored in SQLite. The browser does not receive stored password hashes. Public welcome/login/registration work without TMDb; a movie API failure after login shows an unavailable message rather than preventing account access.

### Protected pages and watchlist ownership

Apply Django's `login_required` decorator or equivalent LoginRequiredMixin to dashboard, title search, genre browsing, Surprise Me, movie details, recommendations, and every watchlist action. Hiding a link is not access control. The public welcome page stays accessible without authentication.

The login destination is `/accounts/login/`; the application always sends successful login to `/dashboard/` for a predictable course workflow. No arbitrary external redirect supplied by a user is accepted. A signed-in user's watchlist query filters by `request.user`. A removal looks up both the entry ID and that owner, returning a generic not-found response for missing or unauthorized entries. A save takes its owner from the session, never a posted user ID. The unique user/movie constraint prevents duplicate saves. These rules also protect direct URL and forged form requests.

Saving and removing require CSRF-protected POST; GET requests do not change saved entries. The details page may show Save or Remove controls, but the server repeats authentication and ownership checks regardless of what the browser displays. A normal user receives no administration privileges through registration.

### Secure logout and Django Admin

Logout is a CSRF-protected POST to `/accounts/logout/`. Django clears the authenticated session and redirects to the public welcome page. A subsequent request for any protected page requires sign-in again; checking this means making a new request, not relying on an old page left visible in a tab. GET does not log a user out.

Django Admin is a staff management interface, not the user-facing Movie Finder login or dashboard. The first build must include a separate sign-in page and a protected application page even before movie features are added. A working `/admin/` login alone does not meet the initial-build requirement.

### Demonstration users and planned checks

During the foundation build, create a local demonstration account using Django's `createsuperuser` command with its interactive password prompt; a separate ordinary account will demonstrate normal access once registration is available. Use two fictional ordinary accounts for the ownership test. Passwords, session cookies, API tokens, the local SQLite database, and real personal data must not be committed or shown in screenshots or recordings. Registration, not shared default credentials, will let someone create their own local account.

Planned checks are valid and invalid login (AC-01–AC-02), anonymous direct access (AC-03), logout ending access (AC-04), valid/invalid registration (AC-15–AC-16), protected random discovery (AC-27), private watchlists and forbidden cross-user removal (AC-38), safe removal methods (AC-39), and public welcome access (AC-42). Initial-build screenshots will show the sign-in page, the authenticated protected page, and the sign-in requirement after logout. No check or screenshot has been executed or captured yet.

Password reset, email verification, social login, and additional business roles are outside the current scope. This is a local course application design, not a production authentication deployment.

## 7. Integrations and configuration

TMDb is the planned external movie source, not an optional enhancement. Django will make authenticated HTTPS requests on the server; SQLite remains local storage for accounts, sessions, and private watchlist entries. This section is a design plan: documentation links and endpoint names identify what to verify during implementation, not proof of working access. No credentials, API calls, downloads, installed dependencies, or successful responses are claimed.

| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|
| Django and Python | Routing, forms, templates, authentication, sessions and ORM | [Django documentation](https://docs.djangoproject.com/en/stable/), [Python documentation](https://docs.python.org/3/) | `DJANGO_SECRET_KEY`; optional local settings `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` | Select compatible supported versions and pin dependencies during the build. Foundation authentication must work without TMDb. |
| SQLite | Persist accounts, sessions and owner-linked saved entries | [Django database documentation](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) | None required for the planned local SQLite path | Apply migrations during setup; display clear setup instructions if the database is unavailable. Do not replace private data with fictional records or reset the database to hide errors. |
| TMDb API v3 | Popular movies, search, genres, ALL-genre browsing, details and movie-based recommendations | [Getting started](https://developer.themoviedb.org/docs/getting-started), [Application authentication](https://developer.themoviedb.org/docs/authentication-application) | `TMDB_READ_ACCESS_TOKEN` — planned server-side read-access bearer credential; verify current authentication instructions | Handle missing configuration, timeout, non-success status, malformed data and empty results. Use explicitly labeled fictional responses in automated tests; never silently present them as live TMDb results. |
| TMDb image service | Build poster references from documented image configuration and movie poster paths | [Image basics](https://developer.themoviedb.org/docs/image-basics), [Configuration details](https://developer.themoviedb.org/reference/configuration-details) | No separate image credential planned; metadata/configuration requests use the server-side TMDb credential | Use a local poster placeholder for absent references or failed image loads. Do not assume every movie has a poster. Verify image-use and attribution terms before display. |

### Planned movie requests

Use one small server-side client rather than repeating HTTP logic in every view. Base API destination: `https://api.themoviedb.org/3`. The paths below are planned API routes, distinct from the application's URLs in section 4.

| Operation | Planned API request | Used by / validation |
|---|---|---|
| Popular movies | `GET /movie/popular` | Dashboard and bounded Surprise Me candidate set; handle empty pages. |
| Title search | `GET /search/movie` with `query` | Trim and validate the submitted title before sending it. Select results by TMDb movie ID, not a title-only identity match. |
| Genre choices | `GET /genre/movie/list` | Build valid genre selections. If unavailable, explain the failure instead of guessing IDs. |
| Multi-genre discovery | `GET /discover/movie` with `with_genres` | Send validated IDs using documented AND semantics. The planned comma-separated format must be confirmed against current TMDb documentation and a live integration check; do not substitute OR behavior. |
| Movie details | `GET /movie/{movie_id}` | Positive validated ID; check required fields and handle not-found responses. |
| Movie-based recommendations | `GET /movie/{movie_id}/recommendations` | Use TMDb's returned recommendations, removing the original ID and duplicate IDs. Do not claim custom storyline scoring or personal-history ranking. |
| Poster configuration | `GET /configuration` and returned poster references | Use documented secure image base URLs and available sizes. Never concatenate unvalidated arbitrary URLs supplied by a user. |

Request parameter values will be encoded using the chosen Python HTTP client's supported parameter handling. API URLs come from configured application constants, not user-supplied destination URLs. No CSV, trailer, streaming-provider or AI-service integration is included. Exact API schema, rating scale, genre semantics, recommendation access and image configuration remain checks to complete before the API-dependent build.

### Authentication and local configuration

The planned TMDb authentication is an application read-access token sent as a server-side bearer credential, subject to current TMDb setup instructions. Kate will need suitable developer access before live integration. Never request or record the token in this document. The planned application variable is `TMDB_READ_ACCESS_TOKEN`; there is no need to add a second credential variable unless TMDb's verified instructions require it.

During implementation, document how the app reads process environment variables. If `.env.example` is supplied, it contains names and dummy values only; `.env` values are not loaded automatically by Django. The chosen loading method must be stated explicitly. Ignore real environment files, local SQLite data, and credentials in Git. Do not print tokens in logs, screenshots, errors, browser HTML or JavaScript. `DJANGO_SECRET_KEY` is separate from the TMDb credential. Development defaults for debug/allowed hosts must be documented as local-only settings, not production deployment instructions.

### Failure handling and test responses

- **Bounded requests:** Proposed initial timeout is 10 seconds per API request, to tune during implementation. Keep TLS verification enabled. Do not retry indefinitely or make unbounded page-by-page requests. The first version uses a bounded response page with clear result limits rather than claiming exhaustive catalog coverage.
- **Missing credentials or denied access:** Keep public/account pages and locally saved watchlist titles usable; show a movie-service-unavailable message for discovery. Missing configuration must not reveal token values or grant access to private records.
- **Timeouts, connection failures and service errors:** Return a readable unavailable message with retry/dashboard navigation. A rate-limit response receives a try-again-later message; confirm provider guidance before adding any retry behavior. Never expose upstream response bodies or tracebacks to users.
- **Malformed responses or missing fields:** Validate returned data before rendering or saving. Missing posters use a placeholder; missing descriptions/ratings are labeled unavailable, not fabricated or replaced by misleading zeroes. Unknown movie IDs show a not-found message.
- **Valid empty responses:** Distinguish no search matches, no recommendations and no random candidates from a service failure. The detail page remains usable when only recommendations are empty.
- **Watchlist persistence:** Existing saved title snapshots remain available during outages. New saves require server-side movie validation as described in section 4; a failed lookup does not create an incomplete entry. Ownership checks do not depend on TMDb.
- **Fictional tests:** Mock the client responses using the proposal's fictional movie examples, including empty, duplicate, unavailable-field and failure cases. This is test data, not a second production data source or an offline replacement for TMDb. Live access verification remains required separately (AC-43).

### Terms, attribution and outstanding verification

Before implementation, review the [TMDb API FAQ](https://developer.themoviedb.org/docs/faq) and current official terms for account eligibility, course/noncommercial usage, any charges, limits, permitted storage of movie IDs/title snapshots, image use, required credits/logos, and exact attribution wording. Do not assume access is free or unrestricted. Place verified attribution on an appropriate visible credits/footer area, following the current terms, without claiming TMDb endorses the project.

These items remain **Open**: credentials and network access; terms/costs and required attribution; all-genres request semantics; endpoint response fields and rating scale; image configuration; and a successful live popular/search/details/recommendations/browse check. They do not block planning or the local authentication foundation, but they do block claiming API readiness or complete movie discovery. No external connection is made as part of this section.

## 8. Outputs and business rules

These are planned rules for the required application, not calculations or outputs already implemented. Examples use fictional controlled responses so checks do not depend on changing live movie data. API field formats, rating scale, and request semantics still need verification.

| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|
| FR-17, FR-01 | Public welcome and protected application | Welcome, login and registration are public. Dashboard, discovery, details, recommendations and watchlist require an authenticated session on every request. | A signed-out visitor can open `/` but is redirected to login when requesting `/watchlist/`. |
| FR-08, FR-01 | Registration and login feedback | Unique username; matching passwords accepted by Django validators. Invalid input shows errors without granting access. Successful registration automatically creates an authenticated session and redirects to the dashboard. | A duplicate `demo_viewer` username produces a form error, not a second account. |
| FR-09, FR-12 | Popular-movie dashboard | Show the available popular results in TMDb response order, with duplicate movie IDs removed while retaining first occurrence. Popularity is supplied by TMDb, not calculated from watchlists or treated as a review score. | A controlled response containing A, B and B produces cards for A and B. |
| FR-10 | Title-search matches | Trim surrounding spaces; reject blank or overlong input as specified in section 4. Use TMDb search behavior and retain response order; select movies by ID rather than assuming an exact title match. Deduplicate by movie ID, not title. | Two records titled Moonlight Picnic with different TMDb IDs remain individually selectable. |
| FR-16 | ALL-selected-genres matching | Require at least one valid genre ID. A movie qualifies only if its genres contain every selected genre: selected genres are a subset of movie genres. Deduplicate selected IDs before requesting documented TMDb AND behavior. | Selecting Comedy and Family includes Garden of Laughs (both genres), but excludes Moonlight Picnic (Comedy only) and Clockwork Harbor (Mystery). |
| FR-10 | Movie-based recommendations | Request TMDb recommendations for the chosen movie ID. Exclude that original ID; remove duplicate IDs and retain the remaining provider order. Do not add custom genre counts, storyline scores or user-history ranking. | For selected A, response `[A, B, B, C]` displays B then C. An empty list produces a no-recommendations message without hiding A's details. |
| FR-11 | Surprise Me selection | Use a bounded valid popular-movie candidate page. Keep candidates with a usable positive movie ID and title, remove duplicate IDs, and choose one candidate with equal probability within that set. This is not a uniform sample of the entire TMDb catalog. | Controlled candidates A, B and C each have a 1-in-3 chance for that selection. |
| FR-11 | Try Again | Make a new selection request using the same candidate-source rule. Immediate repeats are allowed; no viewing history or last-result exclusion is required. | A followed by A is valid. A single-candidate response still works. |
| FR-03 | Movie details | Show title, genre names, numeric rating with its verified scale, and description on a separate page. Runtime, personal ratings and watched status are excluded. Ratings are descriptive API data, not a promise that the user will enjoy the movie. | Fictional Garden of Laughs shows Comedy and Family, 7.2/10 if that scale is verified, and its supplied description. |
| FR-03, FR-04 | Missing movie information | Distinguish missing values from genuine supplied values. Use field-unavailable text; do not invent a rating or description. An unknown/deleted movie ID gets a not-found message. Missing essential ID/title data does not create a blank selectable card. | A missing description displays “Description unavailable”; a missing score is not silently changed to 0. |
| FR-12 | Posters | Display only supplied image references using verified TMDb image configuration. Use meaningful alternative text and the local placeholder when a poster is absent or fails to load. | A posterless movie retains its title, details link and Save control. |
| FR-06 | Saving a movie | Set owner from the session; validate the movie ID and obtain the title server-side. Save one WatchlistEntry per `(user, tmdb_movie_id)` pair using a database constraint. Repeat requests do not create duplicates. | Saving fictional movie B twice leaves one entry in user One's watchlist. |
| FR-06 | Private watchlist output | Read entries filtered by the signed-in user. Display stored title snapshots and detail/remove controls; planned ordering is newest saved first, with entry ID as a stable tie-breaker. No live API request is required to list saved titles. | User Two cannot see user One's saved B, even though both users may independently save B. |
| FR-06, FR-01 | Removal and persistence | POST with CSRF and owner lookup deletes only the user's selected entry. GET never saves/removes entries. Data persists in SQLite across restart. Removing a save does not delete a TMDb movie or another user's save. | User One removes B; user Two's independently saved B remains. |
| FR-04 | Empty versus failed results | Empty valid responses show feature-specific no-results messages. Network/authentication/rate-limit/invalid-response failures show service-unavailable messages and retry/home navigation, not a misleading no-matches claim. | No recommendations is different from “Movie service unavailable. Please try again.” |

### Worked genre and recommendation examples

The fictional sample movies are A: Moonlight Picnic (Comedy), B: Garden of Laughs (Comedy, Family), and C: Clockwork Harbor (Mystery). Browsing Comedy matches A and B; browsing Comedy plus Family matches only B. No minimum-rating, runtime or year threshold is applied. The selected-genre combination must be checked against TMDb's documented all-genres request behavior before claiming live integration works (AC-33–AC-35, AC-43).

These genre examples do not predict TMDb's recommendation algorithm. Recommendation tests instead supply a controlled response with known IDs and verify original/duplicate exclusion and preserved provider ordering (AC-19, AC-36). Fictional recommendation relationships are not presented as live provider facts.

### Limits and unchanged scope

Each discovery operation uses bounded API results as specified in section 7. The first version does not promise every matching movie or unlimited pagination. A failed details request after selecting a random or saved movie shows the same honest unavailable message as other detail requests. Existing watchlist snapshots remain readable during outages; they are not a full offline movie catalog.

No trailers, streaming providers, CSV import, personal ratings, watched status, release-year/rating/runtime filters, custom storyline similarity or viewing-history personalization are introduced here. Rules link to the existing proposal IDs; no requirement or acceptance-criterion ID is reassigned. All examples and checks remain planned.

## 9. Build increments

These are planned implementation steps, not completed work. Increment IDs identify build steps and are different from course deliverable numbers. Build one demonstrable outcome at a time, verify it, and record actual results in the build log before continuing. No existing increment IDs were present; INC-01–INC-06 are assigned here for future tracking.

| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|
| INC-01 | Runnable Django/SQLite foundation: public welcome, user-facing login, protected application landing page and POST logout, before movie features. | FR-01, FR-17; foundation portion of FR-09 | Base project, migrations, Django User/session tables, welcome/login templates, protected dashboard shell, logout form and locally created demonstration account. No TMDb dependency. | AC-02, AC-04, AC-42; foundation-only portions of AC-01 and AC-03. Popular movies and later protected routes are verified in subsequent increments. |
| INC-02 | New users register and reach the protected dashboard shell; invalid submissions show errors. Navigation layout is usable before live movie data is added. | FR-08, FR-01; navigation portion of FR-09 | Registration form/template, Django password validation, authenticated session after registration, shared page layout and account navigation. | AC-15, AC-16; account/dashboard-navigation portion of AC-01. Full AC-17 remains pending movie features. |
| INC-03 | TMDb integration foundation: popular dashboard, title search, separate details pages and posters with readable empty/error states. | FR-09, FR-10, FR-03, FR-12, FR-04, FR-01 | Secure server-side client, popular/search/details/image requests, dashboard cards, search form, details template, placeholders and fictional mocked responses. No local movie catalog. | AC-01 popular/dashboard portion; AC-07 via search/popular cards, AC-08 search portion, AC-20, AC-23, AC-28, AC-41; AC-40 movie-request portion and AC-43 popular/search/details portion. |
| INC-04 | Multi-genre browsing and related recommendations work end to end, with ALL matching, empty states and original/duplicate exclusion. | FR-16, FR-10, FR-03, FR-12, FR-04, FR-01 | Genre-list and discover requests; browse form/results; recommendations view/results; existing details and cards reused. Verify current TMDb AND semantics. | AC-33–AC-36, AC-19, AC-21; AC-08 browse portion, AC-07 browse portion, AC-40 browse/recommendation portion and AC-43 remaining endpoint portions. |
| INC-05 | Surprise Me returns one valid movie; Try Again makes another selection request and handles empty candidates. | FR-11, FR-03, FR-04, FR-01 | Bounded popular-response candidates, random selection view, details redirect/context and retry control; no additional data model or viewing history. | AC-24–AC-27; AC-07 random-discovery portion and AC-40 random-request portion. |
| INC-06 | Private watchlists persist across restart, prevent duplicate saves and support safe owner-only removal. Complete navigation and final regression checks. | FR-06, FR-01, FR-03, FR-04, FR-09 | WatchlistEntry model/migration/unique constraint, admin registration, list/save/remove views, CSRF-protected forms and two fictional accounts. Reuse TMDb validation for new saves and details. | AC-37–AC-39; AC-07 watchlist portion, AC-40 saved-titles-during-outage portion. Finish full AC-01, AC-03 and AC-17 across all implemented routes; repeat the complete active acceptance checklist, including AC-43. |

### INC-01: Initial build for Deliverable 3

Target completion is **November 18, 2026**, following the supplied course deadline. Create a compatible, pinned Python/Django setup, a local SQLite database through migrations, and a non-admin protected application page. Use Django's authentication, not custom password storage. A locally created demonstration account is enough for this foundation; registration follows in INC-02.

Demonstrate valid login reaching the protected page, invalid credentials being rejected, an anonymous direct request being redirected/denied, and POST logout ending access. Capture screenshots of the sign-in page, protected page after sign-in, and access restriction after sign-out. Do not expose credentials in screenshots. An admin login alone does not satisfy this increment. The full proposal's AC-01 includes popular movies and navigation, so passing only the foundation login test must not be recorded as completing all of AC-01. Likewise, AC-03 must later cover every added protected route.

Plan to record environment/setup instructions, actual checks, pending screenshots and the student checkpoint in `deliverables/03-bootstrap.md`, with an INC-01 entry in `deliverables/04-build-log.md` during implementation. These are future build artifacts, not files or evidence created by this design step.

### Remaining schedule and dependencies

| Target window | Planned work | Completion evidence |
|---|---|---|
| November 11–18 | INC-01 foundation; keep API investigation independent so it cannot delay basic authentication. | Runnable local project, focused authentication checks, setup instructions and three initial-build screenshots. |
| November 19–22 | INC-02 registration and INC-03 popular/search/details integration. | Account validation, mocked API edge cases and representative live popular/search/details checks. |
| November 23–27 | INC-04 ALL-genre browsing and TMDb recommendations. | Controlled multi-genre and recommendation cases plus verified live request semantics. |
| November 28–30 | INC-05 Surprise Me. | One-candidate, empty-candidate, valid-selection and protected-access checks. |
| December 1–3 | INC-06 private watchlist and full navigation. | Two-user ownership tests, duplicate prevention, safe removal and persistence after restart. |
| December 4–7 | Fix defects, review the full criteria checklist, rehearse and record the final local video. | Demonstration of all Must requirements, useful outputs, an error case and design choices. Video submission remains Kate's responsibility. |

Dates after the initial-build deadline are proposed targets, not completed commitments. The final video deadline is **December 7, 2026**, as supplied in the assignment. Keep time for integration failures and testing rather than adding Later features.

Before INC-03, verify TMDb credentials, networking, terms, attribution, image use and required endpoint behavior. Mocked responses allow isolated development/testing but do not prove live integration or replace AC-43. If access remains unavailable, document the blocker and seek a scope decision; do not silently return to a CSV or invent successful API results. Account and SQLite work can continue independently.

INC-02 must implement the consistent proposal/design rule: successful registration automatically authenticates the user and redirects to the dashboard. For each increment, preserve IDs, use non-destructive migrations, update actual build-log evidence, and ask Kate to explain the request/data flow. No dependency installation, application code, migration, test execution, screenshot or API request is performed in this planning section.

## 10. Verification and delivery plan

All checks and evidence below are **planned and unrun**. No passing result, screenshot, recorded video or live TMDb access is claimed. Use fictional accounts and controlled fictional movie responses for repeatable tests, with a separate live integration check. Retired acceptance criteria are excluded rather than reassigned.

### Acceptance-criterion checklist

| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|
| AC-01 | Valid fictional account; popular response A and B | Sign in | Dashboard opens with popular movies and complete discovery/watchlist navigation | Django authentication/view test plus browser check; foundation evidence covers login only until movie features exist |
| AC-02 | Invalid credentials | Submit login | Helpful error; no authenticated access | Django client test checking session/access plus browser error display |
| AC-03 | Signed-out client; all protected route types | Request dashboard, searches, details, recommendations, random and watchlist routes directly | Redirect/deny access; no private data exposed | Route-by-route Django access tests; include save/remove requests |
| AC-04 | Authenticated session | POST logout, then request protected page again | Session ends; login required | Django client test with CSRF checks enabled plus browser sequence |
| AC-07 | Fictional B details response | Open details from search, browse, random discovery and saved entry | Separate details page shows required fields and poster/placeholder | View/template tests for every entry path and browser navigation checks |
| AC-08 | Empty search and browse responses | Submit valid searches | No-results message with retry/home path | Mocked view tests plus browser empty state |
| AC-15 | Unused fictional username and acceptable confirmed password | Register | Exactly one account created; account can access authenticated dashboard under the current design | Form/database/session tests plus registration browser check; verify automatic authentication and dashboard redirect |
| AC-16 | Duplicate username, mismatched passwords, rejected password | Submit each invalid registration case | Helpful errors; no new account | Form tests checking errors and account counts |
| AC-17 | Popular response containing A and B | Open dashboard and follow each navigation choice | Popular cards and search/browse/random/watchlist links work; return-home routes are usable | Mocked dashboard test and browser navigation checklist |
| AC-19 | Selected A; recommendations `[A, B, B]` | Open recommendations | B shown once; A excluded | Test returned movie IDs and rendered cards |
| AC-20 | Blank title; unknown title with empty response | Submit each search | Blank title rejected before API request; unknown title gets no-results message | Form/view tests asserting API call or no call as appropriate |
| AC-21 | Valid details; empty recommendation response | Request related movies | No-recommendations message; original details stay accessible | Mocked view test and browser navigation |
| AC-23 | Two title matches with different movie IDs | Select each result | Requests use the selected ID, not an arbitrary title match | Mocked client-call assertions and detail links check |
| AC-24 | Candidate response A, B and C | Click Surprise Me | One eligible candidate selected and displayed | Deterministic tests controlling the random choice; verify selected ID belongs to candidate set, not a flaky distribution test |
| AC-25 | Existing random result and valid candidates | Click Try Again | New selection request; one valid movie; repeats allowed | View/client-call test plus browser retry control |
| AC-26 | Empty random candidates | Request Surprise Me | Helpful empty-candidate message; no exception | Mocked view test and rendered retry/home links |
| AC-27 | Signed-out client | Request random-selection URL | Login required | Direct anonymous access test |
| AC-28 | Valid poster, absent poster and failing image URL | View movie cards/details | Poster or placeholder with meaningful alternative text | Template tests for absent references; browser checks for actual image-load failure |
| AC-33 | Fictional A and B match Comedy | Browse Comedy | A and B appear without numeric filters | Mocked browse test and request-parameter check |
| AC-34 | Select Comedy and Family; A is Comedy, B is both, C is Mystery | Browse selected genres | Only B qualifies; request uses verified ALL semantics | Parameter/validation test and controlled result test; live request behavior verified separately in AC-43 |
| AC-35 | Empty or invalid genre selection | Submit browse form | Validation error; invalid discover request not sent | Form/view tests and API no-call assertion |
| AC-36 | Search A/B; recommendation for A returns B | Select A and open related movies | Selectable title matches and API-supplied B recommendation | Mocked end-to-end view sequence plus browser sequence |
| AC-37 | User One; valid B details | Save B twice, restart server and reopen list | One saved entry persists | Database uniqueness/duplicate-request tests; manual restart check against the same SQLite file |
| AC-38 | One owns B; Two has a separate session | View Two's list and attempt removal of One's entry | One's data hidden and unchanged; access denied/not found | Two-user authorization tests, including forged entry IDs |
| AC-39 | Both users independently save B | One removes their entry; attempt GET mutations | Only One's entry removed; GET cannot mutate | Owner-filtered database tests with CSRF enforcement and HTTP method checks |
| AC-40 | Controlled timeout, denied credential, rate-limit or malformed response; saved title exists | Use each affected movie feature, then open watchlist | Helpful unavailable message, no leaked token/traceback; saved title visible | Mocked service-error tests, response-content checks and local-watchlist no-API dependency check |
| AC-41 | Unknown movie ID; absent description/rating | Open details | Not-found or field-unavailable message; no invented values | Mocked detail tests for each case |
| AC-42 | Signed-out visitor | Open public welcome | Registration/login links visible; discovery remains protected | Anonymous view test and browser screenshot |
| AC-43 | Securely configured TMDb credentials and permitted networking | Run representative popular, title search, details, recommendations and ALL-genre browse requests | Real data renders or honest empty states appear; response semantics and attribution recorded | Separate live integration checklist with redacted evidence; never substitute mocked passes for live success |

### Foundation evidence for November 18

INC-01 must produce a runnable Django/SQLite foundation before business features. Plan three screenshots: (1) the user-facing sign-in page, (2) the protected application page after successful sign-in, and (3) the redirect/denial or sign-in requirement after logout and a new protected-page request. Record invalid-login and anonymous-access checks as well. Do not use admin login as the sole demonstration.

Screenshots must come from the actual initial build and show no passwords, API tokens or session cookies. Record exact paths, actual outcomes and any missing evidence in the future bootstrap report/build log; leave them pending until captured. Full AC-01 and AC-03 remain partially unverified until popular movies/navigation and every later protected route are added.

### Build verification and evidence records

For each increment, run Django system checks, migration consistency checks, and the relevant existing/focused test suite during implementation. Confirm the intended tests executed; a zero-test run is not a passing verification. Record commands, date, test counts, results and failures in the build log. Keep pass, fail, skipped, blocked and unrun statuses separate. Preserve actual assertion failures rather than changing requirements to make checks pass.

Mocked tests establish local behavior with known responses. Browser checks establish form/navigation behavior and poster fallbacks. A same-database restart check establishes watchlist persistence. AC-43 establishes real integration access separately. Keep secrets out of logs and Git; identify the live requests performed without publishing credentials or private user records. Report any required criterion that remains blocked by service access.

### Final local video plan — December 7

| Demonstration step | Requirement IDs | Criterion IDs | What to show and explain |
|---|---|---|---|
| Introduce the problem and public welcome | FR-17 | AC-42 | Explain who benefits, the revised TMDb/SQLite split, and the public versus protected pages. |
| Register, log in and open dashboard | FR-08, FR-01, FR-09 | AC-15, AC-01, AC-17 | Show an account workflow, popular movies and navigation; explain Django authentication. Do not reveal passwords while recording. |
| Search and open a movie | FR-10, FR-03, FR-12 | AC-23, AC-36, AC-07, AC-28 | Show title matches, ID-based detail links, poster/title/genres/rating/description, and related recommendations. Explain server-side TMDb calls. |
| Browse multiple genres | FR-16 | AC-33, AC-34 | Show one genre and then multiple selected genres; explain ALL rather than ANY matching and the API dependence. |
| Request a random movie | FR-11 | AC-24, AC-25 | Show Surprise Me and Try Again; explain bounded candidates and allowed repeats without promising every movie is equally likely across TMDb. |
| Save and manage a private watchlist | FR-06, FR-01 | AC-37–AC-39 | Show save, duplicate-save prevention, persistence after restart, another fictional user's separate list, and safe removal. Explain the user/movie unique pair and ownership query. |
| Demonstrate a failure/empty case | FR-04, FR-03 | AC-20, AC-08, AC-40 or AC-41 | Show a blank/no-result search and a controlled unavailable response if needed. Explicitly label any controlled simulation; do not pretend it is a live outage. |
| Log out and prove access restriction | FR-01 | AC-02–AC-04, AC-27 | Show invalid login or its recorded test evidence, logout, and a direct protected-page request requiring login again. |
| Connect design to implementation and evidence | All active Must requirements | Full checklist including AC-43 | Briefly show URL → view → TMDb/ORM → template, the ERD, checks and any remaining limitations. Explain design choices and AI assistance. |

A video samples important user-visible behavior; supporting test results must cover the remaining acceptance cases instead of claiming the recording proves every edge case. Use real TMDb results for the live integration portion, recognizing titles, ratings and recommendations may change. Do not promise fixed live recommendation relationships or order.

The final demonstration is local; public hosting is not required. Review every active Must requirement against evidence before declaring completion. Video link, timestamps, recording, student narration and submission status remain pending until Kate supplies them. No video length is imposed here. No tests, screenshots, API requests or recordings were executed for this design section.

## 11. Decisions, risks, and student explanation

### Design decisions and reasons

| Decision | Reason | Status / Requirement connection |
|---|---|---|
| Use Django templates, HTML and CSS with Python views and forms | One full-stack project is easier to develop and explain than separate frontend/API applications. Built-in forms and authentication avoid custom account handling. | Selected stack; FR-01, FR-08 and all application pages |
| Use TMDb rather than a downloaded CSV | One movie source supports popular titles, search, genres, details, posters and provider-generated recommendations without maintaining a local discovery catalog. | Kate's November 11 scope change; API access and terms remain unverified |
| Store accounts, sessions and watchlists in SQLite | Meets the course database requirement and supports persistent personal saves without a separate database service. | FR-01, FR-06, FR-08; local course workflow |
| Save TMDb IDs and a minimal title snapshot | IDs identify movies even when titles repeat. A saved title remains readable during API outages without storing a complete movie dataset. | FR-06; permitted snapshot storage must be confirmed under current TMDb terms |
| Require authentication after the public welcome | Keeps discovery and saved-list workflows behind consistent access checks while allowing new users to register. | FR-01, FR-17 |
| Enforce ownership in every watchlist query and mutation | An entry ID alone must not allow one user to see or remove another user's saved movie. | FR-06; unique user/movie constraint and CSRF-protected POST saves/removals |
| Match ALL selected genres | Makes multi-selection predictable and follows the revised proposal rather than returning any loosely related genre. | FR-16; TMDb request semantics still need verification |
| Preserve TMDb recommendation order after removing the selected ID and duplicates | Avoids a custom similarity algorithm, machine learning and viewing-history tracking. | FR-10; do not claim knowledge of TMDb's internal ranking logic |
| Sample one bounded popular-result candidate set for Surprise Me | Achievable without requesting or storing the entire catalog. Try Again allows repeats. | Proposed implementation detail for FR-11, recorded in the proposal |
| Use placeholders and explicit unavailable messages | Missing external information should not break navigation or be replaced with fabricated data. | FR-03, FR-04, FR-12 |
| Exclude trailers, streaming availability and extra filters | Keeps implementation focused on the revised Must requirements and the remaining course timeline. | Retired IDs remain retired; no removed feature is silently restored |

### Risks and responses

| Risk | Impact | Planned response |
|---|---|---|
| TMDb credentials, network access, terms or endpoint behavior cannot be verified | API-dependent movie features cannot be claimed ready. | Complete the section 7 checks before INC-03. Continue independent authentication/SQLite work; document a blocker and request a scope decision if required access is unavailable. Do not silently switch back to CSV. |
| Timeouts, limits or malformed responses | Discovery may temporarily fail. | Bound requests, preserve readable error/navigation paths and test controlled failures. Existing saved titles remain visible locally. |
| Changing movie data or empty recommendations | Fixed live examples may stop matching expected results. | Use fictional mocked responses for repeatable assertions and separate live evidence for real access; do not promise a specific recommendation relationship. |
| Missing posters, descriptions or ratings | Results can be incomplete. | Use placeholders and unavailable labels; never invent a score or description. |
| Cross-user access or duplicate saves | Privacy or persistence requirements fail. | Owner-filtered queries, session-derived owners, unique constraints, CSRF checks and explicit two-user tests. |
| Limited candidate sampling | Surprise Me is not random across every movie. | Explain the bounded candidate set honestly; allow immediate repeats without collecting user history. |
| Time pressure before November 18 and December 7 | A large unfinished build could undermine the demo. | Finish authentication first, build in the six documented increments and reserve the final window for defects and evidence. Do not add Later features. |

### Open questions and review items

| Item | Owner | What remains to resolve |
|---|---|---|
| Registration redirect consistency | Kate | Resolved in planning: successful registration automatically authenticates the user and redirects to the protected dashboard. Proposal and design are aligned; implementation remains future work. |
| TMDb setup and policy checks | Kate during implementation | Confirm access, authentication instructions, costs, terms, required attribution, image use, permitted title-snapshot storage and request limits. No values belong in the documents. |
| API behavior and output formats | Kate during implementation | Confirm rating scale, ALL-genre parameter behavior, response fields and recommendation availability. AC-43 needs separate live evidence. |
| Runtime versions | Kate during initial build | Choose compatible supported Python/Django versions using official documentation and pin the actual installed dependencies; no toolchain installation is part of this design. |
| Instructor review | Instructor / Kate | No instructor feedback or approval evidence has been supplied. Record any later requested scope/design changes while preserving IDs. |
| Diagram display | Design review | All three diagrams are rendered PNGs embedded directly in this document, with SVG and editable Graphviz sources. Local visual inspection is recorded below. Remote GitHub display must still be checked after pushing. |
| Student explanation and final evidence | Kate | Review the explanation below, supply it in your own words, and later provide actual screenshots, test results, video timestamps and submission evidence. |

### Student explanation checkpoint

Kate's earlier description was that users search for a movie they like or a particular genre and then see results. Kate also explained that Django and SQLite were chosen because the professor requires them. That explains the user goal and course constraint; it is not yet a complete explanation of the request and data flow.

**Learning guide — not a statement attributed to Kate:** A browser sends a movie-search request to a URL. Django routes it to a view, checks the authenticated session, and validates the search text. For movie discovery, the view calls the server-side TMDb client; for a watchlist, it uses Django's ORM to query only the current user's SQLite entries. The view passes results or a helpful error to a template, which produces the HTML response shown in the browser. A Save action uses a protected POST request to create a user-linked entry in SQLite; it does not alter TMDb.

Django fits because it provides routing, forms, templates, authentication and database tools in one Python application. SQLite fits because the local course project needs persistent accounts and private watchlists without running another database server. TMDb avoids preparing a separate movie dataset, but introduces credentials, network and policy dependencies. These are design reasons to understand, not evidence that any integration works yet.

**Kate's explanation remains pending.** Before building, explain in your own words:

1. When you submit a movie title, what do the URL, view, TMDb client, template and browser each do?
2. When you save a movie, what SQLite record is added and how does it connect to your account?
3. Why does a watchlist query filter by the signed-in user, even if other users' links are hidden?
4. What does the user see when TMDb is unavailable, and which locally stored information still works?
5. Why does selecting Comedy and Family require both genres, and how is Surprise Me different from searching the entire TMDb catalog?

### Design status

All eleven required design sections now contain a planning draft. This is not a ready-for-build or completed-application claim: external-source verification, student review, instructor review and remote GitHub display review remain open as listed above. Registration wording is aligned and diagrams are rendered locally. No application features, tests, screenshots, API responses or video evidence have been built or verified by writing this document. Future changes must update proposal/design traceability rather than reuse retired IDs.

### Diagram export verification

All three charts are exported as PNG and SVG from the adjacent editable Graphviz `.dot` sources. The document embeds PNGs rather than raw Mermaid code, so chart display does not depend on a Mermaid plugin. Full-size SVG links support zoom without pixelation. All three rendered PNG exports were visually inspected locally at document-scale widths. The self-contained HTML preview embeds all three SVGs, but a full-browser screenshot check did not complete in this environment; this does not establish API access, application behavior, or remote GitHub rendering.
