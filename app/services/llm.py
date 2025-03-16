import openai
from ..config import settings
from typing import Optional

openai.api_key = settings.openai_api_key

async def generate_macro(description: str, job: str, level: int) -> str:
    prompt = f"""根据FF14游戏规则为{job}(等级{level})生成战斗宏：
需求描述：{description}

要求：
1. 符合该职业的技能循环逻辑
2. 包含必要的注释说明
3. 使用标准的宏命令格式
4. 包含条件判断语句（如/ac "技能" <条件>）

请用中文输出，使用<wait>进行技能间隔控制"""
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一个专业的FF14游戏宏生成专家"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message['content']
