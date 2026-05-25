# router/user_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# 사용자 데이터 관리

users = [
	{"user_id": 1, "name": "Alice", "email": "alice@example.com", "pw": "password1"},
	{"user_id": 2, "name": "Bob", "email": "bob@example.com", "pw": "password2"}
]


## 사용자 생성

class UserCreate(BaseModel):
	name: str
	pw: str
	email: str


@router.post("/users")
def create_user(user: UserCreate):
	user_id = max([u["user_id"] for u in users], default=0) + 1

	users.append({
		"user_id": user_id,
		"name": user.name,
		"email": user.email,
		"pw": user.pw
	})
	return {
		"message": "User created successfully",
		"user_id": user_id
	}



## 사용자 조회/로그인(email,pw 확인)

class UserLogin(BaseModel):
	email: str
	pw: str


@router.post("/users/login")
def get_user(user: UserLogin):
	for u in users:
		if u["email"] == user.email and u["pw"] == user.pw:

			return {
				"message": "Login successful",
				"user_id": u["user_id"]
			}
	raise HTTPException(status_code=404, detail="User not found")

