# Week 10 Lab: Markdown Memory (Plugin Contract Spec)

## `plugin-contract.md` template

```markdown
# Plugin Contract

## Plugin name and purpose
<name>

## Input schema
- <argument>: <type + meaning>

## Output schema
- <field>: <type + meaning>

## Error modes
- <error condition 1>:
  - When it occurs:
  - What the output/error payload looks like:

## Safety constraints (must never do)
1. <constraint>
2. <constraint>

## Versioning policy
- How breaking changes are introduced:
- How compatibility is maintained:
- What the agent should do with old versions:

## Fallback behavior when the plugin fails
- What the agent does next:
- What guarantees it still preserves:
```

## Deliverables
- `plugin-contract.md` (filled)
- One paragraph describing how this plugin reduces tokens or improves reliability

