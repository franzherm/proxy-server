from fastapi import FastAPI, HTTPException, Response
import requests
import os

app = FastAPI()

# Load API key from environment or Kubernetes Secrets
#API_KEY = os.getenv("API_KEY")
BASE_URL = "https://jsonplaceholder.typicode.com/todos/1"

@app.get("/")
def fetch_file():
    #headers = {"Authorization": f"Bearer {API_KEY}"}
    #answer = requests.get(f"{BASE_URL}")#, headers=headers)
    json_str = '{ \
    "userId": 1, \
    "id": 1, \
    "title": "delectus aut autem", \
    "completed": false \
    }'
    #if answer.status_code != 200:
    #    raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=json_str, media_type="application/json")

@app.get("/file")
def fetch_file():
    #headers = {"Authorization": f"Bearer {API_KEY}"}
    #answer = requests.get(f"{BASE_URL}")#, headers=headers)
    json_str = '{ \
    "userId": 1, \
    "id": 2, \
    "title": "delectus aut autem", \
    "completed": false \
    }'
    #if answer.status_code != 200:
    #    raise HTTPException(status_code=answer.status_code, detail="Error fetching file")

    return Response(content=json_str, media_type="application/json")

