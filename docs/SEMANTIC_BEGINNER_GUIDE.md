# Learn the project in 10 minutes

**ERD:** a conceptual picture of entities and relationships in the real world; surrogate IDs belong to the relational implementation for this course. **Relational database:** tables and keys, with SQL joins. **RDF (Resource Description Framework):** statements as subject–predicate–object triples, e.g. `pc:movieExample pc:filmedBy pc:cameraExample`. Both ends are resources; `pc:movieExample pc:title "Oppenheimer"` has a literal object. An IRI uniquely identifies a resource, even if two people have identical names. The `pc:` prefix abbreviates the namespace. The same person can have several types, without creating several independent person resources.

**Ontology:** vocabulary plus formal meaning and constraints. **RDFS:** classes, subclass inheritance, domains and ranges. **OWL:** more expressive logic (e.g. each PerformanceRole belongs to exactly one Movie, and inverse relationships). `Actor rdfs:subClassOf Person` means every Actor is a Person. The program explicitly writes both types so queries work without a reasoner. The ER diagram's name/title identifiers are simplifying assumptions, not globally unique keys. **TBox** is the ontology (`producast.owl`); **ABox** is the actual facts (`seed.rdf` and working RDF file).

**Triple store:** stores RDF triples and executes graph queries. This project includes Virtuoso server storage and an embedded RDFLib fallback. RDFLib also performs data conversion. **SPARQL:** query language for RDF. Unlike SQL joins, graph patterns link shared variables. Example:

```sparql
PREFIX pc: <https://github.com/karanbe17/film-talent-kg/ontology#>
SELECT ?movie ?actor ?character WHERE {
  ?role pc:belongsTo ?m ; pc:filledBy ?a ; pc:characterName ?character .
  ?m pc:title ?movie .
  ?a pc:name ?actor .
}
```

`?role`, `?m`, `?a` and the names with `?` are variables. The semicolon repeats the same subject. The dot ends a triple pattern. The results are matching movie/actor/character rows. `INSERT DATA` adds triples, `DELETE WHERE` removes matched triples, and `DELETE/INSERT WHERE` changes a property. The website sends these commands through its services rather than asking users to type them.

**Open-world assumption:** not knowing a director is different from knowing there is no director. Missing source values are left absent and diagnosed, not falsely filled. OWL cardinality means a logical restriction, not SQL NOT NULL or a database check; validation is separately implemented in Python. **FAIR:** findable, accessible, interoperable and reusable; reproducible files and quickstart make the graph easier for others to evaluate.

## Explain in a viva

- Why not put surrogate keys in ERD? They are implementation identifiers; conceptual model describes domain meaning. Relational IDs become stable resource IRI suffixes when data is converted.
- Why `PerformanceRole` class? The actor–movie link carries its own character name, role type and billing order, so we model the role as an individual rather than losing those attributes.
- Why convert StudioName into Studio? Multiple movies can reference a shared resource, which can hold its own HQ and be queried independently.
- Why no SQL at runtime? SQL is used to build and read the curated normalized staging database during conversion. The semantic app reads and changes the RDF graph via SPARQL.
- Why a replacement catalogue? Original tables contained incomplete and inaccurate film credits. The new sample contains selected real credits and award wins.
- How does update work? The app validates fields, removes old triples for the resource, inserts updated triples, and persists the RDF/XML file. The explicit update script uses DELETE/INSERT WHERE.
- What is the limitation? Small local dataset, no automated OWL reasoning, selected rather than exhaustive credits, single-writer application, no user accounts. It is a working course demonstration, not a production casting service.
