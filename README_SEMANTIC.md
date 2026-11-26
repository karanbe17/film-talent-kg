# ProduCast — Semantic Web (CSC501 Milestone 5)

ProduCast is the interface and academic project name. This milestone adds an RDF/OWL knowledge graph and a server-rendered, multi-page application without altering the original SQLite database or relational code. The original README and `main.py` are retained for Milestone 4. No React, no CDN dependencies, no movie posters scraped from external sources. The logo and abstract film artwork are local SVG/CSS assets.

## Recommended quickstart: Virtuoso (Windows PowerShell)

Install Docker Desktop and start it. From the repository root, choose a private local password (do not commit it):

```powershell
$env:PRODUCAST_VIRTUOSO_PASSWORD = 'replace-with-your-local-password'
docker compose up -d
docker compose logs --tail=30 virtuoso
python -m pip install -r requirements-semantic.txt
python verify_virtuoso.py
python semantic_main.py --virtuoso
```

Wait for the server to finish initialization before running verification. Conductor: http://127.0.0.1:8890/conductor (user `dba`, password chosen above). Application: http://127.0.0.1:8000. The official OpenLink open-source Docker image is used. On macOS/Linux use `export PRODUCAST_VIRTUOSO_PASSWORD='your-password'` instead. If an existing Virtuoso instance is already running, set `PRODUCAST_VIRTUOSO_URL` and `PRODUCAST_VIRTUOSO_USER` as needed and omit Docker startup. The authenticated `/sparql-auth` endpoint must allow SELECT and UPDATE for the configured user; use Conductor to configure permissions if necessary. Never enable anonymous writes or expose the local app publicly. If changing the password after initializing the Docker volume, change it inside Virtuoso too; the environment setting only initializes new databases.

The application loads the RDF/XML ontology and seed into separate named graphs through SPARQL INSERT DATA if absent. Conductor can also import the RDF/XML files manually. Data graph: `https://github.com/karanbe17/film-talent-kg/graph/data`; ontology graph: the same IRI with `/ontology` appended. The Query Lab SELECTs target the data graph. `python semantic_main.py --virtuoso --queries` runs the remote SELECTs in terminal; `verify_virtuoso.py` checks remote loading, SELECT, INSERT, UPDATE and DELETE in disposable graphs. `--reset` clears and reseeds the application graphs; omit it to preserve edits. `docker compose down` stops the server without deleting its named volume.

## Tested fallback: embedded mode

If Virtuoso is unavailable, `python quickstart_semantic.py` installs dependencies and launches the original RDFLib-backed version. `python semantic_main.py --reset` resets only local sample data; omit reset on later launches. The original relational application remains available via `python main.py` after installing `requirements.txt`. No React or CDN dependencies.

## Architecture and verification status

Browser → FastAPI/Jinja2 → domain services → Virtuoso HTTP SPARQL adapter → persistent named graphs in Virtuoso. RDFLib converts SQLite, parses RDF/XML and stages validation of edits; remote SELECT and SPARQL update requests execute in Virtuoso when `--virtuoso` is selected. The adapter stages the small instance graph locally and sends scoped triple changes; use a single writer, not a concurrent production deployment. The fallback uses atomic RDF/XML files. Five automated tests passed (four local application tests and one simulated SPARQL protocol test); a live Virtuoso server and Protégé reasoner were not available in the development environment. Run `verify_virtuoso.py` and validate the ontology in Protégé before claiming live verification. See OpenLink setup: https://www.openlinksw.com/howto/install/docker/ .

## Data and conversion

Milestone 4 is preserved unchanged. Milestone 5 uses a curated replacement catalogue of selected real films, credits and award wins, stored in `data/raw/film_catalogue.txt` and `data/raw/award_catalogue.txt`. The original SQLite data had incomplete and inaccurate credits. `src/dal/catalogue.py` builds a separate normalized SQLite staging database (`data/preprocessed/catalogue.db`) and converts it into RDF/XML. Run `python semantic_main.py --init-only --reset` to regenerate the seed and local working graph. When upgrading from an earlier version, use `--reset` once; `--virtuoso --reset` also replaces the application server graphs. Export valuable user changes before resetting.

| Relational input | RDF representation |
|---|---|
| Person and Profession | Person individual plus Actor, Director or CameraMan type |
| Studio | Studio resource and selected production company relationship |
| Movie | Movie resource, title, genre, release year |
| MovieDirector / MovieCamera | directedBy / filmedBy edges |
| PerformanceRole | Association resource with belongsTo, filledBy, characterName |
| Award | Award occurrence, recipient, film, category, ceremony year |

35 films, 43 actors, 31 directors, 31 cinematographers, 104 distinct people, 29 production companies, 59 role credits and 82 selected award wins. Every film has a director, selected cast, production company and cinematographer. Each included actor has a film credit. `awardedFor` and `filmedBy` extend the conceptual baseline, with no surrogate ID attributes added to the ERD. Stable staging identifiers become IRIs; names and titles are not asserted globally unique. Unknown budgets, role classifications, billing order and exact dates are omitted. One selected production company per film is recorded, not every producer or studio. Award wins are not exhaustive career totals. Some actors have no wins in this selected sample; this is not a statement about their complete career.

See `data/raw/SOURCES.md` for review links and limitations. The catalogue is manually curated with AI assistance, not an independently verified or complete commercial database. Source metadata is retained in RDF and documentation but hidden from the producer-facing pages.

## Demonstration and verification

1. Open Talent, select Actors, search Leonardo DiCaprio, and inspect his characters, films, awards and repeated collaboration with Martin Scorsese. Select Directors separately. Movies: search Rocky; inspect John G. Avildsen, Sylvester Stallone and Rocky Balboa.
2. Collaborations: search Cillian Murphy, Christopher Nolan or Leonardo DiCaprio; select repeat partnerships only. Browse awards, studios and casting independently. All directories use pagination.
3. Create a test studio, person, movie, casting role and award, edit, reload and delete. Removing a film removes dependent roles and awards; removing a person removes dependent roles and awards. In-use studios cannot be deleted. Minimum participation is not fully enforced during incremental entry.
4. Research tools in the footer opens six prepared SELECT queries; data export downloads RDF/XML. Run `python demo_sparql.py` for isolated INSERT, UPDATE and DELETE. Run `python semantic_main.py --virtuoso --queries` for actual remote queries after successful server setup.
5. `python -m pip install -r requirements-test.txt`, then `python -m unittest discover -s tests -v`. Open `src/dal/models/semantic/producast.owl` in Protégé and run a reasoner. Live Virtuoso and Protégé verification remain team tasks.

## FAIR / citation / license

Repository: https://github.com/karanbe17/film-talent-kg . Keep access available to course instructors/markers. The namespace uses the project repository URI. Reusable RDF/XML, standalone SPARQL, converter, explicit provenance, pinned dependencies, setup and test scripts are included. Original repository license applies (see LICENSE). Cite the course manual (CSC501 Fall 2026 Milestone 5), W3C RDF 1.1 Concepts, OWL 2 Primer, SPARQL 1.1 Query and Update, RDFLib and OpenLink Virtuoso. AI assistance is documented in `docs/AI_USAGE_M5.md`; students must critically review and disclose actual contributions before submission.
