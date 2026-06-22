from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "HEllo World"}


@app.get("/about")
def about():
    return {"info" : "name is dramz"}

@app.get("/status")
def status():
    return {"STATUS": "alright"}