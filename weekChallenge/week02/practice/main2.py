from fastapi import FastAPI, HTTPException

app = FastAPI()

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# 사용자 조회
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"data" : user, "message": "User retrieved successfully"}


# 사용자 생성 (201 Created 명시)
@app.post("/users", status_code=201)
def create_user(data: dict):
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    if any(u["email"] == email for u in users):
        raise HTTPException(status_code=400, detail="email_already_exists")
  
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email
    }
    users.append(new_user)
    return {"data": new_user, "message": "User created successfully"}


# 로그인
@app.post("/login")
def login(data: dict):
    email = data.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": {"user_id": user["id"], "name": user["name"]}, "message": "Login successful"}