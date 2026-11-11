# System Design

## 1. Design baseline
- Project: Movie Finder — Kate McKenzie
- Proposal path: [01-proposal.md](01-proposal.md)
- Date: November 11, 2026
- Status: Draft — design is being completed one section at a time; not ready for build.
- Instructor feedback: None supplied yet; instructor review remains pending.
- Scope changes and unresolved blockers: The updated plan below adds a random picker and considers optional media enhancements. The proposal workflow, requirements, and acceptance criteria now include all three discovery methods. The remaining design sections are pending review. Existing requirement and acceptance-criterion IDs will be preserved; FR-05 and AC-10 through AC-12 remain retired.

### Required application

Movie Finder will use Django, SQLite, Python, HTML, and CSS, with minimal JavaScript where needed. Users can register, sign in, and sign out securely. The home page and discovery pages require server-side authentication.

After sign-in, the home page will offer:

1. **Search for a Movie:** Find a known title in SQLite and recommend other movies sharing at least one genre. Exclude the original movie and duplicate results.
2. **Discover by Genre and Preferences:** Browse using genre, minimum numeric rating, and maximum runtime. Preserve the existing optional filters, combined matching, and inclusive numeric boundaries unless a change is approved.
3. **Surprise Me!:** Randomly choose one eligible movie from SQLite, offer “Surprise Me Again,” and show a helpful message when no eligible records exist. This is Must requirement FR-11, with AC-24–AC-27 covering selection, repeat requests, empty data, and authentication. The eligibility rule and whether immediate repeats are allowed will be defined in the business-rules section.

All three methods display title, genres, numeric rating, runtime, and description/storyline from the local database (FR-03, AC-07). FR-09 and AC-17 cover the three home-page choices. Optional posters, trailers, US availability, and storyline comparison are tracked separately as FR-12–FR-15 with conditional checks AC-28–AC-32; these are not initial-build requirements. Numeric rating means a review score, not a view count.

### Main data source

The planned source is the [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), using `tmdb_5000_movies.csv`. Download, preparation, and import into SQLite will happen later. Actual columns, missing values, rating scale, runtime units, permitted use, and attribution remain unverified. No additional dataset is planned.

If the CSV contains a verified TMDB movie ID, that ID could link a local movie to optional TMDB information. A matching ID is not assumed to be present or valid; title matching alone will not establish a reliable match.

### Optional enhancements — not approved for implementation

- **Storyline comparison:** Evaluate simple keyword overlap using the existing descriptions. It needs no AI service, but common words and vague descriptions can produce weak matches. Do not add storyline similarity to ranking without approval. The requested baseline ranking is most shared genres first, then highest numeric rating; the earlier saved documents did not define an ordering, so this rule still needs explicit confirmation in the business-rules step.
- **Posters, trailers, and where-to-watch:** Consider one TMDB API integration instead of additional datasets. Investigate documented capabilities, authentication/key requirements, costs, restrictions, attribution, matching IDs, and US availability coverage. No API call or access test is authorized at this stage. These capabilities and terms have not been verified.
- **Optional hover preview:** After 7 continuous seconds over a poster, transition to a muted trailer if supported. On cursor exit, cancel the timer or stop playback and restore the poster. Evaluate external video hosting, embedding permissions, browser autoplay limits, and mobile/keyboard access. Muted autoplay is not guaranteed. A “Watch Trailer” button is the fallback if hover playback is impractical, with a non-hover route for accessibility. Neither trailer links nor poster links are assumed to be in the CSV.
- **US streaming information:** Display providers only when reliable, region-specific information can be obtained under suitable terms. Do not infer Netflix, Hulu, Disney+, or Prime Video availability. Show “Streaming availability unavailable” when reliable information cannot be retrieved. Provider availability may change; freshness, attribution, and any required provider link must be addressed before approval.

Core searches and results must still work if optional media information is absent or an integration is unavailable. Optional enhancements come after the required application and must fit the course timeline. TV shows, favorites, watchlists, and viewing-history personalization remain future work.

### Review limits

This is a planning update only. No dataset has been downloaded, no API has been connected, and no application code has been written. Integration feasibility will be evaluated from documentation in its own design step; no access, license, cost, or provider coverage is claimed as verified. Before advancing, review this scope baseline. Sections 2–11 remain pending.

## 2. System context
Pending — Include a Mermaid flowchart showing users, Django, SQLite, and any external services.

## 3. Data model
Pending — Include a Mermaid erDiagram and this field dictionary.

| Entity | Field | Django field type | Required / Default | Validation | Relationship / Deletion rule |
|---|---|---|---|---|---|

## 4. Pages and actions
| Requirement ID | Page / URL | User action / HTTP method | Input and validation | Result / Template |
|---|---|---|---|---|

## 5. Main user flow
Pending — Include a Mermaid flowchart with success, invalid-input, and empty-data paths.

## 6. Access and login
| Role | Allowed actions | Ownership / Access restriction |
|---|---|---|

Pending — Basic login is required. Describe Django session authentication, sign-in, POST sign-out, and a protected application page. Distinguish staff admin from application pages; admin login alone does not fulfill the initial build. Specify how demonstration users are created without recording credentials.

## 7. Integrations and configuration
| Dependency / API | Purpose | Official documentation | Environment variable names | Failure / Sample-data fallback |
|---|---|---|---|---|

## 8. Outputs and business rules
| Requirement ID | Output / Rule | Calculation or format | Example |
|---|---|---|---|

## 9. Build increments
| Increment ID | Demonstrable outcome | Requirement IDs | Data / Pages needed | Acceptance criterion IDs |
|---|---|---|---|---|

Pending — Make the first increment the runnable base Django/SQLite project with authentication and a protected application page. Map it to authentication requirement/criterion IDs and initial-build screenshot evidence. Defer business workflows to later increments. Preserve existing IDs when revising a design.

## 10. Verification and delivery plan
| Criterion ID | Sample input / Setup | Action | Expected result | Verification method |
|---|---|---|---|---|

Pending — Plan a video demonstration of the local SQLite app. Map acceptance criteria to demonstration steps, including saved data, useful outputs, authentication, and an error case. Plan initial-build screenshots of sign-in, the authenticated protected page, and the signed-out access restriction. The final video must connect proposal requirements to working behavior and highlight the design choices behind it.

## 11. Decisions, risks, and student explanation
Pending — Record assumptions, open decisions, and risks. Leave a prompt for the student to explain the request → URL → view → ORM → template → response path in their own words.
