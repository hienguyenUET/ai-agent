# Papertrail

Papertrail is a research-paper finder with a LangChain agent backend and a
React frontend. A user enters a topic, the finder agent searches arXiv, and the
ranked papers are displayed in the browser.

## Start the backend

```bash
cd backend
uv sync
uv run dev
```

The backend expects `OPENAI_API_KEY` in `backend/.env`. Its health endpoint is
available at `http://localhost:8000/health`.

## Start the frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`, enter a research topic, and select **Search
papers**. The frontend sends the topic to the backend's `POST /search` route.

See `backend/README.md` and `frontend/README.md` for configuration details.
