# ProduCast: Interoperable Knowledge Representation for Film Casting

![Course](https://img.shields.io/badge/Course-CSC501%20Fall%202026-blue)
![University](https://img.shields.io/badge/Institution-University%20of%20Victoria-gold)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-green)

## 1. Overview
**ProduCast** (formally *Representing Film Casting and Production Networks*) is a progressive data modeling architecture and knowledge representation framework designed to assist directors and producers in multi-relational talent assembly. The system maps complex industry relationships—spanning cast (leads, supporting, cameos) and creative crew (directors)—to ensure interoperable and semantically rich data retrieval.

This project transitions through Conceptual Modeling (ERD), Logical Relational Schemas (SQLite/3NF), and ultimately Semantic Web Knowledge Graphs (RDF/OWL/SPARQL).

## 2. System Architecture
The current relational milestone utilizes a strict, fully decoupled three-tier architecture:
1. **Presentation Layer (`src/ui`):** A Flask web application rendering pure HTML/CSS Jinja2 templates (Cinematic Dark Mode). Contains zero raw SQL.
2. **Business Logic Layer (`src/biz`):** Orchestrates multi-step transactions, sanitizes inputs, and raises `BizError` exceptions to enforce integrity rules before data hits the database.
3. **Data Access Layer (`src/dal`):** Domain-specific modules (`movie_dal.py`, `person_dal.py`) that handle all parameterized SQL execution. Backed by `config.py` for dynamic `pathlib` relative pathing, guaranteeing crash-free instantiation across any host environment (including GitHub Codespaces).

## 3. Prerequisites
To run this project locally, ensure you have the following installed:
* **Python 3.9+**
* **Git**
* A modern web browser

## 4. Installation Guide
Follow these steps to clone the repository and set up the local environment.

```bash
# 1. Clone the repository
git clone https://github.com/karanbe17/film-talent-kg.git
cd film-talent-kg

# 2. Create a virtual environment (Recommended)
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

## 5. Quickstart & Demonstration
The system includes an automated initialization sequence. You do not need to manually build the database.

```bash
# Run the application directly from the repository root
python main.py
```

*Note: If `ProduCast.db` is missing, `main.py` will automatically read `01_schema.sql` and `02_seed.sql` to bootstrap the schema and seed the database in the `data/preprocessed/` directory before launching the server.*

**Access the Application:** Open your web browser and navigate to `http://127.0.0.1:5000`. 

**Demonstration Steps:**
1. **INSERT:** Use the "Add Movie Project" and "Cast Talent" forms to create multi-relational links.
2. **SELECT:** Use the "Search & Filter Database" form (e.g., enter "Sci-Fi") to dynamically query the portfolio.
3. **DELETE (Cascade):** Click "Delete" next to a movie in the Project Portfolio. Scroll down to the Casting Ledger to verify that `ON DELETE CASCADE` automatically purged all associated bridge table records without leaving orphans.

**Additional Commands:**
* `python main.py --queries`: Executes the demonstration DML tests (multi-join aggregations, subqueries) directly in the terminal.
* `python main.py --reset`: Drops the existing database and safely rebuilds it from the seed files.

## 6. Team Members & Responsibilities

| Contributor | Role | Core Domain & Technical Focus |
| :--- | :--- | :--- |
| **Karan Brahmbhatt**<br>`karanbrahmbhatt@uvic.ca` | Conceptual Architect & Character Subsystem | Scoping domain boundaries, conceptual ERD design for cast/archetypes, OWL ontology formalization, and semantic expressivity evaluation. |
| **Moksh Patel**<br>`mokshpatel@uvic.ca` | Relational Systems & Crew Subsystem | Logical relational schema transformation, SQL DDL design, triple store ingestion, and SPARQL query performance benchmarking. |

## 7. Milestone Timeline

* **Milestone 1:** Project Definition & Team Formation (Completed)
* **Milestone 2:** Background & Related Work / Literature Review (Completed)
* **Milestone 3:** Project Presentation / 3-Minute Talk (Completed)
* **Milestone 4:** Solution Design Part I: Relational (Completed)
* **Milestone 5:** Solution Design Part II: Semantic Web (Upcoming)
* **Milestone 6:** Project Demonstration / 10-Minute Talk (Upcoming)

## 8. Repository Structure

```text
film-talent-kg/
├── docs/                     # LaTeX reports, architecture diagrams, and UI screenshots
├── data/
│   └── preprocessed/         # Auto-generated SQLite database (ProduCast.db)
├── src/
│   ├── cmn/                  # Central configuration and dynamic pathing
│   ├── biz/                  # Business logic, validation, and multi-step orchestration
│   ├── dal/                  # Data Access Layer and relational SQL scripts
│   ├── ui/                   # Flask presentation layer and HTML templates
│   └── ontology/             # RDF/OWL domain ontologies and SPARQL scripts (Upcoming)
├── main.py                   # Single entry point / automated quickstart script
├── requirements.txt          # Python dependencies (Flask>=3.0)
├── README.md                 # Project documentation and setup instructions
└── LICENSE                   # CC BY-NC-SA 4.0 licensing terms
```

## 9. License & Citation
This project and its associated software artifacts are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License. 

If referencing this architecture in academic work, please cite the Milestone 4 report located in the `/docs` directory.
