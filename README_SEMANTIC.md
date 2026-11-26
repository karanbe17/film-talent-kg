# ProduCast — Semantic Web technical guide

[Back to project overview](README.md) · [ACM report (PDF)](docs/5_Semantic_Karan_Moksh.pdf) · [LaTeX source](docs/5_Semantic_Karan_Moksh.tex)

This guide describes how to reproduce the Milestone 5 semantic implementation with OpenLink Virtuoso or the embedded RDFLib fallback. The earlier relational application is preserved separately.

## 1. Environment and installation

Use Python 3.11 (tested), Git and a browser. For Virtuoso, install and start Docker with Compose. All commands below run from the repository root. On macOS/Linux, substitute `python3` for `python` if needed.

### Automated setup

```bash
python quickstart_semantic.py
```

This creates `.venv`, installs dependencies and launches the RDFLib application on http://127.0.0.1:8000. Use `--port 8001` to choose another application port.

### Manual setup

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements-semantic.txt
```

## 2. Virtuoso setup

Set a private password in the terminal used for Docker and Python. The placeholder below must be replaced with your own value.

Windows PowerShell:

```powershell
$env:PRODUCAST_VIRTUOSO_PASSWORD = 'replace-with-your-local-password'
```

macOS/Linux:

```bash
export PRODUCAST_VIRTUOSO_PASSWORD='replace-with-your-local-password'
```

Start the database:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=30 virtuoso
```

A running container does not necessarily mean the HTTP server is ready. Check the logs and confirm that Conductor opens before verification.

| Endpoint | Purpose |
| --- | --- |
| http://127.0.0.1:8890/conductor | Administration (`dba` and configured password) |
| http://127.0.0.1:8890/sparql | Public query interface, subject to permissions |
| http://127.0.0.1:8890/sparql-auth | Authenticated application SPARQL endpoint |
| http://127.0.0.1:8000 | ProduCast web application |

After manual installation, run:

```bash
python verify_virtuoso.py
python semantic_main.py --virtuoso
```

Alternatively, `python quickstart_semantic.py --virtuoso` handles Python installation and application launch (Docker must already be running).

The adapter uses HTTP Digest authentication and the official OpenLink open-source Docker image. It loads missing named graphs automatically. For an existing server, configure `PRODUCAST_VIRTUOSO_URL` and `PRODUCAST_VIRTUOSO_USER` as needed, alongside the password. The configured user must have SELECT and UPDATE permissions. Do not enable anonymous writes or expose this development application publicly.

The Docker password setting initializes a new database volume; changing the environment variable does not change an existing database account password. Stop Virtuoso with `docker compose down`, which preserves its named volume.

## 3. Data model and conversion

The ontology is stored in `src/dal/models/semantic/producast.owl`; the initial RDF/XML instance graph is `src/dal/models/semantic/seed.rdf`.

The converter in `src/dal/catalogue.py` reads `data/raw/film_catalogue.txt` and `data/raw/award_catalogue.txt`, builds a normalized SQLite staging database (`data/preprocessed/catalogue.db`) and produces the RDF instance graph.

| Relational input | Semantic representation |
| --- | --- |
| Person and Profession | Person resource with Actor, Director or CameraMan types |
| Studio | Studio resource and production company relationship |
| Movie | Movie resource, title, genre and release year |
| MovieDirector / MovieCamera | `directedBy` / `filmedBy` relationships |
| PerformanceRole | Association resource linked by `belongsTo`, `filledBy` and `characterName` |
| Award | Award occurrence linked to recipient, film, category and year |

Stable staging identifiers become IRIs. Names and titles are not assumed globally unique. The conceptual ER model does not contain artificial surrogate ID attributes. See [ER extensions](docs/er/semantic_extensions.md) and [source notes](data/raw/SOURCES.md).

The sample contains 35 films, 104 distinct people, 29 companies, 59 acting credits and 82 selected award wins. It is a curated sample, not a complete or independently verified commercial database. Unknown budgets, billing order, role classifications and exact dates are omitted where unavailable. One selected production company is recorded per film.

### Named graphs

| Graph | IRI |
| --- | --- |
| Instance data | `https://github.com/karanbe17/film-talent-kg/graph/data` |
| Ontology | `https://github.com/karanbe17/film-talent-kg/graph/data/ontology` |

The application stages RDF/XML conversion and scoped change validation with RDFLib; Virtuoso mode executes remote SPARQL queries and updates. The adapter is intended for a small single-writer academic demonstration, not concurrent production deployment.

## 4. Reproducible SPARQL demonstration

The six prepared queries cover cast by film, collaboration counts, studio film counts, award recipients, camera credits and talent with multiple professions. They are accessible through the research tools and stored as `.sparql` files under `src/dal/models/semantic/`.

Run them locally or remotely:

```bash
python semantic_main.py --queries
python semantic_main.py --virtuoso --queries
```

An example query for the Virtuoso query interface (subject to graph read permissions):

```sparql
PREFIX pc: <https://github.com/karanbe17/film-talent-kg/ontology#>
SELECT ?title
FROM <https://github.com/karanbe17/film-talent-kg/graph/data>
WHERE { ?movie a pc:Movie ; pc:title ?title . }
ORDER BY ?title
```

To demonstrate temporary CRUD operations without changing the original sample:

```bash
python demo_sparql.py
```

For live Virtuoso graph loading and CRUD verification using disposable graphs:

```bash
python verify_virtuoso.py
```

In the website, create temporary records through the relevant forms, inspect their relationships, update them, and delete them afterward. Removing a film or person removes associated dependent roles and awards; in-use studios cannot be deleted. Minimum participation constraints are not fully enforced during incremental entry.

## 5. Testing and verification

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

| Check | Recorded result |
| --- | --- |
| Automated tests | Five passed during implementation (four local application tests, one simulated protocol test) |
| Local SPARQL DML | All assertions passed; original data unchanged |
| Live Virtuoso | Graph loading, SELECT, INSERT, UPDATE and DELETE passed on the merged repository, as reported by the team |
| Studio film counts | 29 rows |
| Award recipients | 82 rows |
| Camera crew credits | 35 rows |
| Talent with multiple professions | 1 row |
| Website and quickstart | Successful execution reported by the team |
| Ontology | RDF/XML parsing and structural inspection; full OWL reasoner validation not claimed |

To inspect the ontology visually, open `producast.owl` in Protégé. This is separate from RDF/XML parsing and live SPARQL verification.

## 6. Reset, maintenance and troubleshooting

| Command | Effect |
| --- | --- |
| `python semantic_main.py --reset` | Regenerates the local sample and replaces the local working graph. |
| `python semantic_main.py --virtuoso --reset` | Replaces the application named graphs with the seed and ontology. |
| `python semantic_main.py --init-only --reset` | Regenerates local seed and working graph without launching the website. |
| `docker compose down` | Stops Virtuoso while preserving its volume. |

**Reset operations discard changes in the affected working graphs.** Export valuable edits before resetting. Omit `--reset` on subsequent launches to retain changes.

| Symptom | Action |
| --- | --- |
| Docker daemon connection error | Start Docker and check `docker info`. |
| Connection closed immediately after startup | Inspect `docker compose logs --tail=30 virtuoso` and verify HTTP readiness. |
| HTTP authentication failure | Confirm account credentials and authenticated SPARQL permissions. |
| Missing Python module | Activate the correct environment and reinstall the requirements. |
| Port 8000 already in use | Stop the existing application or launch with `--port 8001`. |

Generated databases, working RDF files, caches and virtual environments are excluded from version control. Keep credentials private.

## 7. Application previews

The following screenshots show the rebuilt application in embedded RDFLib mode; live Virtuoso verification is recorded separately above. Open the links below to view the screenshots at full size.

### Movie catalogue

[View Movie catalogue screenshot](docs/semantic_screenshots/movies.png)

### Movie profile

[View Movie profile screenshot](docs/semantic_screenshots/rocky.png)

### Director directory

[View Director directory screenshot](docs/semantic_screenshots/directors.png)

### Talent directory

[View Talent directory screenshot](docs/semantic_screenshots/talent.png)

### Awards

[View Awards screenshot](docs/semantic_screenshots/awards.png)

### SPARQL research tools

[View SPARQL research tools screenshot](docs/semantic_screenshots/query.png)

[Overview](docs/semantic_screenshots/overview.png) · [Talent portfolio](docs/semantic_screenshots/portfolio.png) · [Collaborations](docs/semantic_screenshots/connections.png) · [Mobile layout](docs/semantic_screenshots/mobile.png)

## 8. References and documentation

- [Project overview and contributors](README.md)
- [Milestone 5 ACM report](docs/5_Semantic_Karan_Moksh.pdf)
- [Catalogue provenance and limitations](data/raw/SOURCES.md)
- [W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)
- [W3C SPARQL 1.1](https://www.w3.org/TR/sparql11-overview/)
- [RDFLib documentation](https://rdflib.readthedocs.io/)
- [OpenLink Virtuoso Docker setup](https://www.openlinksw.com/howto/install/docker/)

Repository access, documented IRIs, standard semantic formats, source provenance and repeatable setup support FAIR-oriented reuse. See [LICENSE](LICENSE) for repository licensing terms.
