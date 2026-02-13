# ccxt-pandas Claude Code Skills

This directory contains Claude Code skills to help you work with ccxt-pandas more efficiently.

## Available Skills

### `ccxt-pandas-helper`
Helper skill for working with ccxt-pandas in any project.

**What it provides:**
- Quick reference for sync/async usage patterns
- Common DataFrame structures for all fetch methods
- Batch operation examples
- Best practices and troubleshooting tips
- Testing setup guidance

## Using Skills

### Option 1: Use in ccxt-pandas Project (Automatic)
When working in the ccxt-pandas project directory, these skills are automatically available.
Invoke with: `/ccxt-pandas-helper`

### Option 2: Copy to Global Skills (For Other Projects)
To use these skills in any project on your machine:

**On Windows:**
```bash
cp .claude/skills/ccxt-pandas-helper.md C:\Users\<YOUR_USERNAME>\.claude\skills\
```

**On macOS/Linux:**
```bash
cp .claude/skills/ccxt-pandas-helper.md ~/.claude/skills/
```

After copying, the skill will be available in all your projects!

### Option 3: Keep Project-Specific
Keep the skill in `.claude/skills/` in your project repository. Anyone who clones your repo will have access to it when working in that project.

## Creating Your Own Skills

Skills are markdown files with frontmatter:

```markdown
---
name: my-skill-name
description: What this skill does
---

Your skill instructions here...
```

Place them in:
- `.claude/skills/` - Available in this project only
- `~/.claude/skills/` - Available globally across all projects

## Learn More

- [Claude Code Skills Documentation](https://docs.anthropic.com/claude/docs/claude-code-skills)
- See existing skills: `ls ~/.claude/skills/` or `ls .claude/skills/`