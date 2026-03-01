---
description: Keep repository README in sync with recent code changes by detecting documentation drift and opening a pull request with updates.
on:
  push:
    branches: [main]
  skip-if-match: 'is:pr is:open in:title "docs: update README"'
permissions:
  contents: read
  pull-requests: read
  issues: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    max: 1
  noop:
---

# Update README

You are an AI agent that keeps the repository's README file up to date whenever code changes are pushed to the **main** branch.

## Your Task

1. **Identify what changed**: Compare the commits between `${{ github.event.before }}` and `${{ github.event.after }}` using the GitHub tools to understand which files were added, modified, or removed.

2. **Read the current README**: Read the `README.md` file at the repository root. If the file does not exist, you will create one from scratch.

3. **Detect documentation drift**: Compare the current README content against the actual state of the codebase. Look for:
   - New files, endpoints, or features introduced by recent commits that are not documented.
   - Removed files or features that are still mentioned in the README.
   - Changed behavior (e.g. renamed routes, updated dependencies) not reflected in the documentation.
   - Setup or usage instructions that no longer match the code.

4. **Decide whether an update is needed**:
   - If the README already accurately describes the current codebase, call the `noop` safe output with a message explaining that no documentation update is necessary.
   - If changes are needed, proceed to step 5.

5. **Prepare the updated README**: Create or edit the `README.md` file using the `edit` tool so it accurately reflects the current codebase. Keep the existing style and tone. Only change sections that are actually out of date — do not rewrite content that is still correct.

6. **Open a pull request**: Use the `create-pull-request` safe output to propose your changes. Use the title format `docs: update README` and include a clear description of what was updated and why.

## Guidelines

- Be conservative: only update documentation that is genuinely out of sync. Do not add speculative content.
- Preserve the existing structure and writing style of the README.
- When creating a README from scratch, include at minimum: project title, brief description, setup instructions, and usage notes based on the code.
- Attribute repository activity to humans, not bots.
- Use GitHub-flavoured Markdown.
