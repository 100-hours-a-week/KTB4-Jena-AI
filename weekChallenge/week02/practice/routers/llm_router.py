# router/llm_router.py

import httpx
from fastapi import APIRouter
from ollama import chat
from routers import post_router


router = APIRouter()


posts = [
	{"post_id": 1, "user_id": 2, "title": "첫 게시글 작성합니다.", "content": "안녕하세요. 오늘 위클리 챌린지 처음 테스트 해보고 있어요. 너무너무 어렵네요. 이미 일요일까지 과제를 제출했었어야되는데 오늘이 월요일인데도 아직 못했어요. 성공적으로 백엔드 코드 짤 수 있도록 여러분 응원해주세요 ㅠㅠ !!"},
	{"post_id": 2, "user_id": 1, "title": "Second Post", "content": "This is the second post."}
]


## 게시글 LLM 요약
@router.get("/posts/{post_id}/summary")
def summarize_post(post_id: int):
	
	try:
		response = chat(
			model = "gemma4:e2b",
			messages = [
			{"role" : "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
			{"role" : "user", "content": f"다음 게시글 내용을 요약해줘:\n\n{post_router.get_post(post_id)['content']}"}
        	]
		)

		return {"summary" : response.message.content}

	except httpx.HTTPStatusError as exc:
		return {"error" : exc.response.status_code}