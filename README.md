# ProduCast: Interoperable Knowledge Representation for Film Casting

![Course](https://img.shields.io/badge/Course-CSC501%20Fall%202026-blue)
![University](https://img.shields.io/badge/Institution-University%20of%20Victoria-gold)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-green)

## 1. Overview
**ProduCast** is a progressive data modeling architecture and knowledge representation framework designed to assist directors and producers in multi-relational talent assembly. The system maps complex industry relationships—spanning cast (leads, supporting, cameos) and creative crew (cinematographers)—to ensure interoperable and semantically rich data retrieval.

This project transitions through Conceptual Modeling (ERD), Logical Relational Schemas (SQLite/3NF), and ultimately Semantic Web Knowledge Graphs (RDF/OWL/SPARQL).

## 2. System Architecture
The current relational milestone is built on a three-tier architecture:
1. **Presentation Layer:** HTML/CSS web forms for safe data entry and search retrieval.
2. **Application Layer:** A Python Flask backend (`app.py`) that translates HTTP requests into SQL Data Manipulation Language (DML) commands.
3. **Data Layer:** A lightweight local SQLite database (`ProduCast.db`) enforcing ISA hierarchies and `ON DELETE CASCADE` referential integrity constraints.

## 3. Prerequisites
To run this project locally, ensure you have the following installed:
* **Python 3.9+**
* **Git**
* A modern web browser

**Required Python Packages:**
* `Flask==3.0.0`

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
pip install Flask
```

## 5. Quickstart & Demonstration
The SQLite database (`ProduCast.db`) is pre-configured with the DDL schema and seed data. To launch the user interface and demonstrate the DML operations:

```bash
# Navigate to the UI directory
cd src/ui

# Run the Flask application
python app.py
```
**Access the Application:** Open your web browser and navigate to `http://127.0.0.1:5000`. 

**Demonstration Steps:**
1. **INSERT:** Use the "Register New Talent" form to add an actor.
2. **SELECT:** Use the "Search Movies by Genre" form (e.g., enter "Sci-Fi") to dynamically filter the database.
3. **DELETE:** Click the "Delete" button next to any movie in the primary database to verify the `ON DELETE CASCADE` backend constraints (which automatically purge associated bridge table records).

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
├── src/
│   ├── relational/sql/       # SQL DDL schemas and local SQLite database (.db)
│   ├── ui/                   # Flask backend (app.py) and frontend HTML templates
│   └── ontology/             # RDF/OWL domain ontologies and SPARQL scripts (Upcoming)
├── data/                     # Dataset samples and knowledge graph triples
├── README.md                 # Project documentation and setup instructions
└── LICENSE                   # CC BY-NC-SA 4.0 licensing terms
```

## 9. License & Citation
This project and its associated software artifacts are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License. 

If referencing this architecture in academic work, please cite the Milestone 4 report located in the `/docs` directory.
