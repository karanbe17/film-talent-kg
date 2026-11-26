# Conceptual-model refinement for Milestone 5

The original Chen diagram is retained as the submitted conceptual baseline, without surrogate IDs. The revised domain includes the following refinements; all identifiers are implementation keys/IRIs, not conceptual attributes.

| Relationship | Domain meaning | Participation |
|---|---|---|
| Movie — filmed by — CameraMan | A film has cinematographers; each cinematographer may work on several films. | Many-to-many, zero or more recorded camera credits during incremental entry. |
| Award — awarded for — Movie | An award occurrence may identify the film for which it was won. | At most one film per award occurrence; each film can have many wins. |
| Award — received by — Person | An award occurrence belongs to one recipient. | One recipient per occurrence; a person may receive many awards. |
| Movie — produced by — Studio | This demonstration selects one credited production company for each film, not all production companies. | Exactly one selected company per movie in seed; many films per studio. |
| Movie — directed by — Director | Director–film creative credit. | Many-to-many; at least one director in seed. |
| PerformanceRole — filled by — Actor | Each role occurrence identifies a performer. | Exactly one actor per role. |
| PerformanceRole — belongs to — Movie | Each role occurrence identifies the film. | Exactly one movie per role. |

Release year is added to Movie as a meaningful attribute where exact release dates are not established. `referenceUrl` and `source` are technical provenance metadata rather than film-domain identifiers. Role type and billing order may remain unknown. Class hierarchy and original natural domain labels remain unchanged; names are not asserted globally unique.
