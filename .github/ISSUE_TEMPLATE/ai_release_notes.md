---
name:  📋 Copilot Release Notes
about: Create release notes with Copilot
title: ''
type: task
assignees: 'copilot'
projects: []

---

**NOTE** Replace placeholders 
- {MILESTONE}: GitHub Milestone
- {VERSION_TO_RELEASE}: Format `<major>.<minor>`
- {LAST_RELEASE_TAG}: Format `v<major>.<minor>.0`

Write the release notes for version {VERSION_TO_RELEASE}. Take `docs/documentation/reference/release-notes/2_1/index.md` as a reference. Take especially care of noteworthy issues & PRs:

- https://github.com/operaton/operaton/issues?q=is%3Aissue%20state%3Aclosed%20label%3Anoteworthy%20milestone%3A{MILESTONE}
- https://github.com/operaton/operaton/issues?q=is%3Aissue%20state%3Aclosed%20label%3Anoteworthy%20milestone%3A{MILESTONE}

Analyze the changes from https://github.com/operaton/operaton/compare/{LAST_RELEASE_VERSION}...HEAD and document noteworthy changes, also important dependency upgrades. Unimportant are dependencies that are only used in tests.
  Document changes to API, also internal ones. Find the sources at https://github.com/operaton/operaton .
  Add as much details and examples as useful to help users to get the relevant information about the release. 