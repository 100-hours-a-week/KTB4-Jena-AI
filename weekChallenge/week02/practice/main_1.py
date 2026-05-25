from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


# 사용자 데이터 관리

users = [
	{"user_id": 1, "name": "Alice", "email": "alice@example.com", "pw": "password1"},
	{"user_id": 2, "name": "Bob", "email": "bob@example.com", "pw": "password2"}
]


class UserCreate(BaseModel):
	name: str
	pw: str
	email: str


class UserLogin(BaseModel):
	email: str
	pw: str


## 사용자 생성
@app.post("/users")
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
@app.post("/users/login")
def get_user(user: UserLogin):
	for u in users:
		if u["email"] == user.email and u["pw"] == user.pw:


			return {
				"message": "Login successful",
				"user_id": u["user_id"]
			}
	raise HTTPException(status_code=404, detail="User not found")
	



# 게시글 생성/조회

posts = [
	{"post_id": 1, "user_id": 2, "title": "First Post", "content": "This is the first post."},
	{"post_id": 2, "user_id": 1, "title": "Second Post", "content": "This is the second post."}
]


class PostCreate(BaseModel): # Post 요청
	user_id: int # DB 연결 시 삭제 가능
	title: str = Field(min_length=1, max_length=26)
	content: str = Field(min_length=1)

	# <예외처리 방법>
	# 1. Field(max_length) : FastAPI 자동 검증 
	# 1. class 안에 field_validator() 사용 : BaseModel 검증 유지, msg 커스텀 가능
	# 2. FastAPI의 RequestValidationError 핸들러 덮어쓰기 : 전체 커스텀


class PostResponse(BaseModel): # Post 응답
	post_id: int
	user_id: int
	title: str
	content: str


## 게시글 생성
@app.post("/posts", status_code=201)
def create_post(post: PostCreate):
	
	post_id = max([p["post_id"] for p in posts], default=0) + 1

	new_post = {
		"post_id": post_id,
		"user_id": post.user_id, # DB연결 시 current_user.user_id 로 변경
		"title": post.title,
		"content": post.content
	}
	posts.append(new_post)

	return {
		"message": "Post created successfully", 
		 "post": new_post
	}


## 게시글 조회
@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
	for p in posts:
		if p["post_id"] == post_id:
			return p
		# 현재 DB연결 안되어 있어서 posts 데이터 전체를 for문으로 탐색 후 PostResponse 형태로 반환
		# DB연결 시에는 애초에 필요한 데이터 값(PostResponse 형태)만 가져와서 반환 가능

	raise HTTPException(status_code=404, detail="Post not found")


## 게시글 LLM 요약




# 댓글기능

comments = [
	{"comment_id": 1, "post_id": 1, "user_id": 2, "content": "Great post!"},
	{"comment_id": 2, "post_id": 1, "user_id": 1, "content": "Thanks for sharing."}
] 

class CommentCreate(BaseModel):
	user_id: int
	content: str = Field(min_length=1)

class CommentResponse(BaseModel):
	comment_id: int
	post_id: int
	user_id: int
	content: str

## 댓글 생성
@app.post("/posts/{post_id}/comments", status_code=201)
def create_comment(post_id: int, comment: CommentCreate):

	# 게시글 존재 여부 확인
	for p in posts:
		if p["post_id"] == post_id:
			# comment_id = len(comments) + 1  # 댓글 삭제 시 후 새 댓글 생성 시 comment 아이디 번호 중복 문제 발생 가능
			comment_id = max([c["comment_id"] for c in comments], default=0) + 1

			new_comment = {
				"comment_id": comment_id,
				"post_id": post_id,
				"user_id": comment.user_id,
				"content": comment.content
			}
			comments.append(new_comment)

			return {
				"message": "Comment created successfully",
				"comment": new_comment
			}

	raise HTTPException(status_code=404, detail="Post not found")
	

## 댓글 조회
@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
	return [c for c in comments if c["post_id"] == post_id] # post_id가 일치하는 댓글만 반환


## 댓글 수정
@app.put("/posts/{post_id}/comments/{comment_id}")
def update_comment(post_id: int, comment_id: int, updated_comment: CommentCreate):
	# 댓글 존재 여부 확인
	for c in comments:
		if (
			c["post_id"] == post_id and
			c["comment_id"] == comment_id
		):    
			c["content"] = updated_comment.content    # content 업데이트 
		
			return {"message": "Comment updated successfully", "comment": c}
		
	raise HTTPException(status_code=404, detail="Comment not found")


## 댓글 삭제
@app.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_id: int, comment_id: int):
	for c in comments:
		if (
			c["post_id"] == post_id and
			c["comment_id"] == comment_id
		):
			comments.remove(c) 
			return {"message": "Comment deleted successfully"}
		
	raise HTTPException(status_code=404, detail="Comment not found")






## 게시글 LLM 요약
@app.get("/posts/{post_id}/summary")
def summarize_post(post_id: int):
