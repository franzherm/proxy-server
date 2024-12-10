from fastapi import FastAPI, HTTPException, Response, File, UploadFile
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

# Load API key from environment or Kubernetes Secrets
# API_KEY = os.getenv("API_KEY")
TEST_URL = "https://jsonplaceholder.typicode.com/todos/1"
URL = os.environ.get("ARTIFACT_URL", None)  # follows the scheme: https://<server-url>/artifactory/path/to/file/example_file.csv
USER = os.environ.get("USER", None)
API_KEY = os.environ.get("JFROG_API_KEY", None)
FILE_ROOT_PATH = os.environ.get("FILE_ROOT_PATH", None)


@app.get("/")
def fetch_test_file():
    # headers = {"Authorization": f"Bearer {API_KEY}"}
    answer = requests.get(f"{TEST_URL}")
    if answer.status_code != 200:
        raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=answer.content, media_type="application/json")


@app.get("/jfrog")
def fetch_file():
    headers = {"X-JFrog-Art-API": f"{API_KEY}"}
    session = requests.session()
    answer = session.get(f"{URL}", headers=headers, verify=False)
    if answer.status_code != 200:
        raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=answer.content, media_type=answer.headers["content-type"])

@app.get("/file/{filename}")
async def fetch_local_file(filename: str = "default_file.csv"):
    return FileResponse(f"{FILE_ROOT_PATH}/{filename}", media_type='application/octet-stream', filename=filename)

@app.put("/upload")
async def upload_local_file(file: UploadFile):
    try:
        contents = file.file.read()
        with open(f"{FILE_ROOT_PATH}/{file.filename}", 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
