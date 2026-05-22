
# pydantic 모델
from pydantic import BaseModel
# BasEModel : pydantic 모델의 기본 클래스, 상속해서 사용
# 데이터 검증(타입검사, 필수값검사) + 객체 생성 + JSON 변환 + 문서생성 기능

# pydantic 모델 정의
class Post(BaseModel):
    title: str
    content: str
    message: str

# FastAPI 사용
from fastapi import FastAPI

app = FastAPI()

@app.post("/posts")
def create_post(post: Post):
    print(post.title) # 객체 생성이 완료됐기 때문에 post.00000 가능 
    return post





# -----
# 그냥 FastAPI 만 사용
@router.get("/posts/{post_id}") # path parameter(경로 파라미터) 검증
def get_post(post_id: int):
    return {"post_id": post_id}

# >> fastapi 장점 : int 값 아닐때 자동으로 422 에러 보냄
# >> get은 보통 body가 없어서, type hint 만으로도 구조 검사 OK


# ----
# FastAPI만 사용했을 때 단점 - Body(JSON) 구조 검사 안함 
@app.post("/posts")
def create_post(data: dict):
    return data
{
 "title":123 # 문자열 아닌 숫자도 다 가져와버림
}


