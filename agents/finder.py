from langchain.agents import create_agent
from base_models.paper import PaperSearchResult
from tools.search_arxiv import search_arxiv
from dotenv import load_dotenv

load_dotenv()

FINDER_PROMPT = """
You are a helpful assistant that finds relevant papers based on user input.

Rules:
    1. If the user asks for a specific topic, search for papers that must be related to that topic.
    2. Use search_arxiv to search for papers on arxiv.
    3. Return only list of papers that is provided by search tool.
    4. Invent or make up about titles, abstracts, arxiv ids, and url-related fields are not allowed.
    5. Rank papers based on relevance to the user's query.
    6. Explain why you are returning those papers.
"""

finder_agent = create_agent(
    model = "gpt-4o",
    tools=[
        search_arxiv
        ],
    response_format=PaperSearchResult,
    system_prompt = FINDER_PROMPT
)

if __name__ == "__main__":
    query = "Embedding models for images"
    result = finder_agent.invoke({
        "messages":[
            {"role": "user", "content": query}
        ]
    })
    structured_result = result["structured_response"]

    print(structured_result)
