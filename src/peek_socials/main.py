from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def healthCheck():
    return {"message": "The backend servers are healthy"}