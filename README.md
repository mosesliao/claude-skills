# claude-skills

A collection of [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
— reusable instruction sets that extend Claude with domain-specific workflows.

## Skills in this repo

| Skill | What it does |
|-------|--------------|
| [`db-modernizer`](./db-modernizer) | Audits a legacy, badly-designed SQL database over a live connection and produces a cleanup-and-migration plan landing the data in a clean, normalized Laravel-ready schema. |

## Installing a skill

Each skill is a folder containing a `SKILL.md` plus optional `references/` and `scripts/`.
To use one in Claude, package the folder into a `.skill` file and upload it under
**Settings → Capabilities → Skills**:

```bash
python package_skill.py db-modernizer ./dist
```

Or point Claude Code at the folder directly.

## Repo layout

```
claude-skills/
├── LICENSE
├── README.md
└── db-modernizer/
    ├── SKILL.md
    ├── README.md
    ├── references/
    └── scripts/
```

## Contributing

Each skill lives in its own top-level folder and must contain a `SKILL.md` with YAML
frontmatter (`name`, `description`). Keep the description explicit about when the skill
should trigger — that text is what Claude matches against.

## License

MIT — see [LICENSE](./LICENSE).
