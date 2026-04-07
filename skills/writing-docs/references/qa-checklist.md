<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-04-07 -->

# Doc Writer QA Checklist

Run before proposing any document output.

- [ ] `references/doc-principles.md` read before writing
- [ ] Purpose, audience, and document type identified before writing
- [ ] Conclusion or main point stated at the top (except procedural docs)
- [ ] Each section covers exactly one concept
- [ ] Density matches document type
- [ ] Terms defined on first use
- [ ] Version, author, and date present on any document that will be referenced
- [ ] Output format selected deliberately — not defaulted
- [ ] If `.md`: `references/markdown-formatting.md` read and applied
- [ ] If output format is docx / pptx / xlsx / HTML / React / SVG: `references/theme.md` read and Elevate theme artifact passed to composed format skill
- [ ] If output format is HTML or React AND contains form elements (inputs, textareas, buttons, pill groups): `shared/elevate-theme/elevate-artifact.md` read and `applyAll()` inline style pattern applied — CSS custom properties on interactive elements are prohibited
- [ ] If version-sensitive technical claims present: `reviewing-tech-claims` skill loaded and applied
