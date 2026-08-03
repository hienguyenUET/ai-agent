import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from base_models.paper import Paper, PaperSearchResult
from main import app


class SearchApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("main.run_search_agent")
    def test_search_passes_topic_to_agent(self, run_search_agent) -> None:
        run_search_agent.return_value = PaperSearchResult(
            topic="vision-language models",
            papers=[
                Paper(
                    arxiv_id="2501.12345",
                    title="A Relevant Paper",
                    authors=["Ada Researcher"],
                    publication_date="2025-01-15T00:00:00+00:00",
                    abstract="A grounded abstract.",
                    url="https://arxiv.org/abs/2501.12345",
                    pdf_url="https://arxiv.org/pdf/2501.12345",
                )
            ],
        )

        response = self.client.post(
            "/search",
            json={"topic": "  vision-language models  "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["papers"][0]["title"], "A Relevant Paper")
        run_search_agent.assert_called_once_with("vision-language models")

    def test_search_rejects_blank_topic(self) -> None:
        response = self.client.post("/search", json={"topic": "   "})

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
