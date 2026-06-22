from fastapi import FastAPI, Query

app = FastAPI()

FK_DB_USERS = {
    1: {
        "Username" : "daramz_dev", "role": "Backend", "lvl" : 100
    },
    2: {
        "Username" : "bro_code fan", "role": "frontend", "lvl" : 200
    },
    3: {
        "Username" : "koded_kg", "role": "DevOPs", "lvl" : 300
    },
}

@app.get("/")
def home():
    return {
        "Message" : "Welcome"
    }

@app.get("/user/{user_id}")
def get_user_profile(user_id: int):
    if user_id in FK_DB_USERS:
        return{
            "status": "success",
            "requested_id": user_id,
            "profile_data" : FK_DB_USERS[user_id]
        }
    return{
        "status" : "error",
        "message" : "User doesn't exist"
    }


@app.get("/search/{role}/{lvl}")
def get_user_role_lvl(role: str, lvl: int):
    return{
        "searching_for_role": role,
        "searching for lvl": lvl,
        "msg" :"Success"
    }



@app.get("/users")
def get_user(role: str | None = Query(default=None, min_length=2, max_length=15)):
    if not role:
        return{
            "Status": "Success",
            "result" : FK_DB_USERS
        }
    filtered_results= {}
    for user_id, user_data in FK_DB_USERS.items():
        if user_data["role"].lower() == role.lower():
            filtered_results[user_id] = user_data


    if filtered_results:
        return {
            "Status" : "success",
            "filtered_by": role,
            "results": filtered_results
        }
    return {
        "status": "error",
        "message": f"No user found matching role: {role}"
    }