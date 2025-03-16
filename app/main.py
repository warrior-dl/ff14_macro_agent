from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import macro, validate, chat
from app.config import settings

app = FastAPI()

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(macro.router, prefix="/api/macro", tags=["宏生成"])
app.include_router(validate.router, prefix="/api/validate", tags=["校验"])
app.include_router(chat.router, prefix="/api/chat", tags=["对话"])

@app.get("/")
def read_root():
    return {"status": "FF14宏生成服务运行中"}
