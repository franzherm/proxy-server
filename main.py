from fastapi import FastAPI, HTTPException, Response
import requests
import os

app = FastAPI()

# Load API key from environment or Kubernetes Secrets
# API_KEY = os.getenv("API_KEY")
TEST_URL = "https://jsonplaceholder.typicode.com/todos/1"
URL = os.environ.get("ARTIFACT_URL", None)  # follows the scheme: https://<server-url>/artifactory/path/to/file/example_file.csv
API_KEY = os.environ.get("JFROG_API_KEY", None)


@app.get("/")
def fetch_test_file():
    # headers = {"Authorization": f"Bearer {API_KEY}"}
    answer = requests.get(f"{TEST_URL}")
    if answer.status_code != 200:
        raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=answer.content, media_type="application/json")


@app.get("/file")
def fetch_file():
    headers = {"X-JFrog-Art-API": f"{API_KEY}"}
    answer = requests.get(f"{URL}", headers=headers)
    if answer.status_code != 200:
        raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=answer.content, media_type=answer.headers["content-type"])
