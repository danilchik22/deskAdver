from fastapi import FastAPI


app = FastAPI(title="Bulletin board")

adv = [{"id": 1, "text": "sale!"}]


@app.get("/")
def hello(id: int):
    obj = list(filter(lambda item: item.get("id") == id, adv))[0]
    return f'{obj["text"]}'


@app.post("/{id}")
def hello_post(id: int, text: str):
    obj = list(filter(lambda item: item.get("id") == id, adv))[0]
    obj["text"] = text
    return {"status": 200, "data": obj}
