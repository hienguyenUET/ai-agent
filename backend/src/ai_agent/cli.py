import os
import sys
from pathlib import Path

import uvicorn


def dev() -> None:
    """Start the Papertrail API development server."""
    project_root = Path(__file__).resolve().parents[2]
    python_path = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(project_root), python_path) if part
    )
    sys.path.insert(0, str(project_root))

    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "127.0.0.1"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True,
    )
