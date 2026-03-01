# Contributing to Claude Code Starter Kit

Thank you for your interest in contributing! This guide will help you get started.

## Ways to Contribute

### 1. Add New Commands

Create a new slash command in `.claude/commands/`:

```markdown
---
name: your-command
description: "Brief description of what it does"
---

# Command Title

What this command does: $ARGUMENTS

## Instructions
[Detailed instructions for Claude]

## Examples
[Usage examples]
```

### 2. Add New Agents

Create a specialized agent in `.claude/agents/`:

```markdown
---
name: your-agent
description: "Agent specialization"
model: sonnet
---

# Agent Name

You are a [role] specializing in [expertise].

## Responsibilities
[What this agent does]

## Process
[How it works]
```

### 3. Language-Specific Templates

Add templates for specific languages or frameworks:
- Create a folder: `templates/python-django/`
- Include customized CLAUDE.md, commands, and agents
- Add a README explaining the setup

### 4. Improve Documentation

- Fix typos and clarify instructions
- Add examples and use cases
- Translate to other languages

### 5. Report Issues

Open an issue for:
- Bugs in commands or agents
- Feature requests
- Documentation gaps

## Contribution Guidelines

### Code Quality

- Keep commands focused on one task
- Include clear instructions for Claude
- Add examples where helpful
- Test commands before submitting

### Commit Messages

Use conventional commits:

```
feat: add /deploy command for Vercel
fix: correct regex in security scanner
docs: add Python testing examples
chore: update dependencies
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test your changes with Claude Code
5. Submit a pull request

### PR Template

```markdown
## Description
[What does this PR add/change?]

## Type of Change
- [ ] New command
- [ ] New agent
- [ ] Bug fix
- [ ] Documentation
- [ ] Other

## Testing
[How did you test this?]

## Checklist
- [ ] I've tested with Claude Code
- [ ] Documentation is updated
- [ ] No sensitive data included
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/dachivadachkoria/claude-code-starter-kit.git

# Create a test project
mkdir test-project
cd test-project

# Copy starter kit
cp -r ../claude-code-starter-kit/.claude .
cp ../claude-code-starter-kit/CLAUDE.md .

# Test with Claude Code
claude
```

## Style Guide

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Include code blocks with language specifiers
- Use emoji sparingly and consistently

### Commands

- Clear, action-oriented names: `/test`, `/deploy`
- Include `$ARGUMENTS` handling
- Document all options
- Provide example output

### Agents

- Define clear expertise areas
- Include step-by-step processes
- Specify output format
- List anti-patterns to avoid

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

## Questions?

- Open a Discussion for general questions
- Open an Issue for bugs or feature requests
- Tag maintainers if urgent

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make Claude Code more accessible to developers! 🙏
