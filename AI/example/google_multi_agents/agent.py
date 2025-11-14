"""
代理模块：定义天气代理、计算器代理和领导代理
"""
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from .tools import get_weather, calculate, add, subtract, multiply, divide
# 加载环境变量
load_dotenv()


default_model = LiteLlm(model="openai/gpt-4o")

# 1. 天气查询代理
weather_agent = LlmAgent(
    name="weather_agent",
    model=default_model,
    description="专门负责查询城市天气信息的代理，可以提供温度、湿度和天气状况。",
    instruction="""
你是一个专业的天气查询助手。

你的职责：
- 当用户询问天气时，使用 get_weather 工具查询指定城市的天气信息
- 以友好、清晰的方式向用户报告天气情况
- 可以基于天气情况给出简单的建议（如是否需要带伞等）

注意事项：
- 只处理天气相关的查询
- 如果用户没有指定城市，礼貌地询问他们想查询哪个城市的天气
""",
    tools=[get_weather]
)


# 2. 计算器代理
calculator_agent = LlmAgent(
    name="calculator_agent",
    model=default_model,
    description="专门负责数学计算的代理，可以进行加减乘除等基本运算和复杂表达式计算。",
    instruction="""
你是一个专业的计算助手。

你的职责：
- 帮助用户进行数学计算
- 对于简单的加减乘除，可以使用 add、subtract、multiply、divide 函数
- 对于复杂的数学表达式，使用 calculate 函数
- 清晰地向用户展示计算过程和结果

注意事项：
- 只处理数学计算相关的任务
- 确保表达式格式正确再进行计算
- 如果计算出错，友好地向用户解释原因
""",
    tools=[calculate, add, subtract, multiply, divide]
)


# 3. 领导代理（协调其他代理）
root_agent = LlmAgent(
    name="leader_agent",
    model=default_model,
    description="智能助手领导者，负责理解用户需求并协调天气和计算器代理完成任务。",
    instruction="""
你是一个智能助手的协调者和领导者。

你的能力：
- 你可以调用两个专业代理来帮助用户：
  1. weather_agent：查询城市天气信息
  2. calculator_agent：进行数学计算

你的职责：
- 理解用户的问题和需求
- 判断问题类型，将任务委派给合适的代理：
  * 如果是天气相关问题 → 使用 weather_agent
  * 如果是数学计算问题 → 使用 calculator_agent
  * 如果问题同时涉及天气和计算 → 分别调用相应的代理
- 整合代理返回的信息，用清晰、友好的方式回复用户
- 对于不属于天气或计算的一般性问题，可以直接回答

交互原则：
- 保持友好、专业的语气
- 如果用户的问题不清楚，主动询问以澄清需求
- 在调用代理前，简要告知用户你将要做什么
- 汇总结果时，确保信息完整、易懂

示例场景：
用户："上海今天天气怎么样？"
→ 调用 weather_agent 查询上海天气

用户："帮我算一下 25 * 4 + 10"
→ 调用 calculator_agent 进行计算

用户："如果北京今天是 28 度，比昨天高了 5 度，昨天是多少度？"
→ 先调用 weather_agent 确认北京温度，再调用 calculator_agent 计算 28 - 5
""",
    sub_agents=[weather_agent, calculator_agent]
)


# 初始化session和runner
def get_runner():
    """创建并返回runner实例"""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="adk_multi_agent_demo",
        session_service=session_service
    )
    return runner, session_service


def call_agent(query: str, user_id: str = "user_1", session_id: str = "session_1"):
    """
    调用代理处理用户查询

    Args:
        query: 用户查询内容
        user_id: 用户ID
        session_id: 会话ID
    """
    runner, session_service = get_runner()

    # 创建或获取session
    try:
        session_service.get_session(
            app_name="adk_multi_agent_demo",
            user_id=user_id,
            session_id=session_id
        )
    except:
        session_service.create_session(
            app_name="adk_multi_agent_demo",
            user_id=user_id,
            session_id=session_id
        )

    # 创建用户消息
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # 运行agent
    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)

    # 处理返回的事件
    for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 最终答案\n", final_answer, "\n")
            return final_answer


if __name__ == "__main__":
    # 测试示例
    call_agent("今天北京天气怎么样？")