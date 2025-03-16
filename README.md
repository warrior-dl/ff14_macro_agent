# FF14宏AI生成器

## 功能
1. 用户输入想生成的宏功能，agent根据要求生成对应宏
2. 支持对生成的宏进行格式校验
3. 支持对话继续修改宏

## 系统架构

```mermaid
graph TD
    A[React前端] -->|API调用| B[FastAPI主服务]
    B --> C[宏生成模块]
    B --> D[校验模块]
    B --> E[对话管理模块]
    C -->|调用LLM| F[OpenAI API]
    C -->|工具调用| G[MCP服务器]
    G --> H[工具注册中心]
    G --> I[规则知识库]
    G --> J[校验服务接口]
    E -->|存储| I[PostgreSQL对话记录]
    
    J[统一日志] -->|文件记录| K[/logs/]
    
    style B fill:#f9d,stroke:#333
    style G fill:#c9f,stroke:#333
```

## 项目结构
```
app/
├── main.py
├── routers/
│   ├── macro.py    # 宏生成路由
│   ├── validate.py # 校验路由
│   └── chat.py     # 对话路由
├── services/
│   ├── llm.py      # LLM交互服务
│   └── mcp_tools.py    # MCP工具交互封装
├── db/
│   ├── models.py   # 数据库模型
│   └── crud.py     # 数据库操作
└── config.py       # 配置管理
```

## 系统需求
1. 网页部署：使用React构建前端界面
2. 核心服务：FastAPI实现RESTful API
3. MCP服务：基于MCP服务器实现LLM工具调用
4. 数据库：PostgreSQL 15+
5. 依赖服务：
   - OpenAI API访问权限
   - MCP核心服务（包含工具管理、知识库、校验服务）

## 开发与部署

### 本地开发
```bash
# 安装依赖
pip install -r app/requirements.txt

# 配置环境变量
echo "OPENAI_API_KEY=您的API密钥" > .env

# 启动后端服务
uvicorn app.main:app --reload

# 前端开发（另开终端）
cd frontend && npm install && npm start
```

### 生产部署
```docker-compose
services:
  main:
    image: fastapi
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    environment:
      - OPENAI_API_KEY=your_api_key
      - MCP_SERVER_URL=http://mcp-core:8000
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - mcp-core

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: macro123
    volumes:
      - pgdata:/var/lib/postgresql/data

  mcp-core:
    image: mcp-core:latest
    environment:
      MCP_TOOL_REGISTRY: /tools/ff14-tools.yaml
      MCP_KNOWLEDGE_DB: postgresql://postgres:macro123@postgres:5432/macrodb
    volumes:
      - ./mcp-tools:/tools

volumes:
  pgdata:
```

### API测试
```bash
# 生成宏示例
curl -X POST "http://localhost:8000/api/macro/generate" \\
  -H "Content-Type: application/json" \\
  -d '{"description": "白魔导士群体治疗宏", "job": "白魔导士", "level": 90}'

# 访问API文档
open http://localhost:8000/docs
```
