# Papertrail backend

FastAPI service for the arXiv finder agent.

## Run locally

```bash
uv sync
uv run dev
```

The service loads the existing `.env` file. It requires a valid
`OPENAI_API_KEY` for agent searches.

Available routes:

- `GET /health` checks whether the API is running.
- `POST /search` accepts `{ "topic": "your research topic" }` and returns a
  `PaperSearchResult`.

To allow additional frontend origins, set a comma-separated value:

```bash
FRONTEND_ORIGINS=http://localhost:3000,https://your-frontend.example
```

## Test

```bash
uv run python -m unittest discover -s tests
```
