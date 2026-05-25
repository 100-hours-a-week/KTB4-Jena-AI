# router/comment_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# 댓글기능

posts = [
	{"post_id": 1, "user_id": 2, "title": "첫 게시글 작성합니다.", "content": "안녕하세요. 오늘 위클리 챌린지 처음 테스트 해보고 있어요. 너무너무 어렵네요. 이미 일요일까지 과제를 제출했었어야되는데 오늘이 월요일인데도 아직 못했어요. 성공적으로 백엔드 코드 짤 수 있도록 여러분 응원해주세요 ㅠㅠ !!"},
	{"post_id": 2, "user_id": 1, "title": "Second Post", "content": "This is the second post."}
]

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
@router.post("/posts/{post_id}/comments", status_code=201)
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
@router.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
	return [c for c in comments if c["post_id"] == post_id] # post_id가 일치하는 댓글만 반환


## 댓글 수정
@router.put("/posts/{post_id}/comments/{comment_id}")
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
@router.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_id: int, comment_id: int):
	for c in comments:
		if (
			c["post_id"] == post_id and
			c["comment_id"] == comment_id
		):
			comments.remove(c) 
			return {"message": "Comment deleted successfully"}
		
	raise HTTPException(status_code=404, detail="Comment not found")

