from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    print("hello world")