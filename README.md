# data-processing-app

## backend installation

1. create virtual environment: `python3.11 -m venv .venv`.
2. activate virtual environment: `source .venv/bin/activate` for unix systems and `.venv\Scripts\activate.bat` for Windows cmd-based systems.
3. install dependencies: `pip install -r requirements.txt`.
4. start application through uvicorn server: `uvicorn src.api.main:app --reload --reload-dir src` (optionally remove `--reload` and `--reload-dir` params).
5. check whether application is running successfully by pinging healthcheck endpoint: `curl 127.0.0.1:8000`.
