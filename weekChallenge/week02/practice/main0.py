from fastapi import FastAPI
from routers import user_router, post_router, comment_router, llm_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(llm_router.router)
