from fastapi import FastAPI, HTTPException
from pydantic import BaseModel








class PostCreate(BaseModel): # Post 요청
	title: str
	content: str


class PostResponse(BaseModel): # Post 응답
	post_id: int
	user_id: int
	title: str
	content: str


# 게시글 생성
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, session: Session):

	new_post = PostTable(
		user_id = current_user.user_id,
		title = post.title,
		content = post.content,
	)
	
	database.add(new_post) # DB에 추가
	database.commit() # DB에 반영
	database.refresh(new_post) # 새로 생성된 게시글의 post_id를 가져오기 위해 새로고침

	return {
		"message": "Post created successfully", 
		 "post": new_post
	}


# 게시글 조회
@app.get("/posts/{post_id}")
def get_post(post_id: int, data: SessionDep):
	for p in posts:
		if p.post_id == post_id:
			return p
		
	raise HTTPException(status_code=404, detail="Post not found")