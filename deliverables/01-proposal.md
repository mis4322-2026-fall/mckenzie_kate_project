# Project Proposal

## 1. Project identity
- Project name: Movie Finder
- Student: Kate McKenzie
- Original proposal date: November 3, 2026
- Scope revision date: November 11, 2026
- Status: Draft — planning only; no features are claimed as built or tested.
- Review evidence: Kate supplied the revised scope. Instructor feedback has not been supplied; instructor review remains pending.

## 2. Business problem and users
Movie Finder is a full-stack Django web application for people who have trouble deciding what movie to watch. Searching across many options can take time. The application will bring popular movies, title search, genre browsing, related recommendations, and random discovery into one place. Users can read a movie's information and save interesting titles to a private watchlist for later.

The backend will use Python and Django. Django templates, HTML, and CSS will provide a simple interface. Django's built-in authentication will manage accounts, while SQLite will store accounts and personal watchlists. TMDb will be the planned source for movie information, posters, genres, numeric ratings, popularity, and movie-based recommendations. Recommendations will relate to a selected movie, not a user's viewing history.

### November 11 scope changes
The original purpose remains helping users choose a movie. The approach has changed to keep discovery in one external data source and local storage focused on accounts and saved movies.

| Area | Earlier plan | Revised plan |
|---|---|---|
| Movie source | Download TMDB 5000 CSV and filter imported SQLite movie records | Request movie information from TMDb; no CSV import or local discovery catalog |
| Genre browsing | One genre with minimum rating and maximum runtime; release-year filtering later appeared in the design | One or multiple genres; every selected genre must match. No rating, runtime, or release-year filter |
| Title search and recommendations | Local title matching and shared-genre recommendations; possible storyline keyword comparison | TMDb title search and an available movie-based recommendations feature; no custom similarity algorithm |
| Dashboard | Links to discovery methods | Popular movies, title search, genre browsing, Surprise Me, and watchlist navigation |
| Accounts and watchlists | Authentication already required; watchlist previously Later in the proposal and planned in the design | Registration and private persistent watchlists are Must requirements |
| Random discovery | Random movie from SQLite | Random selection from a bounded set of movies returned by TMDb, not the entire TMDb catalog |
| Details and media | Runtime required; optional trailers and streaming providers | Separate details page with poster, title, genres, rating, and description; runtime no longer required; trailers and streaming removed |

Title search, registration, and Surprise Me were already added in earlier revisions and are retained. The ledger in section 4 records ID changes. This revision supersedes earlier design ideas about CSV import, local recommendation ranking, trailer hover, streaming availability, and release-year filtering.

## 3. Main user workflow
1. Open the public welcome page. New users can create an account; returning users can log in.
2. Register with a unique username and a confirmed password. Successful registration automatically authenticates the user and redirects to the protected dashboard; no separate login is required. Invalid registration or login displays helpful errors.
3. Successful login opens the protected dashboard, showing popular movies, a search bar, genre browsing, a Surprise Me button, and watchlist navigation.
4. Enter a title to receive matching movies from TMDb, or choose one or more genres to browse movies matching all selected genres.
5. Open a movie's details page to view its poster, title, genres, numeric rating, and description. Choose related recommendations supplied by TMDb when available.
6. Alternatively, click Surprise Me to receive one random movie from the available candidate set. Click Try Again for another selection request.
7. Save a movie to the personal watchlist, view saved titles, or remove a saved movie. Only the signed-in user's entries are visible or changeable through application pages.
8. If information cannot be retrieved or nothing matches, read the explanatory message and try again or return to the dashboard. A missing poster or description must not break the page.
9. Log out through a secure POST action. Protected pages require login again, while the welcome page remains public.

## 4. Scope
| Requirement ID | User action and observable result | Priority (Must / Later) |
|---|---|---|
| FR-01 | Returning users can sign in and log out. The dashboard, searches, recommendations, random discovery, details, and watchlist require server-side authentication; invalid login grants no access. | Must |
| FR-03 | Clicking a movie opens a separate details page showing its title, genres, numeric rating with its scale, description, and poster when supplied. Missing fields have honest unavailable messages or a poster placeholder. | Must |
| FR-04 | Users receive understandable messages for invalid inputs, empty searches/results, missing movies, unavailable information, and TMDb failures, with a way to retry or navigate back. | Must |
| FR-06 | Signed-in users can save movies, view their private watchlist, and remove their own saved entries. Saved entries persist in SQLite, and duplicate saves do not create duplicate entries. | Must |
| FR-07 | TV-show discovery and additional interface polish may be considered after the required movie application is complete. | Later |
| FR-08 | New users can register with a unique username and a password entered identically twice. Invalid registration shows helpful errors; successful registration automatically authenticates the user through Django and redirects to the protected dashboard. | Must |
| FR-09 | Successful login opens a dashboard displaying TMDb popular movies, a title-search bar, genre browsing, Surprise Me, and watchlist navigation. Users can return to the dashboard from application pages. | Must |
| FR-10 | Users can search TMDb by title, choose the intended movie from matches, and request related movies through an available TMDb movie-based recommendation feature. Recommendations exclude the selected movie and duplicate IDs. | Must |
| FR-11 | Users can click Surprise Me to receive one randomly selected TMDb candidate movie and click Try Again to request another selection. Empty candidate sets and failures display a helpful message. | Must |
| FR-12 | Dashboard/results/detail pages display TMDb posters when supplied, with meaningful alternative text and a local placeholder when an image is missing or cannot load. | Must |
| FR-16 | Users can select one or multiple valid TMDb genres. Browse results must include every selected genre; empty selection prompts the user to select a genre. | Must |
| FR-17 | Visitors can open a public welcome page with account-creation and login links without gaining access to protected movie-discovery pages. | Must |

### Requirement ID ledger
- **Retained and updated:** FR-01, FR-03, FR-04, FR-08, FR-09, FR-10, and FR-11 keep their original user goals. FR-10 replaces local shared-genre logic with TMDb recommendations. FR-11 replaces local random selection with API candidate selection. FR-03 drops runtime and adds a separate details page.
- **Priority changes:** FR-06 promotes the watchlist from Later to Must. FR-12 promotes poster display from optional to Must, with missing-image handling.
- **Replaced:** FR-02 is retired because its local genre/rating/runtime filtering behavior is removed. New FR-16 covers multi-genre API browsing instead of silently reassigning FR-02.
- **New:** FR-17 makes the public welcome page explicit.
- **Retired earlier:** FR-05 stays retired. Its ID is not revived; TMDb failures now fall under FR-04.
- **Retired in this revision:** FR-13 (trailers/hover previews), FR-14 (streaming availability), and FR-15 (custom storyline similarity). These are excluded, not conditional requirements.
- **Future boundary:** FR-07 is narrowed to TV shows and interface polish. Personalized recommendations, personal ratings, watched status, trailers, and streaming availability are not part of this project scope.

## 5. Data, inputs, and outputs
| Item | Input / Stored data / Output | Source or destination | Fictional example |
|---|---|---|---|
| Account | Input / Stored data | Registration form; Django user records and password hashes in SQLite | Fictional username `demo_viewer`; no password recorded |
| Movie title | Input | Django search form to server-side TMDb title search | Moonlight Picnic |
| Genres | Input | Genre choices from TMDb, validated by Django before an all-genres browse request | Comedy and Family |
| Movie information | Output | TMDb response to dashboard, results, and details templates | Fictional movie A: Moonlight Picnic; Comedy; 7.8/10; two neighbors arrange an outdoor dinner |
| Second movie | Output | Controlled fictional response for demonstrating genre browsing | Fictional movie B: Garden of Laughs; Comedy and Family; 7.2/10; a family prepares a talent show |
| Third movie | Output | Controlled fictional response for demonstrating exclusion by genre | Fictional movie C: Clockwork Harbor; Mystery; 8.1/10; a librarian investigates a missing clock |
| Popularity and popular movies | Output | TMDb popular-movie results to dashboard | Controlled response returns movies A and B; popularity is separate from numeric rating |
| Movie-based recommendations | Output | TMDb recommendation response for a selected movie | Controlled response for A contains B; this does not claim TMDb will return that relationship live |
| Poster | Output | TMDb-supplied image reference to browser, following documented image configuration | Generic local placeholder if no poster is supplied |
| Saved movie reference | Stored data | SQLite WatchlistEntry linked to Django User; planned minimum fields: user, TMDb movie ID, title snapshot, saved timestamp | `demo_viewer` saves fictional movie B |
| Watchlist | Output | Current user's SQLite entries; details use TMDb when available | Saved title remains visible during an API outage; current details may be unavailable |
| Error or empty-result message | Output | Django form or results page | No movies matched your search. Try another title. |

The planned source is the [TMDb developer API](https://developer.themoviedb.org/docs/getting-started). Relevant operations to verify include popular movies, title search, genre lists, discover filtering, movie details, recommendations, and image configuration. Documentation starting points include [Discover Movies](https://developer.themoviedb.org/reference/discover-movie) and [Movie Recommendations](https://developer.themoviedb.org/reference/movie-recommendations). These links identify intended research sources; no live requests or terms verification are claimed in this revision.

The CSV dataset is no longer a dependency. SQLite is not a replacement movie search engine: it stores authentication data and each user's saved references, with only a minimal title snapshot for a readable watchlist during outages. TMDb IDs, not titles, identify movies. Fictional examples above are planned test responses, not actual TMDb movie records or verified API outputs.

## 6. Acceptance criteria
These are planned checks, not execution results. Controlled fictional API responses make behavior repeatable; a separate live integration check will confirm real access. Every criterion below is required unless its underlying requirement is explicitly Later.

| Criterion ID | Requirement ID | Given / When | Expected result |
|---|---|---|---|
| AC-01 | FR-01, FR-09 | Given a valid demonstration account, when the user signs in | The protected dashboard opens with popular movies and all discovery/watchlist navigation. |
| AC-02 | FR-01 | When invalid login credentials are submitted | A helpful error appears and no authenticated access is granted. |
| AC-03 | FR-01 | Given a signed-out visitor, when any protected discovery, detail, or watchlist URL is requested directly | The server redirects to login or denies access; no private entries are exposed. |
| AC-04 | FR-01 | Given a signed-in user, when the user submits CSRF-protected POST logout and revisits a protected page | The session no longer grants access and login is required. |
| AC-07 | FR-03 | Given fictional movie B in a details response, when its card is selected from search, browse, random discovery, or watchlist | A separate details page displays B's title, genres, rating with scale, description, and poster or placeholder. Runtime is not required. |
| AC-08 | FR-04 | Given an empty TMDb search or browse response, when results are displayed | A clear no-results message appears with a way to change the search or return to the dashboard. |
| AC-15 | FR-08 | Given an unused username and an acceptable password confirmed twice, when registration is submitted | One account is created, the user is automatically authenticated and redirected to the protected dashboard, and no credentials are saved in documentation. |
| AC-16 | FR-08 | When registration uses an existing username, mismatched passwords, or a password rejected by Django validators | Clear errors appear and no new account is created. |
| AC-17 | FR-09 | Given a signed-in user and a controlled popular-movie response containing A and B, when the dashboard opens | A and B are displayed; search, genre browsing, Surprise Me, and My Watchlist are reachable and have a return-home path. |
| AC-19 | FR-10 | Given a recommendation response containing selected movie A and duplicate copies of B, when recommendations are displayed | B appears once and A is excluded. |
| AC-20 | FR-04, FR-10 | When the user submits a blank title or searches an unknown title with an empty response | Blank input prompts for a title; an unknown title produces a no-results message. |
| AC-21 | FR-04, FR-10 | Given a selected movie with an empty recommendation response, when related movies are requested | Its details remain usable and a no-recommendations message appears. |
| AC-23 | FR-10 | Given two TMDb matches with the same title but different IDs, when the user selects one | Details and recommendations use the selected TMDb ID, not an arbitrary title match. |
| AC-24 | FR-11, FR-03 | Given a controlled candidate response containing A, B, and C, when Surprise Me is clicked | Exactly one candidate is selected and its details are shown; no global-catalog randomness is claimed. |
| AC-25 | FR-11 | Given one random result, when Try Again is clicked | Another selection is requested and one valid candidate is displayed. Immediate repeats are allowed to keep the rule simple. |
| AC-26 | FR-11, FR-04 | Given an empty candidate response, when Surprise Me is clicked | A helpful no-movies-available message appears with retry and dashboard navigation. |
| AC-27 | FR-01, FR-11 | Given a signed-out visitor, when the random-selection URL is requested directly | Login is required before a result can be viewed. |
| AC-28 | FR-12 | Given one movie with a poster and another without one, or an image that fails to load | A supplied poster is displayed where available; otherwise a placeholder and meaningful alternative text keep the page usable. |
| AC-33 | FR-16 | Given fictional responses for Comedy browsing containing A and B, when Comedy is selected | A and B appear without a rating or runtime threshold. |
| AC-34 | FR-16 | Given Comedy and Family are selected and fictional movies A, B, and C, when genre browsing runs | Only B qualifies because it includes both genres; A and C do not. The request uses TMDb's documented all-genres behavior, to be verified during integration. |
| AC-35 | FR-16, FR-04 | When no genre or an invalid genre identifier is submitted | A helpful validation message appears; an invalid browse request is not sent. |
| AC-36 | FR-10 | Given title search returns A and B and the recommendation response for A contains B, when the user selects A and requests related movies | Both search matches are selectable and B is shown as an API-supplied recommendation, without custom storyline or history ranking. |
| AC-37 | FR-06 | Given user One saves B twice, when the watchlist is reopened or the application restarts | Exactly one saved entry for B remains in user One's SQLite watchlist. |
| AC-38 | FR-06, FR-01 | Given user One has saved B and user Two signs in, when user Two views their watchlist or attempts to remove One's entry by ID | One's entry is not shown or changed; an ownership check denies the attempted mutation. |
| AC-39 | FR-06 | Given user One has saved B, when One submits its CSRF-protected POST removal | B is removed from One's watchlist; other users' entries remain unchanged. A GET request cannot save or remove entries. |
| AC-40 | FR-04 | Given a controlled TMDb timeout, authorization error, or malformed response, when a movie feature is requested | A helpful unavailable message appears without exposing credentials or a traceback; retry/navigation remain available. Existing saved titles still appear in the watchlist. |
| AC-41 | FR-03, FR-04 | Given a missing movie ID or missing description/rating in a details response | The page shows an appropriate movie/field-unavailable message instead of invented values or an application error. |
| AC-42 | FR-17 | Given a signed-out visitor, when the root welcome page is opened | The welcome page shows registration/login links; discovery still requires login. |
| AC-43 | FR-09, FR-10, FR-16 | Given securely configured TMDb access, when a representative live popular, search, detail, recommendation, and all-genres browse request is demonstrated | Real responses render correctly or honestly report empty results; the integration and attribution checks are recorded. This is planned, not yet run. |

### Acceptance-criterion history
Existing IDs are retained where their purpose remains: AC-01–AC-04, AC-07–AC-08, AC-15–AC-17, AC-19–AC-21, AC-23–AC-28. Their wording now reflects API responses and the revised page structure.

AC-05, AC-06, AC-09, AC-13, and AC-14 are retired with the old local rating/runtime filtering rules. AC-18 and AC-22 are retired because local shared-genre and exact-title matching are replaced by TMDb behavior. AC-29–AC-32 are retired with trailers, streaming, and custom storyline ranking. AC-10–AC-12 remain retired from earlier revisions. New checks start at AC-33; retired IDs are not reused.

## 7. Feasibility and boundaries
Django provides URL routing, views, forms, templates, ORM access, and built-in user/session authentication. SQLite is sufficient for a small course application with accounts and private watchlists. A minimal WatchlistEntry can reference a user and a TMDb movie ID with a unique pair, a title snapshot, and a saved timestamp. Movie ownership is not required; ownership applies to saved entries. No separate local movie catalog, CSV import, custom recommendation engine, or frontend framework is needed.

Python code will make TMDb requests from the server using timeouts and validated inputs. API authentication material must stay in secure local environment configuration, not templates, browser scripts, Git, or documents. Proposed configuration names are `TMDB_READ_ACCESS_TOKEN` and `DJANGO_SECRET_KEY`; these are names only, not values. `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` describe local runtime configuration if used. Exact setup will be documented during implementation, without committing credentials.

TMDb access, account/credential setup, endpoint behavior, all-genres filtering semantics, permitted use, attribution, costs, image configuration, and applicable request limits need confirmation before the API-dependent build. Do not assume unrestricted or free access. A small server-side integration helper will centralize requests and readable error handling. The application will display required attribution once the current terms are checked. Controlled fictional responses support tests without calling TMDb; they do not replace a successful live integration demonstration.

Surprise Me will choose randomly from a bounded candidate response, initially a valid page of popular movies. This is intentionally simpler than sampling every movie on TMDb. Try Again requests a fresh selection, but repeats are allowed. TMDb numeric ratings are distinct from popularity and do not represent user-entered ratings. Movie-based recommendations use TMDb's available results and may be absent; no custom genre/storyline scoring or claims about TMDb's internal algorithm are made. Movie data can change, so fixed live titles or recommendation order will not be promised.

Main risks are unavailable credentials or networking, service interruptions, empty or changing responses, missing posters/descriptions, and unauthorized watchlist access. Timeouts, validation, clear messages, placeholders, unique saved entries, authentication, and owner-filtered database operations address these risks. SQLite saves persist independently of the API, but current movie details and discovery require connectivity. A title snapshot keeps saved entries readable during an outage; it does not guarantee offline discovery.

Excluded from this project: rating/runtime/year filters, movie-runtime display as a requirement, CSV data import, trailers and hover previews, streaming availability, personal ratings, watched status, personalized recommendations, and custom storyline similarity. Password reset, email verification, TV shows, and hosting are also outside the initial scope. Delivery is a local video demonstration by December 7. The first build increment remains the Django/SQLite authentication foundation with protected access and screenshot evidence for the November 18 initial-build deadline. No implementation, screenshot, test, or API success is claimed here.

## 8. Assumptions and open questions
| Item | Assumption / Open question | Owner | Resolution |
|---|---|---|---|
| A-01 | Intended users need help choosing movies. | Kate McKenzie | Retained project purpose. |
| O-01 | Primary audience. | Kate McKenzie | Resolved — anyone struggling to find a movie. |
| O-02 | Main movie source. | Kate McKenzie | Changed November 11 — TMDb API replaces the CSV catalog. |
| O-03 | Meaning of rating. | Kate McKenzie | Numeric TMDb movie score, not view count or a personal rating. Confirm displayed scale from current documentation. |
| O-04 | Browse matching behavior. | Kate McKenzie | Confirmed — every selected genre must match; rating/runtime/year filters are excluded. |
| A-02 | Blank filters impose no restriction. | Kate McKenzie | Superseded — genre browsing now requires at least one genre; old numeric filter boundaries do not apply. |
| A-03 | Runtime and rating scale assumptions. | Kate McKenzie | Runtime requirement retired. Confirm numeric rating scale before display. |
| O-05 | External source verification. | Kate McKenzie | Open — confirm credentials/access, endpoint semantics, terms, costs, attribution, image use, and request limits. No API connection has been made. |
| O-06 | Student identity. | Kate McKenzie | Confirmed — Kate McKenzie. |
| A-04 | Course stack and delivery. | Kate McKenzie | Django, SQLite, built-in authentication, and local video demonstration retained. |
| O-07 | Instructor review. | Instructor | Pending; no feedback or approval evidence supplied. |
| O-08 | Missing movie information. | Kate McKenzie | Show placeholders or field-unavailable messages; do not invent values. |
| O-09 | Role of SQLite. | Kate McKenzie | Accounts, sessions, and private saved entries; no local discovery catalog. |
| A-05 | Public welcome and private dashboard. | Kate McKenzie | Required; dashboard has popular movies and four navigation choices including watchlist. |
| A-06 | Recommendation logic. | Kate McKenzie | Local similarity superseded — use TMDb movie-based recommendations, excluding selected/duplicate IDs, without user-history personalization. |
| A-07 | Surprise Me candidate set. | Proposed implementation choice | A bounded popular-movie response; immediate repeats allowed. This defines manageable random selection rather than catalog-wide sampling. |

## 9. Student explanation
My original goal is to help people find something to watch without spending too much time searching. The revised plan keeps that goal and adds a private watchlist so users can keep track of movies they want to see.

I plan to use Django for the pages, forms, and login, SQLite for accounts and watchlists, and TMDb for current movie information. This avoids preparing a separate movie dataset or building my own recommendation algorithm. The tradeoff is that discovery depends on an outside service. I will need to understand the API requests, error handling, and how watchlist entries stay private.

This explanation is a draft for Kate to review in her own words. It is not evidence of student understanding, implementation, testing, or instructor approval.
