# router/post_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter()


# 게시글 생성/조회

posts = [
	{"post_id": 1, "user_id": 2, "title": "첫 게시글 작성합니다.", "content": "안녕하세요. 오늘 위클리 챌린지 처음 테스트 해보고 있어요. 너무너무 어렵네요. 이미 일요일까지 과제를 제출했었어야되는데 오늘이 월요일인데도 아직 못했어요. 성공적으로 백엔드 코드 짤 수 있도록 여러분 응원해주세요 ㅠㅠ !!"},
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
@router.post("/posts", status_code=201)
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
@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
	for p in posts:
		if p["post_id"] == post_id:
			return p
		# 현재 DB연결 안되어 있어서 posts 데이터 전체를 for문으로 탐색 후 PostResponse 형태로 반환
		# DB연결 시에는 애초에 필요한 데이터 값(PostResponse 형태)만 가져와서 반환 가능

	raise HTTPException(status_code=404, detail="Post not found")
