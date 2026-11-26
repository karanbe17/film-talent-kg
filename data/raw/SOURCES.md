# Catalogue provenance and scope

These AI-assisted, manually curated data files select real films, credited performers, directors, cinematographers, one production company per film and award wins. They are not a complete filmography, nominations database or verified commercial catalogue. Some people are deceased; no casting availability is asserted.

Reference and review links:
- Official Academy Awards ceremony archive: https://www.oscars.org/oscars/ceremonies (individual ceremony-year URLs stored in award records; examples https://www.oscars.org/oscars/ceremonies/2024 and https://www.oscars.org/oscars/ceremonies/2016).
- Official Golden Globes winners and nominees: https://goldenglobes.com/winners-nominees/ ; film pages https://goldenglobes.com/film/oppenheimer/ and https://goldenglobes.com/film/the-revenant/ .
- IMDb film-title search URLs generated from title and year, for checking credited cast, director, cinematographer and production-company credits. Example: https://www.imdb.com/find/?q=Rocky%201976 . These are review links, not proof that each full credit page was independently retrieved.

Selected award examples were checked against award archives; other rows require team factual review. Standard award category names are shortened. Ceremony year can differ from release year. Names use familiar professional credits rather than unverified legal names. Missing role classifications, exact dates, budget and billing order are omitted. No external posters or photos are copied. Provenance is stored in RDF, not displayed to producers.

Film format: title | release year | genre | selected company | directors (semicolon separated) | cinematographers | actor~character pairs (semicolon separated).
Award format: recipient | film | ceremony year | award organization | category. Each award resolves to a person and film; relational foreign keys are checked. Historical Milestone 4 data remain untouched.
