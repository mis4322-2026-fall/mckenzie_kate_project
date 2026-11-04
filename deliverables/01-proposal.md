# Project Proposal

## 1. Project identity
- Project name: Movie Finder
- Student(s): Kate McKenzie
- Date: November 3, 2026
- Status: Draft
- Review evidence: Project scope revised by Kate McKenzie; instructor review pending.

## 2. Business problem and users
Movie Finder is for anyone who struggles to find a movie to watch. Looking through many different options can take time, especially when someone has a particular genre in mind or only a limited amount of time. The application will offer two ways to search: enter movie preferences or enter the title of a movie they enjoyed to find other movies with similar genres. Both methods will show matching movies with ratings and brief descriptions. This will help them decide what to watch more quickly.

## 3. Main user workflow
1. Create an account with a username and password, or sign in with an existing account. After creating an account, sign in to continue.
2. Open the protected Movie Finder home page and choose **Find by preferences** or **Find similar movies**.
3. For preferences, choose a genre, minimum rating, and maximum runtime in minutes. Each filter is optional. All selected filters must match, and rating and runtime boundaries are inclusive.
4. For similar movies, enter a movie title from the local catalog. Title matching ignores capitalization and extra spaces at the beginning or end. If more than one movie has that title, choose the intended record from the matches before continuing.
5. The application finds other movies sharing at least one genre with the selected movie and excludes that movie itself. It does not use machine learning, viewing history, or an external API.
6. Read the matching movie titles, genres, ratings, runtimes, and descriptions. If the title is not found or no recommendations match, read the message and try another search. Return to the home page to switch methods.
7. Sign out when finished.

## 4. Scope
| Requirement ID | User action and observable result | Priority (Must / Later) |
|---|---|---|
| FR-01 | Users can sign in with a valid existing account, access the protected Movie Finder home page and both search methods, and sign out. Invalid sign-in does not grant access, and signed-out visitors cannot access these pages or their results. | Must |
| FR-02 | Signed-in users can filter movies stored in SQLite by genre, minimum numeric rating, and maximum runtime. Blank filters impose no restriction, all selected filters must match, and rating and runtime boundaries are inclusive. | Must |
| FR-03 | Both search methods display each matching movie's title, genres, numeric rating with its scale, runtime in minutes, and brief description. | Must |
| FR-04 | Users receive helpful messages for invalid filter values, a blank or unknown movie title, or no matching movies and can change their inputs to search again. | Must |
| FR-06 | Users can save favorites or a watchlist. | Later |
| FR-07 | Users can receive recommendations based on viewing history, follow streaming links, or search for TV shows. | Later |
| FR-08 | New users can create an account with a unique username and a password confirmed twice. Invalid registration shows helpful errors; successful registration allows the user to sign in. | Must |
| FR-09 | After signing in, users see a protected home page with choices for preference search and similar-movie search and can return to it to switch methods. | Must |
| FR-10 | Signed-in users can enter a movie title, select the intended record if the title has multiple matches, and receive other movies sharing at least one of its genres. Each matching movie appears once, and the original record is excluded. | Must |

Scope revision: Movie data will come from a CSV dataset stored in SQLite. FR-05 is retired because external-service error handling is no longer part of the project. Existing requirement IDs are retained and are not reassigned. Account creation is now Must under FR-08 rather than part of the Later features in FR-07. FR-09 and FR-10 cover the home page and genre-based similar-movie search.

## 5. Data, inputs, and outputs
| Item | Input / Stored data / Output | Source or destination | Fictional example |
|---|---|---|---|
| Movie dataset | Input | TMDB 5000 Movie Dataset on Kaggle; planned file: `tmdb_5000_movies.csv`. Download, preparation, and SQLite import are planned for later. Contents and usage terms are not yet verified. | A row containing title, genres, rating, runtime, and description |
| Movie records | Stored data | CSV records imported into SQLite | Moonlight Picnic; Comedy; 7.8/10; 95 minutes; two neighbors organize an unexpected outdoor dinner |
| Second movie record | Stored data | SQLite; fictional sample for demonstrating filtering | Clockwork Harbor; Mystery; 8.1/10; 120 minutes; a librarian investigates a missing town clock |
| User account | Input / Stored data | Registration form, Django's built-in authentication, and SQLite | Fictional user `demo_viewer`; no password included |
| Genre preference | Input | Movie Finder form | Comedy |
| Minimum rating | Input | Movie Finder form; numeric review score, not an age classification | 7.0 on a proposed 0–10 scale |
| Maximum runtime | Input | Movie Finder form; positive whole minutes | 100 minutes |
| Matching movies | Output | Movie Finder results page | Moonlight Picnic matches Comedy, minimum rating 7.0, and maximum runtime 100 |
| Third movie record | Stored data | SQLite; fictional sample for similar-movie checks | Garden of Laughs; Comedy and Family; 7.2/10; 90 minutes; a family prepares a neighborhood talent show |
| Movie title | Input | Similar-movie form; choose a matching record if titles repeat | Moonlight Picnic |
| Similar movies | Output | Similar-movie results page | Garden of Laughs shares Comedy with Moonlight Picnic; Moonlight Picnic itself is excluded |
| Validation or no-match message | Output | Movie Finder form or results page | No movies match your preferences. Try changing your filters. |

The dataset must contain movie titles, genres, numeric ratings, runtimes, and brief descriptions. A manageable subset with complete records will be used rather than trying to include every available movie. The examples above are fictional demonstration data, not verified dataset records.

My planned data source is the [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). I found the dataset and confirmed that its page is accessible in my browser. I plan to use `tmdb_5000_movies.csv`, which is expected to include movie titles, genres, ratings, runtimes, and descriptions.

The expected columns are:

| Project information | Expected CSV column |
|---|---|
| Movie title | `title` |
| Genres | `genres` |
| Numeric rating | `vote_average` |
| Runtime | `runtime` |
| Brief description | `overview` |

I plan to download the CSV later, check and prepare the data, and import the movie records into SQLite for my Django application. Preparation will include checking for missing values and duplicates, making genre values readable, and confirming the rating scale and runtime units. I will use a manageable set of complete records for the first version.

The actual CSV contents, column names, missing values, and usage terms have not yet been verified. Before using the data, I will review the dataset's license and any attribution requirements. Being able to open the Kaggle page does not confirm those details. No dataset has been downloaded or imported.

## 6. Acceptance criteria
The following examples use the fictional movie records in section 5. AC-05, AC-13, and AC-14 use only the original two records (Moonlight Picnic and Clockwork Harbor) and use a proposed 0–10 rating scale. The final rating scale must match the selected dataset.

| Criterion ID | Requirement ID | Given / When | Expected result |
|---|---|---|---|
| AC-01 | FR-01 | Given an existing demonstration account, when the user signs in with valid credentials | The protected Movie Finder home page opens with both search choices. No passwords are recorded in the proposal. |
| AC-02 | FR-01 | Given the sign-in page, when the user submits invalid credentials | A helpful error appears and access is not granted. |
| AC-03 | FR-01 | Given a signed-out visitor, when the visitor directly requests the home page, either search page, or either results page | The server redirects the visitor to sign-in or denies access. |
| AC-04 | FR-01 | Given a signed-in user, when the user signs out through a CSRF-protected POST action and requests the protected page again | The user must sign in again to access the page. |
| AC-05 | FR-02 | Given the two sample movies in SQLite, when the user selects Comedy, minimum rating 7.0, and maximum runtime 100 | Moonlight Picnic appears and Clockwork Harbor does not. |
| AC-06 | FR-02 | Given Moonlight Picnic has rating 7.8 and runtime 95, when the user selects Comedy, minimum rating 7.8, and maximum runtime 95 | Moonlight Picnic appears because both boundaries are inclusive. |
| AC-07 | FR-03 | Given a matching movie, when its result is displayed by either search method | Its title, genres, rating and scale, runtime in minutes, and brief description are readable. |
| AC-08 | FR-04 | Given only the two sample movies, when the user selects Comedy and minimum rating 9.0 | No movies appear and a clear message invites the user to change the filters. |
| AC-09 | FR-04 | Given the proposed 0–10 rating scale, when the user submits a rating outside that scale, a negative runtime, or text in a numeric field | A helpful validation error identifies the invalid input and allows correction. |
| AC-13 | FR-02 | Given the two sample movies, when the user selects only Comedy and leaves rating and runtime blank | Moonlight Picnic appears; blank filters do not restrict rating or runtime. |
| AC-14 | FR-02 | Given the two sample movies, when the user leaves all filters blank | Both movies appear. |
| AC-15 | FR-08 | Given an unused fictional username and a valid password entered identically twice, when a new user submits registration | An account is created, and the user can sign in and reach the home page. No password is included in the proposal. |
| AC-16 | FR-08 | When registration uses an existing username, mismatched passwords, or a password rejected by Django's configured validators | A helpful error appears and no new account is created. |
| AC-17 | FR-09 | Given a signed-in user on the home page, when the user selects either search option | The corresponding form opens, and the user can return home to choose the other method. |
| AC-18 | FR-10 | Given all three sample movies, when the user searches for Moonlight Picnic | Garden of Laughs appears because it shares Comedy; Clockwork Harbor and Moonlight Picnic do not appear. |
| AC-19 | FR-10 | Given two different records share multiple genres, when one is selected as the starting movie | The other record appears only once and the starting record is excluded. |
| AC-20 | FR-04, FR-10 | When a user submits a blank title or a title absent from SQLite | A helpful message requests a title or explains that the movie was not found, and the user can try again. |
| AC-21 | FR-04, FR-10 | Given the three sample movies, when the user searches for Clockwork Harbor | A clear message explains that no other movies share its genres. |
| AC-22 | FR-10 | Given Moonlight Picnic is stored, when the user enters `  moonlight picnic  ` | The same movie is found regardless of capitalization and surrounding spaces. |
| AC-23 | FR-10 | Given two movie records have the same title, when that title is submitted | The user chooses between the matching records before recommendations are generated; only the selected record is excluded. |

AC-10, AC-11, and AC-12 are retired with the previous external-service and pagination scope. The remaining acceptance-criterion IDs are preserved.

## 7. Feasibility and boundaries
This project will use Django, SQLite, and basic Python. Django templates will display the pages, forms will validate search inputs, and Django's ORM will filter the movie records stored in SQLite. Django's built-in user creation form and password validation will support registration. Its session authentication will handle sign-in, CSRF-protected POST sign-out, and server-side protection of the home page, both search methods, and their results. Passwords will be handled by Django rather than custom password storage. A small Movie data model and Django's existing user model should be enough for the first version.

Similar-movie recommendations will use a simple genre comparison: find the chosen record, compare its genre names or identifiers with other stored movies, and return each movie sharing at least one genre, excluding the original record. This uses basic Python and database queries without machine learning or an external API. Genres will need to be stored consistently so comparisons use whole genres rather than partial text matches. Searching by title will use a case-insensitive exact match after trimming surrounding spaces. Duplicate titles will require a simple selection step using distinct record identifiers.

A CSV dataset will be downloaded and imported during development after its suitability and permitted use have been checked. Once the movie records are stored locally, searching will not require an external connection. Using a manageable subset will keep data preparation and displaying results simple. The first version will use a straightforward list of matches without complicated pagination or personalized ranking.

The main risks are missing descriptions or runtimes, inconsistent genre labels, duplicate records or titles, and ratings that use an unexpected scale. Before importing, the selected records will need to be checked for complete required fields, consistent genres, numeric ratings, and runtimes in minutes. The dataset's source and attribution requirements must also be recorded. Recommendations will be limited to the movies included in the local database, so they will not cover every movie or automatically update with new releases.

TV shows, favorites, watchlists, recommendations based on viewing history, streaming links, password reset, and hosting are outside the first version. Final course delivery will be a video demonstration of the local application. No dataset has been downloaded and no application has been built or tested as part of this revision.

## 8. Assumptions and open questions
| Item | Assumption / Open question | Owner | Resolution |
|---|---|---|---|
| A-01 | Movie Finder is for anyone struggling to choose a movie. | Kate McKenzie | Confirmed. |
| O-01 | Primary audience. | Kate McKenzie | Resolved — anyone struggling to find a movie. |
| O-02 | Movie data source. | Kate McKenzie | Resolved — use an existing CSV dataset and store its records in SQLite. |
| O-03 | Meaning of rating. | Kate McKenzie | Resolved — numeric review score rather than age classification. |
| O-04 | Search methods and matching behavior. | Kate McKenzie | Confirmed — optional preference filters and title-based recommendations sharing genres, excluding the original movie. |
| A-02 | Blank filters impose no restriction, and numeric boundaries are inclusive. | Kate McKenzie | Confirmed. |
| A-03 | Ratings use a 0–10 scale and runtime uses positive whole minutes. | Kate McKenzie | Runtime is measured in minutes; the proposed rating scale must be checked against the chosen dataset. |
| O-05 | Planned dataset and remaining checks. | Kate McKenzie | Planned source — TMDB 5000 Movie Dataset on Kaggle, using `tmdb_5000_movies.csv`. The page is accessible in my browser. Open — verify the actual CSV contents, missing values, rating scale, runtime units, usage terms, and attribution before use. |
| O-06 | Student name. | Kate McKenzie | Resolved — Kate McKenzie. |
| A-04 | The project uses Django authentication, SQLite, and a local video demonstration. | Kate McKenzie | Included to follow the repository's course requirements. |
| O-07 | Instructor review and approval. | Instructor | Pending. |
| O-08 | Handling incomplete movie records. | Kate McKenzie | Proposed approach — use a subset with complete required fields; confirm during data preparation. |
| O-09 | Local dataset or externally requested movie data? | Kate McKenzie | Resolved — local CSV dataset, imported into SQLite. |
| A-05 | Account creation and a home page with both search choices. | Kate McKenzie | Required in this revision. |
| A-06 | Similar movies share at least one genre; title lookup ignores capitalization and surrounding spaces, and duplicate titles require choosing a record. | Proposal defaults | Simple matching rules for the first version; no advanced ranking. |

## 9. Student explanation
This application will be useful because it helps people find movies to watch without spending a lot of time searching through different options. Users can enter their preferences and receive movie suggestions with ratings and brief descriptions to help them decide.

This project is manageable because I can use an existing movie dataset and basic Python filtering to find matching movies. Django and SQLite will allow me to build a simple web application without needing complicated APIs or advanced features.
