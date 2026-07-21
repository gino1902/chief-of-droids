# chief-of-droids project instructions

## Skills lab isolation

The skills lab is the sibling repository `../skills-lab`, outside this tree. It holds
work-in-progress and draft skills that must not leak into chief-of-droids sessions.

Two rules keep the boundary intact:

1. Never add the lab to a chief-of-droids session. Do not launch a session with
   `--add-dir ../skills-lab`, and do not open the lab as a working directory from
   within this repo. Skills reach this repo only through `deploy.sh`, never through
   live discovery.

2. No skill-name collisions across discoverable tiers. A skill name that already
   resolves at one `.claude/skills` tier inside this repo (the root
   `.claude/skills`, or a subfolder such as `wiki-data/.claude/skills`) must not
   also be placed at another tier. One name resolves at exactly one tier, so
   discovery is unambiguous.
