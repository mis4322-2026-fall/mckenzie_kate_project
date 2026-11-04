# Project Proposal

## 1. Project identity
- Project name: Movie Finder
- Student(s): Kate McKenzie
- Date: November 3, 2026
- Status: Draft
- Review evidence: Project scope revised by Kate McKenzie; instructor review pending.

## 2. Business problem and users
Movie Finder is for anyone who struggles to find a movie to watch. Looking through many different options can take time, especially when someone has a particular genre in mind or only a limited amount of time. The application will let users enter their preferences and see matching movies with ratings and brief descriptions. This will help them decide what to watch more quickly.

## 3. Main user workflow
1. Sign in with an existing account.
2. Open the protected Movie Finder page.
3. Choose a genre, minimum rating, and maximum runtime in minutes. Each filter is optional.
4. Submit the search to find movies stored in SQLite. Movies must match all selected filters. A movie with a rating equal to the minimum or a runtime equal to the maximum is included.
5. Read the matching movie titles, genres, ratings, runtimes, and brief descriptions. If nothing matches, change the preferences and search again.
6. Sign out when finished.

## 4. Scope
| Requirement ID | User action and observable result | Priority (Must / Later) |
|---|---|---|
| FR-01 | Users can sign in with a valid existing account, access the protected Movie Finder page, and sign out. Invalid sign-in does not grant access, and signed-out visitors cannot access the protected page. | Must |
| FR-02 | Signed-in users can filter movies stored in SQLite by genre, minimum numeric rating, and maximum runtime. Blank filters impose no restriction, all selected filters must match, and rating and runtime boundaries are inclusive. | Must |
| FR-03 | Each matching movie displays its title, genres, numeric rating with its scale, runtime in minutes, and brief description. | Must |
| FR-04 | Users receive helpful messages for invalid filter values or no matching movies and can change their inputs to search again. | Must |
| FR-06 | Users can save favorites or a watchlist. | Later |
| FR-07 | Users can receive personalized recommendations, follow streaming links, or register their own accounts. | Later |

Scope revision: Movie data will come from a CSV dataset stored in SQLite. FR-05 is retired because external-service error handling is no longer part of the project. Existing requirement IDs are retained and are not reassigned.

## 5. Data, inputs, and outputs
| Item | Input / Stored data / Output | Source or destination | Fictional example |
|---|---|---|---|
| Movie dataset | Input | Existing CSV dataset; exact source and usage terms remain Open. Download and import will happen in a later stage. | A row containing title, genres, rating, runtime, and description |
| Movie records | Stored data | CSV records imported into SQLite | Moonlight Picnic; Comedy; 7.8/10; 95 minutes; two neighbors organize an unexpected outdoor dinner |
| Second movie record | Stored data | SQLite; fictional sample for demonstrating filtering | Clockwork Harbor; Mystery; 8.1/10; 120 minutes; a librarian investigates a missing town clock |
| Existing user account | Stored data | Django's built-in authentication and SQLite | Fictional user `demo_viewer`; no password included |
| Genre preference | Input | Movie Finder form | Comedy |
| Minimum rating | Input | Movie Finder form; numeric review score, not an age classification | 7.0 on a proposed 0–10 scale |
| Maximum runtime | Input | Movie Finder form; positive whole minutes | 100 minutes |
| Matching movies | Output | Movie Finder results page | Moonlight Picnic matches Comedy, minimum rating 7.0, and maximum runtime 100 |
| Validation or no-match message | Output | Movie Finder form or results page | No movies match your preferences. Try changing your filters. |

The dataset should contain movie titles, genres, numeric ratings, runtimes, and brief descriptions. Its source URL, rating scale, permitted use, and attribution will be recorded after a dataset is selected. A manageable subset with complete records will be used rather than trying to include every available movie. The examples above are fictional demonstration data, not verified dataset records.

## 6. Acceptance criteria
The following examples use the two fictional movie records in section 5 and a proposed 0–10 rating scale. The final rating scale must match the selected dataset.

| Criterion ID | Requirement ID | Given / When | Expected result |
|---|---|---|---|
| AC-01 | FR-01 | Given an existing demonstration account, when the user signs in with valid credentials | The protected Movie Finder page opens. No passwords are recorded in the proposal. |
| AC-02 | FR-01 | Given the sign-in page, when the user submits invalid credentials | A helpful error appears and access is not granted. |
| AC-03 | FR-01 | Given a signed-out visitor, when the visitor requests the Movie Finder page directly | The server redirects the visitor to sign-in or denies access. |
| AC-04 | FR-01 | Given a signed-in user, when the user signs out through a CSRF-protected POST action and requests the protected page again | The user must sign in again to access the page. |
| AC-05 | FR-02 | Given the two sample movies in SQLite, when the user selects Comedy, minimum rating 7.0, and maximum runtime 100 | Moonlight Picnic appears and Clockwork Harbor does not. |
| AC-06 | FR-02 | Given Moonlight Picnic has rating 7.8 and runtime 95, when the user selects Comedy, minimum rating 7.8, and maximum runtime 95 | Moonlight Picnic appears because both boundaries are inclusive. |
| AC-07 | FR-03 | Given a matching movie, when its result is displayed | Its title, genres, rating and scale, runtime in minutes, and brief description are readable. |
| AC-08 | FR-04 | Given only the two sample movies, when the user selects Comedy and minimum rating 9.0 | No movies appear and a clear message invites the user to change the filters. |
| AC-09 | FR-04 | Given the proposed 0–10 rating scale, when the user submits a rating outside that scale, a negative runtime, or text in a numeric field | A helpful validation error identifies the invalid input and allows correction. |
| AC-13 | FR-02 | Given the two sample movies, when the user selects only Comedy and leaves rating and runtime blank | Moonlight Picnic appears; blank filters do not restrict rating or runtime. |
| AC-14 | FR-02 | Given the two sample movies, when the user leaves all filters blank | Both movies appear. |

AC-10, AC-11, and AC-12 are retired with the previous external-service and pagination scope. The remaining acceptance-criterion IDs are preserved.

## 7. Feasibility and boundaries
This project will use Django, SQLite, and basic Python. Django templates will display the pages, forms will validate search inputs, and Django's ORM will filter the movie records stored in SQLite. Django's built-in session authentication will handle sign-in, sign-out, and protection of the Movie Finder page. A small Movie data model and Django's existing user model should be enough for the first version.

A CSV dataset will be downloaded and imported during development after its suitability and permitted use have been checked. Once the movie records are stored locally, searching will not require an external connection. Using a manageable subset will keep data preparation and displaying results simple. The first version will use a straightforward list of matches without complicated pagination or personalized ranking.

The main risks are missing descriptions or runtimes, inconsistent genre labels, duplicate records, and ratings that use an unexpected scale. Before importing, the selected records will need to be checked for complete required fields, consistent genres, numeric ratings, and runtimes in minutes. The dataset's source and attribution requirements must also be recorded. Recommendations will be limited to the movies included in the local database, so they will not cover every movie or automatically update with new releases.

Favorites, watchlists, personalized recommendations, streaming links, self-registration, password reset, and hosting are outside the first version. Final course delivery will be a video demonstration of the local application. No dataset has been downloaded and no application has been built or tested as part of this revision.

## 8. Assumptions and open questions
| Item | Assumption / Open question | Owner | Resolution |
|---|---|---|---|
| A-01 | Movie Finder is for anyone struggling to choose a movie. | Kate McKenzie | Confirmed. |
| O-01 | Primary audience. | Kate McKenzie | Resolved — anyone struggling to find a movie. |
| O-02 | Movie data source. | Kate McKenzie | Resolved — use an existing CSV dataset and store its records in SQLite. |
| O-03 | Meaning of rating. | Kate McKenzie | Resolved — numeric review score rather than age classification. |
| O-04 | Filters and matching behavior. | Kate McKenzie | Resolved — optional genre, minimum rating, and maximum runtime; all selected filters must match. |
| A-02 | Blank filters impose no restriction, and numeric boundaries are inclusive. | Kate McKenzie | Confirmed. |
| A-03 | Ratings use a 0–10 scale and runtime uses positive whole minutes. | Kate McKenzie | Runtime is measured in minutes; the proposed rating scale must be checked against the chosen dataset. |
| O-05 | Which CSV dataset will be used, and does it contain the required fields with suitable usage terms? | Kate McKenzie | Open — dataset selection is deferred; no dataset search or download is included in this revision. |
| O-06 | Student name. | Kate McKenzie | Resolved — Kate McKenzie. |
| A-04 | The project uses Django authentication, SQLite, and a local video demonstration. | Kate McKenzie | Included to follow the repository's course requirements. |
| O-07 | Instructor review and approval. | Instructor | Pending. |
| O-08 | Handling incomplete movie records. | Kate McKenzie | Proposed approach — use a subset with complete required fields; confirm during data preparation. |
| O-09 | Local dataset or externally requested movie data? | Kate McKenzie | Resolved — local CSV dataset, imported into SQLite. |

## 9. Student explanation
This application will be useful because it helps people find movies to watch without spending a lot of time searching through different options. Users can enter their preferences and receive movie suggestions with ratings and brief descriptions to help them decide.

This project is manageable because I can use an existing movie dataset and basic Python filtering to find matching movies. Django and SQLite will allow me to build a simple web application without needing complicated APIs or advanced features.
