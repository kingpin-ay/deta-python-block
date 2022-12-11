from fastapi import FastAPI



app = FastAPI()


@app.get("/")
def index_page():
    return {"status" : "Welcome .. to the universe of telfund"}


