from fastapi import FastAPI, Request

app = FastAPI()
#RESTFUL Routing
@app.get("/home")
def home(request: Request):
    print(request.headers)
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