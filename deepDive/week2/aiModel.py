# AI server 구조
# 사용자 > FastAPI > Pydantic 검증 > AI 모델 추론 > 응답
# Pydantic 검증 : 타입, 필수값, 범위, 길이, 형식 등 검증 추가해서 모델 실행되기 전에 막는다!!

# AI 모델을 실행하기 전에 입력값을 “검증”해서
# 이상한 데이터가 모델까지 들어가지 못하게 막는다 !!! 
# (모델 실행되기 전에 오류 잡아야해 !!)


# 이미지 분류 예시
def predict(age, text):
    ...

# 검증이 없을 때
@app.post("/predict")
def predict_api(data: dict):

    result = model.predict(
        data["age"]
    )

    return result

# {"age":"강아지"} 요청이 오면 
# dict 생성 > model.predict("강아지") 로 값을 일단 받은 후 
# '모델 실행 중'에 오류 발생함.(검증이 없기 때문에)


# pydantic 모델로 검증
from pydantic import BaseModel

class PredictRequest(BaseModel):
    age: int

@app.post("/predict")
def predict_api(request: PredictRequest): # request객체 생성(PredictRequest 모델로 검증이 완료된 상태)

    return model.predict(
        request.age
    )

# {"age":"강아지"} 요청이 오면,
# JSON > pydantic 검증 : request = PredictRequest(**body) 넣음 
# FastAPI 단계(모델 실행 전)에서 자동으로 422 에러 반환.(함수 자체를 실행 안함)



# 추가 검증 방법

## 1. 범위제한
from pydantic import Field

class PredictRequest(BaseModel):
    age: int = Field(ge=0,le=120) # 0 ~ 120 사이의 값만 허용



## 2. 문자열 길이 제한
class PromptRequest(BaseModel):

    prompt: str = Field(
        min_length=1,
        max_length=500
    )


## 3. Enum 제한(모델 종류 제한)
from enum import Enum

class ModelType(
    str,
    Enum
):

    gpt="gpt"
    vision="vision"

class Request(BaseModel):
    model: ModelType



## 4. 리스트 크기 제한(대량 요청 방지)
class Request(BaseModel):
    items: list[int]

Field(max_length=100)



## 5. 중첩 데이터 검증
class User(BaseModel):
    age:int


class PredictRequest(BaseModel):
    user: User

# { "user":{"age":"abc"}} >> 자동 차단