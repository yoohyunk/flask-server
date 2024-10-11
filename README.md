# Flask Server

## Installation
- **SKIP** if you already have `poetry` - Set up `pipx` and `poetry`
    - `brew install pipx && pipx ensurepath && pipx install poetry`
- `poetry install`

## Development

We use `poe` as a task runner and `poetry` as a dependency manager.

- start dev server: `poe dev`
- run pytest: `poe test`