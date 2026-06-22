from fastapi import FastAPI

app = FastAPI()
#RESTFUL Routing
@app.get("/home")
def home():
    return {
        "Message" : "HELLO WORLD"
    }

@app.get("/about")
def about():
    return {
        "Version": "1.0.01",
        "description" : "Learning",
        "Author": "DARAMZ"
    }

@app.get("/status")
def status():
    return{
        "Status": "up",
        "Health" : "excellent"
    }