# CLAUDE.md

This file provides guidance for AI assistants working with this codebase.

## Project Overview

This is a new repository. Update this section as the project develops with:
- Project purpose and goals
- Target users/audience
- Key features

## Repository Structure

```
/home/user/test/
├── CLAUDE.md          # AI assistant guidance (this file)
└── (empty)            # Add project files here
```

Update this structure diagram as files are added.

## Tech Stack

Document the technologies used:
- **Language(s):** (e.g., TypeScript, Python, Go)
- **Framework(s):** (e.g., React, FastAPI, Express)
- **Build Tool(s):** (e.g., npm, cargo, make)
- **Testing:** (e.g., Jest, pytest, go test)
- **Linting:** (e.g., ESLint, ruff, golangci-lint)

## Development Commands

Document common development commands here:

```bash
# Install dependencies
# npm install / pip install -r requirements.txt / go mod download

# Run development server
# npm run dev / python main.py / go run .

# Run tests
# npm test / pytest / go test ./...

# Lint code
# npm run lint / ruff check . / golangci-lint run

# Build for production
# npm run build / python -m build / go build
```

## Code Conventions

### General Guidelines
- Write clear, self-documenting code
- Follow the project's established patterns
- Add comments for complex logic
- Keep functions focused and small

### Naming Conventions
- Document naming patterns for files, functions, variables, etc.

### File Organization
- Document where different types of code should go

## Testing Guidelines

- Write tests for new functionality
- Maintain existing test coverage
- Run the full test suite before committing

## Git Workflow

- **Branch naming:** Use descriptive branch names (feature/, bugfix/, etc.)
- **Commit messages:** Write clear, concise commit messages
- **PR process:** Document the pull request workflow

## Important Notes for AI Assistants

1. **Read before writing:** Always understand existing code patterns before making changes
2. **Test changes:** Run tests after making modifications
3. **Preserve style:** Match the existing code style in the project
4. **Ask when unclear:** If requirements are ambiguous, ask for clarification
5. **Incremental changes:** Make small, focused changes rather than large rewrites

## Security Considerations

- Never commit secrets, API keys, or credentials
- Sanitize user inputs
- Follow security best practices for the tech stack

---

*Last updated: 2025-11-21*
*Update this file as the project evolves.*
