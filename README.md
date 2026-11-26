# 🎬 ProduCast — Film Casting & Production Knowledge Graph

![Course](https://img.shields.io/badge/Course-CSC501%20Fall%202026-blue)
![Institution](https://img.shields.io/badge/Institution-University%20of%20Victoria-gold)
![Semantic Web](https://img.shields.io/badge/Semantic%20Web-RDF%20%7C%20OWL%20%7C%20SPARQL-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688)
![Virtuoso](https://img.shields.io/badge/Triple%20Store-Virtuoso-555555)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-green)

ProduCast is a knowledge representation and data modelling project developed for CSC501 at the University of Victoria. It helps producers and directors explore film credits, talent portfolios, awards and professional collaborations through an interconnected film catalogue.

The project progresses from conceptual ER modelling and normalized relational storage to an interoperable Semantic Web application. The current implementation (Milestone 5) uses RDF, OWL and SPARQL with OpenLink Virtuoso. The earlier SQLite/Flask application remains available separately.

[Technical setup](README_SEMANTIC.md) · [Milestone 5 report (PDF)](docs/5_Semantic_Karan_Moksh.pdf) · [LaTeX source](docs/5_Semantic_Karan_Moksh.tex) · [Data sources](data/raw/SOURCES.md)

[View ProduCast producer workspace screenshot](docs/semantic_screenshots/overview.png)

*Producer workspace — catalogue overview and navigation.*

## Contents

[Features](#1-features) · [Architecture](#2-architecture) · [Getting started](#3-getting-started) · [Demonstration](#4-demonstration) · [Repository structure](#5-repository-structure) · [Milestones](#6-academic-project-milestones) · [Contributors](#7-contributors) · [FAIR](#8-fair-and-reproducibility) · [License](#9-license--citation)

## 1. Features

- Separate actor, director and cinematographer directories with searchable portfolios.
- Movie profiles linking films, characters, talent and production companies.
- Actor–director collaboration discovery and repeat partnership analysis.
- Selected award wins, casting records and studio portfolios.
- Create, read, update and delete (CRUD) operations for catalogue records.
- Six prepared SPARQL queries and RDF/XML export through the research tools.

### Sample catalogue

| Catalogue entity | Count |
| --- | ---: |
| Films | 35 |
| Actors | 43 |
| Directors | 31 |
| Cinematographers | 31 |
| Distinct people | 104 |
| Production companies | 29 |
| Acting credits | 59 |
| Selected award wins | 82 |

The catalogue is a curated academic sample, not a comprehensive or independently verified film database. Professional roles may overlap. Awards represent selected wins rather than lifetime totals. See [source documentation](data/raw/SOURCES.md).

## 2. Architecture

| Layer | Responsibility |
| --- | --- |
| Presentation (`src/ui/`) | FastAPI routes, Jinja2 templates and local CSS assets. |
| Business logic (`src/biz/`) | Catalogue operations, validation and prepared SPARQL queries. |
| Data access (`src/dal/`) | Relational-to-RDF conversion, RDFLib storage and Virtuoso adapter. |
| Persistence | Separate ontology and instance graphs in Virtuoso; local RDF/XML fallback. |

The [conceptual ER diagram](docs/er/ProduCast_ER_Diagram.png) defines domain entities and relationships. The normalized SQLite staging database is converted into RDF resources with stable IRIs, datatype properties and object properties. RDFLib supports conversion and validation; in Virtuoso mode, SELECT and update requests execute on the remote triple store.

### Data transformation workflow

1. Read the curated film and award catalogue from `data/raw/`.
2. Build normalized SQLite staging records using `src/dal/catalogue.py`.
3. Convert records into RDF individuals, literal attributes and object relationships.
4. Load the OWL ontology and instance data into separate graphs.
5. Execute SPARQL queries and updates through the selected storage adapter.
6. Present results through the producer workspace.

### Technology stack

| Component | Technology |
| --- | --- |
| Web interface | FastAPI, Jinja2, HTML and CSS |
| Business and conversion logic | Python |
| Relational staging | SQLite |
| Semantic representation | RDF/XML and OWL |
| Query language | SPARQL |
| Embedded graph processing | RDFLib |
| Persistent triple store | OpenLink Virtuoso |
| Deployment and testing | Docker Compose and unittest |

## 3. Getting started

**Prerequisites:** Git, Python 3.11 (tested on Windows; compatible versions may also work), a web browser, and Docker Desktop or Docker Engine with Compose for Virtuoso mode.

```bash
git clone https://github.com/karanbe17/film-talent-kg.git
cd film-talent-kg
```

### Manual environment setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

```bash
python -m pip install -r requirements-semantic.txt
```

### Option A — Quickstart without Docker

```bash
python quickstart_semantic.py
```

The script creates an isolated `.venv`, installs semantic dependencies and starts the embedded RDFLib application. On macOS/Linux, use `python3` if `python` is unavailable.

Open **http://127.0.0.1:8000**.

### Option B — Virtuoso (recommended for the semantic demonstration)

Start Docker Desktop, then set a private local database password.

Windows PowerShell:

```powershell
$env:PRODUCAST_VIRTUOSO_PASSWORD = 'replace-with-your-local-password'
```

macOS/Linux:

```bash
export PRODUCAST_VIRTUOSO_PASSWORD='replace-with-your-local-password'
```

Run the following from the repository root, using `python3` instead of `python` if needed:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=30 virtuoso
python quickstart_semantic.py --virtuoso
```

Start the application only after Virtuoso finishes initialization. Visit **http://127.0.0.1:8000** for ProduCast or **http://127.0.0.1:8890/conductor** for Virtuoso administration (user `dba`). Do not commit passwords. See the [semantic setup guide](README_SEMANTIC.md) for manual installation, verification, graph configuration and reset instructions.

## 4. Demonstration

| Area | Suggested demonstration |
| --- | --- |
| Talent | Search Leonardo DiCaprio and inspect characters, films and selected awards. |
| Movies | Open Rocky and inspect its cast, director and character relationships. |
| Collaborations | Explore repeat actor–director partnerships, including Martin Scorsese and Leonardo DiCaprio. |
| Research tools | Execute prepared SELECT queries and export the RDF/XML graph. |
| CRUD | Create, inspect, edit and delete temporary catalogue records. |

### Application previews

These screenshots show the rebuilt application in embedded RDFLib mode. Live Virtuoso verification is documented separately below. Open the links below to view the screenshots.

[View Talent portfolio screenshot](docs/semantic_screenshots/portfolio.png)

*Talent portfolio — filmography, characters and awards.*

[View Professional collaborations screenshot](docs/semantic_screenshots/connections.png)

*Collaboration explorer — recurring professional partnerships.*

[View SPARQL research interface screenshot](docs/semantic_screenshots/query.png)

*Research tools — prepared queries and structured results.*

[Movie profiles](docs/semantic_screenshots/rocky.png) · [Director directory](docs/semantic_screenshots/directors.png) · [Award records](docs/semantic_screenshots/awards.png)

### Additional application views

| Screenshot | Description |
| --- | --- |
| [Movie catalogue](docs/semantic_screenshots/movies.png) | Browse available film records. |
| [Talent directory](docs/semantic_screenshots/talent.png) | Explore film industry professionals. |
| [Mobile interface](docs/semantic_screenshots/mobile.png) | Responsive application layout. |

### Verification

Install test dependencies into the Python environment used to run the application:

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
python demo_sparql.py
```

With Virtuoso running and the password set in the same terminal:

```bash
python verify_virtuoso.py
python semantic_main.py --virtuoso --queries
```

The team reported successful live Virtuoso graph loading, SELECT, INSERT, UPDATE and DELETE verification, website launch and quickstart execution. Five automated tests passed during implementation, and the isolated DML demonstration preserved the original data. Full OWL reasoner validation is not claimed. See the [technical guide](README_SEMANTIC.md) for scope and reproduction details.

### Recorded live query results

| Query | Rows returned |
| --- | ---: |
| Studio film counts | 29 |
| Award recipients | 82 |
| Camera crew credits | 35 |
| Talent with multiple professions | 1 |

## 5. Repository structure

```text
film-talent-kg/
├── data/
│   ├── raw/                         # Curated catalogue and source notes
│   └── preprocessed/                # Generated staging and working databases
├── docs/
│   ├── er/                          # Conceptual ER model
│   ├── semantic_screenshots/        # Application previews
│   ├── producast-logo.svg           # Project logo
│   ├── 5_Semantic_Karan_Moksh.pdf    # Milestone 5 report
│   └── 5_Semantic_Karan_Moksh.tex    # LaTeX source
├── src/
│   ├── cmn/                         # Relational configuration
│   ├── biz/                         # Business services
│   ├── dal/                         # Conversion and data access
│   │   └── models/
│   │       ├── relational/          # SQL schema and seed scripts
│   │       └── semantic/            # OWL, RDF/XML and SPARQL
│   └── ui/                          # Relational and semantic interfaces
├── tests/                           # Automated tests
├── compose.yaml                     # Virtuoso configuration
├── main.py                          # Original relational application
├── semantic_main.py                 # Semantic application entry point
├── quickstart_semantic.py           # Automated environment and launch
├── demo_sparql.py                   # Isolated CRUD demonstration
├── verify_virtuoso.py               # Live triple-store verification
├── requirements.txt                 # Relational dependencies
├── requirements-semantic.txt        # Semantic dependencies
├── requirements-test.txt            # Test dependencies
├── README_SEMANTIC.md                # Detailed semantic setup
├── README.md
└── LICENSE
```

## 6. Academic project milestones

| Milestone | Scope | Status |
| --- | --- | --- |
| 1 | Project definition and team formation | Completed |
| 2 | Background and related work | Completed |
| 3 | Three-minute presentation | Completed |
| 4 | Relational solution design | Completed |
| 5 | Semantic Web solution design | Implemented and tested |
| 6 | Final project demonstration | Upcoming |

The original relational application can be launched independently with `python main.py` after installing `requirements.txt`. It runs at http://127.0.0.1:5000. Use `python main.py --queries` to reproduce its SQL demonstrations. Its `--reset` option rebuilds the relational sample database and removes local edits.

## 7. Contributors

| Contributor | Integration and verification focus |
| --- | --- |
| Karan Brahmbhatt | Semantic backend, ontology, RDF conversion, Virtuoso integration and verification. |
| Moksh Patel | Producer-facing interface, frontend integration and application documentation. |

The responsibilities above describe the division of integration and verification work.

## 8. FAIR and reproducibility

- **Findable:** Repository, report, documented resource IRIs and organized source files.
- **Accessible:** Repository access for authorized course reviewers; RDF/XML export and documented setup.
- **Interoperable:** Standard RDF, OWL and SPARQL representations.
- **Reusable:** Source catalogue, provenance notes, converter, dependency specifications and repeatable tests.

## 9. License & citation

The repository identifies its license as [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE](LICENSE) for the applicable terms. Third-party tools and source material retain their respective terms.

For academic references, cite Brahmbhatt, K. and Patel, M. (2026), *ProduCast*, CSC501 Milestone 5, University of Victoria. See the [ACM report](docs/5_Semantic_Karan_Moksh.pdf) and its bibliography for the full technical references.
