# Project Proposal

## 1. Project identity
- Project name: Movie Finder
- Student(s): Kate McKenzie
- Date: November 3, 2026
- Status: Draft
- Review evidence: Pending — scope and filter choices supplied by Kate McKenzie; API feasibility and instructor review pending.

## 2. Business problem and users
Movie Finder is for anyone struggling to find a movie to watch. Choosing a movie can take too much time when users do not know which titles fit their interests or available time. The application will let users enter their preferences and discover matching movies with a numeric review score and a brief overview. The goal is to make finding a movie easier, faster, and more enjoyable.

The student supplied the idea and selected an external movie API, three filters (genre, minimum numeric review score, and maximum runtime), and a list of matching movies. The app will use filter matching rather than personalized recommendations.

## 3. Main user workflow
1. Sign in with an existing account.
2. Open the protected Movie Finder page.
3. Optionally select genre, minimum numeric review score, and maximum runtime in minutes. Blank filters impose no restriction. All selected filters must match, and score/runtime boundaries are inclusive.
4. Submit the search. The app requests movie data from the selected external API and displays movies matching the selected preferences.
5. Read each movie's title, score, runtime, genre, and brief overview. Browse additional result pages if needed; exact pagination depends on the chosen API.
6. If no movies match, adjust the filters. If the movie service is unavailable, read a clear message and retry later.
7. Sign out when finished.

## 4. Scope
| Requirement ID | User action and observable result | Priority (Must / Later) |
|---|---|---|
| FR-01 | A user can sign in with a valid existing account, access the protected movie search page, and sign out. Invalid sign-in fails, and anonymous visitors cannot access the page. | Must |
| FR-02 | A signed-in user searches with optional genre, minimum numeric review score, and maximum runtime filters and receives movies matching all selected filters from an external movie API. Blank filters impose no restriction, and numeric boundaries are inclusive. Matching results are browsable, subject to the provider's documented result limits. | Must |
| FR-03 | Each movie recommendation displays its title, numeric review score, brief overview, genre, and runtime so the user can decide whether to watch it. | Must |
| FR-04 | Invalid filter values produce helpful errors; an empty search result produces a clear no-match message and allows another search. | Must |
| FR-05 | If the external movie service is unavailable or a request fails, the user receives an understandable message and can retry without losing access to the application. | Must |
| FR-06 | Users can save favorites or a watchlist for later visits. | Later |
| FR-07 | Users can receive recommendations based on viewing history, check streaming availability, or register their own accounts. These are separate possible extensions. | Later |

## 5. Data, inputs, and outputs
| Item | Input / Stored data / Output | Source or destination | Fictional example |
|---|---|---|---|
| Existing user account | Stored data | Django's built-in authentication and SQLite | Fictional account `demo_viewer`; no password recorded |
| Genre preference | Input | Protected search form, mapped to the API's genre identifiers | Comedy |
| Minimum movie score | Input | Search form; provider scale must be confirmed | Proposed minimum 7.0 out of 10 |
| Maximum runtime | Input | Search form, in whole minutes | 100 minutes |
| Movie information | Output | External movie API to search results; provider selection Open | Moonlight Picnic; Comedy; 7.8/10; 95 minutes; two neighbors organize an unexpected outdoor dinner |
| Second sample movie | Output | Controlled fictional API response for acceptance checks | Clockwork Harbor; Mystery; 8.1/10; 120 minutes; a librarian investigates a missing town clock |
| Matching movie list | Output | Protected results page | Comedy, minimum 7.0, maximum 100 returns Moonlight Picnic in the controlled example |
| No-match or validation message | Output | Search form or results page | No movies match your preferences. Try changing your filters. |
| Service error message | Output | Results page | Movie information is temporarily unavailable. Please try again. |
| API credential, if required | Input | Secure runtime configuration used by the server; never source code, browser output, or this document | Not applicable — no credential value is included |

Fictional titles and scores above are demonstration fixtures, not claims about actual API records. No local movie catalog or search-history storage is required for the first version. Persistent movie caching is outside scope unless provider rules make it necessary.

## 6. Acceptance criteria
Optional filters, combined matching, and inclusive boundaries are confirmed by the student. The proposed 0–10 score scale remains subject to provider selection. Controlled fictional API responses allow repeatable checks; live API access must also be verified during development.

| Criterion ID | Requirement ID | Given / When | Expected result |
|---|---|---|---|
| AC-01 | FR-01 | Given an existing fictional account, when the user signs in with valid credentials | The user reaches the protected Movie Finder page. Credentials are supplied securely during demonstration and are not recorded here. |
| AC-02 | FR-01 | Given the sign-in page, when a user submits invalid credentials | Sign-in fails with a helpful error and grants no access to the protected page. |
| AC-03 | FR-01 | Given a signed-out visitor, when the visitor directly requests the protected page | The server redirects the visitor to sign-in or denies access. |
| AC-04 | FR-01 | Given a signed-in user, when the user signs out through a CSRF-protected POST action and requests the protected page again | The session no longer grants access; sign-in is required again. |
| AC-05 | FR-02 | Given the two fictional API records in section 5, when the user searches Comedy, minimum score 7.0, and maximum runtime 100 minutes | Moonlight Picnic appears and Clockwork Harbor does not. All selected filters must match. |
| AC-06 | FR-02 | Given Moonlight Picnic has score 7.8 and runtime 95, when the user searches Comedy, minimum score 7.8, and maximum runtime 95 | Moonlight Picnic appears because filter boundaries are inclusive. |
| AC-07 | FR-03 | Given a matching movie with complete API data, when the recommendation is displayed | Its title, numeric score with scale, genre, runtime in minutes, and brief overview are readable. |
| AC-08 | FR-04 | Given the two sample records, when the user searches Comedy with minimum score 9.0 | No sample movies appear, and a no-match message invites the user to change the filters. |
| AC-09 | FR-04 | Given the proposed 0–10 scale and positive whole-minute runtime, when a user submits a score of 11 or runtime -5 | The form identifies the invalid value and permits correction instead of submitting a valid movie search. |
| AC-10 | FR-05 | Given an API timeout or failure response, when a signed-in user searches | The page displays a helpful service-unavailable message, exposes no credentials or technical error details, and lets the user retry. |
| AC-11 | FR-02 | Given a controlled API response with more matching results than fit on one page, when the user requests the next page | Additional matches are shown while preserving the filters. Provider result limits must be stated once selected. |
| AC-12 | FR-02, FR-03 | Given configured access to the selected API, when a user performs a representative live search | Real movie data is retrieved and displayed with the required fields, and returned movies meet the selected filters. This check has not been run. |
| AC-13 | FR-02 | Given the two fictional API records, when the user selects only Comedy and leaves score and runtime blank | Moonlight Picnic appears; blank filters impose no score or runtime restriction. |
| AC-14 | FR-02 | Given the two fictional API records, when the user leaves all filters blank | Both records are browsable, subject to pagination and provider result limits. |

## 7. Feasibility and boundaries
The proposed application uses Django with server-rendered templates, Django forms for preference validation, Django's built-in session authentication, and SQLite for user accounts. Django's ORM handles local account data; an external API supplies movie information. A local Movie model is not needed unless later design establishes a specific storage need.

The first version uses straightforward filtering. It does not require machine learning, viewing-history analysis, a background job system, a JavaScript framework, or multiple user roles. Self-registration, password reset, watchlists, streaming availability, and deployment are outside the initial scope. Final course delivery is a video demonstration of the local application.

The external API is a student-selected requirement, but its provider, availability, allowed use, credentials, network access, score scale, runtime filtering, pagination, attribution requirements, and missing-field behavior are not yet verified. Selecting a provider with searchable runtime data is particularly important: fetching details for every candidate movie could make searches slow or exceed rate limits. The design stage must establish a practical query strategy and disclose result limits without claiming an exhaustive search that the provider cannot support.

API calls should run on the server, with required credentials supplied through secure configuration. Timeouts and service errors must be handled. Provider-required attribution must appear where required. Missing runtime or score must not cause a movie to be falsely presented as satisfying that filter; precise display rules remain Open.

Authentication, SQLite, and local demonstration follow the repository's course conventions. No application has been built, API selected, credentials requested, or behavior tested during this proposal work. API feasibility is a planning dependency, not an established capability.

## 8. Assumptions and open questions
| Item | Assumption / Open question | Owner | Resolution |
|---|---|---|---|
| A-01 | Intended users are anyone struggling to find a movie. | Student | Confirmed in refinement response. |
| O-01 | Primary audience. | Student | Resolved — anyone struggling to choose a movie. |
| O-02 | Local catalog or external movie API? | Student | Resolved — external movie API selected. |
| O-03 | Meaning of rating. | Student | Resolved — minimum numeric review score selected through the confirmed workflow. |
| O-04 | Filters and recommendation behavior. | Student | Resolved — genre, minimum score, maximum runtime; show matching movies. No personalized ranking requested. |
| A-02 | Users may leave filters blank, and selected filters combine; boundaries are inclusive. | Student | Confirmed by Kate McKenzie in the follow-up response. |
| A-03 | Scores use a 0–10 scale and runtime uses positive whole minutes. | Assistant recommendation | Open — score scale depends on provider; runtime validation proposed. |
| O-05 | Select an API and verify access, runtime filtering, rate limits, result limits, required fields, and terms. | Student and assistant | Open — student explicitly deferred provider selection to the design stage; no API availability promised. |
| O-06 | Student name for the proposal. | Student | Resolved — Kate McKenzie, supplied by the student. |
| A-04 | Sign-in, POST sign-out, protected search, SQLite, and local video delivery follow course conventions. | Repository course skill | Required by the skill; instructor review pending. |
| O-07 | Instructor review and approval. | Instructor | Pending — no review evidence supplied. |
| O-09 | Does “existing movie dataset” in the student explanation mean API data or a local dataset? | Student | Open for design — retain the earlier external API choice until a change is confirmed. |
| O-08 | How should missing score, runtime, or overview be displayed? | Student and assistant | Open — propose labeling unavailable fields and excluding records whose missing fields prevent confirming an active filter. |

## 9. Student explanation
Supplied by Kate McKenzie:

> This application will be useful because it helps people find movies to watch without spending a lot of time searching through different options. Users can enter their preferences and receive movie suggestions with ratings and brief descriptions to help them decide.
>
> This project is manageable because I can use an existing movie dataset and basic Python filtering to find matching movies. Django and SQLite will allow me to build a simple web application without needing complicated APIs or advanced features.

Planning note: Kate's explanation mentions an existing dataset and avoiding complicated APIs, while her earlier scope choice selected an external movie API and her follow-up deferred provider selection to design. The proposal retains the external API choice. During design, clarify whether “dataset” means data returned by that API or a change to a local dataset; document any scope change before implementation.
