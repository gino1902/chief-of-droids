# C4 diagram expression: workflow capture

Captured from the 2026-06-24 session that reworked the ADLS-to-bronze flowchart into a C4 container diagram. This is preparation input for a future editing-docs capability. It records the goal, the workflow, and the guidance. It does not create the skill or the template yet.

## Goal

Give editing-docs a repeatable way to express a known architecture as a C4 diagram in Mermaid, against the Elevate theme, conformant with the C4 model and the Structurizr conventions, and render-safe on the Mermaid plus elk stack.

Scope is expression, not authoring. The architecture (what the systems, containers and components are) is decided elsewhere or supplied by the user. This capability maps that architecture onto C4 notation and renders it. It generalises across the three static C4 levels: system context, container, component. Dynamic and deployment diagrams are out of scope and deployment concerns are kept out of the structural diagrams on purpose (see the abstraction rules).

## Workflow

The session ran seven phases. They generalise to any C4 level.

1. Lock the mapping. Agree the Mermaid-shape-to-C4-element vocabulary before drawing. Treat the mapping table as the contract for the rest of the work.
2. Surface misfits early. List the elements that do not map cleanly (vendor or deployment boundaries, internal-only parts, externals, message infrastructure) with a proposed default for each, and resolve them in one exchange rather than mid-render.
3. Fetch references. Pull the C4 and Structurizr pages before making any conformance claim. No unfetched citation.
4. Apply the notation. Title, boundaries, element subgraphs, black-box nodes, label lines, shape by kind, verb-first relationships, edge styling.
5. Set the abstraction. Pick the level, hold it, and treat any deeper zoom as a deliberate, called-out exception.
6. QA loop. Run a two-axis pass (text-versus-graph consistency, and display drift), tabulate findings with severity, recommend, apply on approval, re-verify, and iterate until the diagram settles.
7. Commit gate. Stage by explicit path, show the diff, commit, push manually.

## Notation guidance

### Title

Every diagram names the element in focus as the title. At context level that is the system in focus, at container level the software system, at component level the container.

### Element label lines

Black-box nodes (no children shown) carry three lines.

| Element | Lines |
| :--- | :--- |
| Person | name, then [Person], then a verb-first description |
| Software system | name, then [Software system], then a verb-first function |
| Container | name, then the technology in brackets, then a verb-first function |
| Component | name, then [Component], then a verb-first function |

Note: the session vocabulary did not define a Person shape. Generalising to context level needs one. This is flagged as an open decision below.

### Shapes

The session shape vocabulary, to be confirmed and extended.

| Shape | Mermaid | Used for |
| :--- | :--- | :--- |
| Box | `[...]` | Application or service container, and any black-box system, component or person |
| Cylinder | `[(...)]` | Datastore container (database, queue, cache as a store) |
| Trapezoid | `[\.../]` | Object storage container |

### Boundaries and nesting

A boundary is a subgraph titled with the name of the thing it contains, plus its type tag where useful. Boundaries nest recursively, one level per C4 level.

- A sub-system or enterprise boundary holds software systems.
- A software system holds containers.
- A container holds components.

The element that owns children becomes a subgraph. The element shown as a black box becomes a node with the label lines above.

### Relationships

Every relationship reads source to destination and leads with an action verb. Keep the description short. A technology or protocol may be added where it carries weight. Default Structurizr styling is a dashed grey line, overridden by tag for meaningful classes like control plane, governance or launch.

## Abstraction rules

A boundary is drawn when the intent is to expose what is inside it. Cardinality is not the test. A boundary around a single child is valid when the point is to show the line between inside and outside. The same holds at each level: a software system shown with one container, a container shown with one component.

Holding one level is the default. Opening one element to the next depth (for example one container shown with its components while the others stay at container depth) is a legitimate deliberate zoom. When done, it must be called out in the notation prose so the reader knows the diagram is mixed-resolution by choice.

Deployment, vendor and infrastructure boundaries do not belong in a structural C4 diagram. They go in a deployment diagram. In the session the Azure and Databricks planes were modelled as software-system boundaries inside the in-focus solution, with ownership-versus-location tension carried by control edges and notes rather than by moving boxes. Capture that pattern: when a part lives in one place but is owned or operated by another, show location by placement and ownership by a control edge plus a note.

## Render safety, Mermaid plus elk

- Attach every edge to a node, never to a subgraph id. Edges on a cluster are the fragile case under elk and can mis-route. If a relationship is conceptually at the boundary level, source it from the boundary-facing child element instead.
- Node-shape rendering is independent of the layout engine. Choosing elk for layout does not restrict the node shapes.
- The trapezoid with a quoted multiline label is the fussiest construct. Use double-quoted labels and `<br/>` for line breaks. Literal square brackets inside a label need the quoted or markdown-string form so they do not close the node early.
- A frontmatter title needs Mermaid 10 or newer. On an older renderer it drops silently while the diagram still renders.
- Re-check the numeric linkStyle indices after any edge reorder. They are positional and silently mis-paint if the edge order changes.

## QA contract

Two axes, run as a tabulated pass.

Consistency, text versus graph. Reconcile every node and every edge against the prose. Confirm every node function line and every relationship description leads with a verb. Confirm the type tags are correct. Confirm the abstraction level is consistent, or that any zoom is stated.

Display drift. Check the linkStyle indices against the current edge order. Check shape and label render risks. Confirm the theme init block is present. Confirm title and any frontmatter are supported by the target renderer.

Process. Tabulate findings with a severity, recommend a fix, apply only on approval, re-verify, and iterate until no findings remain.

## Inherited conventions

- Elevate theme. The Mermaid init block lives at shared/elevate-theme/elevate-mermaid.md. Collapse a duplicate init line when copying.
- Verb-first. Every C4 node function line and every relationship description leads with an action verb (memory edit, this session).
- Version block at the foot of every workflow-written file. Increment on each material revision.
- Read the full file before any write. Full overwrite, no str_replace.
- Commit gate after every write. Stage by explicit path. Push is manual.

## Open decisions for skill authoring

- Person shape. The current vocabulary has no Person element. Context-level diagrams and supporting actors need one. Decide a shape and label form.
- Diagram types. Confirm the capability covers the three static levels only, with deployment and dynamic explicitly excluded and routed elsewhere.
- Relationship annotation. Decide whether to standardise a technology or protocol tag on edges, like [HTTPS] or [abfss], and where it sits in the label.
- Colour mapping. Decide whether colour follows the C4 element type or the Elevate semantic palette used in the session (specialised, mechanism, external, governance). The session used the Elevate palette, not strict C4 element colours.
- Home. Confirm whether this becomes an editing-docs reference template plus a HOW-TO-TRIGGER line (recommended, expression-only) or a standalone skill (only if C4 authoring logic is wanted).

<!--
Version: 1.0 | Last Updated: 2026-06-24 | Status: Draft
-->
