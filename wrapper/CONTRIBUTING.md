# Contribution guide

## Commits conventions

The versioning scheme we use is SemVer. Below is a summary of it.

- Bug fixes: a commit of the type `fix` patches a bug in your codebase.
- Features: a commit of the type `feat` or `wip` introduces a new feature to the codebase.
- Configurations: `chore`, `build`, and `ci` should be used when updating grunt tasks; no production code change.
- Other types: `docs`, `refactor`, `test`

### Commit message with breaking changes

`refactor!: drop support for Node 10`

### Helpful Resources:

- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Branches conventions

Start the branch name with `feature-` or `bugfix-` to indicate the type of change. For example, `feature-add-pedestrians`.
