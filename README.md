# Screenplay-to-Screen: An Interoperable Knowledge Representation for Film Casting and Production Networks

![Course](https://img.shields.io/badge/Course-CSC501%20Fall%202026-blue)
![University](https://img.shields.io/badge/Institution-University%20of%20Victoria-gold)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-green)

An interoperable data modeling architecture and knowledge representation framework designed to assist directors and producers in multi-relational talent assembly—spanning cast (leads, supporting, cameos) and creative crew (cinematographers, writers, composers).

---

## 👥 Team Members & Responsibilities

| Contributor | Role | Core Domain & Technical Focus |
| :--- | :--- | :--- |
| **Karan Brahmbhatt**<br>`karanbrahmbhatt@uvic.ca` | Conceptual Architect & Character Subsystem Lead | Scoping domain boundaries, conceptual ERD design for cast/archetypes, OWL ontology formalization, and semantic expressivity evaluation. |
| **Moksh Patel**<br>`mokshpatel@uvic.ca` | Relational Systems & Crew Subsystem Lead | Logical relational schema transformation, SQL DDL design, triple store ingestion, and SPARQL query performance benchmarking. |

---

## 🎯 Project Architecture & Representation Pipeline

This project explores four progressive paradigms of data representation:
1. **Conceptual Modeling:** Formalizing an Entity-Relationship Diagram (ERD) capturing multi-relational constraints between screenplays, character archetypes, actors, and creative crews.
2. **Logical Relational Schema:** Translating ER representations into normalized relational tables (3NF/BCNF) with foreign key constraints, evaluated via complex multi-join SQL queries.
3. **Semantic Web Representation:** Building an RDF/OWL domain ontology to explicitly capture non-functional artistic synergy, directorial styles, and trope archetypes.
4. **Knowledge Graph & Triple Store:** Storing knowledge graph triples in an RDF database (e.g., GraphDB / Jena) and executing expressive SPARQL queries.

---

## 📂 Repository Structure

The project artifacts and milestone deliverables are organized as follows:

| Directory / File | Description |
| :--- | :--- |
| `docs/` | Milestone reports, research proposal drafts, and presentation slides. |
| `src/relational/` | Conceptual ERD assets, SQL DDL relational schemas, and data manipulation queries. |
| `src/ontology/` | RDF/OWL domain ontology definitions, SPARQL query scripts, and mapping rules. |
| `data/` | Dataset samples, metadata extracts, and graph triples. |
| `README.md` | Project overview, team roles, architecture summary, and setup instructions. |
| `LICENSE` | CC BY-NC-SA 4.0 licensing terms for open academic reuse. |

---

## 📄 License

This project and its associated software artifacts are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License.
