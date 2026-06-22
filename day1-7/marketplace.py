from fastapi import FastAPI, Query

app = FastAPI()


MARKETPLACE_ITEM ={
    1: {
        "Name": "BREAD", "Category": "FOOD", "Price": 1500
    },
    2: {
        "Name": "12 Pro MAx", "Category": "Tech", "Price": 500000
    },
    3: {
        "Name": "Book", "Category": "Education", "Price": 3000
    }
}

@app.get("/")
def home():
    return{
        "MESSAGE": "WELCOME"
    }


@app.get("/status")
def status():
    return{
        "status": "UP and ACTIVE"
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id in MARKETPLACE_ITEM:
        return{
        "YOUR ITEM IS": MARKETPLACE_ITEM[item_id]
    }
    return{
        "status": "error",
        "msg": "Item not found"
    }


@app.get("/items")
def category_search(category: str | None = Query(default=None, min_length=3)):
    if not category:
        return{
            "ALL ITEMS": MARKETPLACE_ITEM
        }
    filtered_res = {}
    for user_id, user_data in MARKETPLACE_ITEM.items():
        if user_data["Category"].lower() == category.lower():
            filtered_res[user_id] = user_data
    
    if filtered_res:
        return{
            "STATUS": "Success",
            "filtered by": category,
            "results": filtered_res
        }
    return {
        "status": "error",
        "message": f"No user found matching category: {category}"
    }