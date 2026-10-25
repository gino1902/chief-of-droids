# CV workspace

Personal CV work. Not part of the chief-of-droids skill tooling.

- `factbase.md` holds the target-neutral facts: identity, timeline, then interview rounds appended as they happen. Facts are edited here only.
- `inputs/` holds the earlier fact bases and decision records, read-only history. The September 2026 fact base lives there.
- `material/` is the drop zone for source documents (earlier CVs, LEAP and Oxygen material, LinkedIn exports). Inputs, never edited.
- One folder per application, named `<employer>-<role>-<year>`, holding that target's `decisions.md`, the research briefs and the CV versions.
- `tools/md2cv_docx.py` renders a CV markdown file to an unbranded docx: `python3 tools/md2cv_docx.py <cv.md> <out.docx>`. It expects a bold subtitle line right after the name heading, then the contact line. Its docstring still says it was built for the September CV, which is where it came from.
- Conventions carried over from the September 2026 effort: invent nothing, a missing fact is omitted, every fact cites its source letter from the list at the top of `factbase.md`.
