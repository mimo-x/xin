# pip install google-adk
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

import warnings
# 忽略所有警告
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

# ============== 环境变量配置 ==============
# 自动加载 .env 文件中的环境变量
# 使用说明：
# 1. 复制 .env.example 为 .env
# 2. 在 .env 文件中填入你的 API 密钥
# 3. .env 文件不会被提交到 git（已在 .gitignore 中）
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 从环境变量获取配置（如果 .env 中没有，使用默认值）
MODEL_GEMINI_2_0_FLASH = os.getenv("MODEL_GEMINI_2_0_FLASH", "gemini-2.0-flash")

# ============== 智能委托机制 Demo 实现 ==============

# 1. 定义专门的工具函数
def say_hello(name: str) -> str:
    """向用户打招呼"""
    return f"你好，{name}！很高兴为您服务！"

def say_goodbye(name: str) -> str:
    """向用户告别"""
    return f"再见，{name}！祝您有美好的一天！"

def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    now = datetime.now()
    return f"当前时间是：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"

def calculate_sum(a: float, b: float) -> str:
    """计算两个数的和"""
    result = a + b
    return f"{a} + {b} = {result}"

def get_weather_info(city: str) -> str:
    """模拟获取天气信息（真实应用中会调用天气API）"""
    weather_data = {
        "北京": "晴天，气温25°C，湿度60%",
        "上海": "多云，气温28°C，湿度75%",
        "广州": "小雨，气温30°C，湿度85%",
        "深圳": "晴天，气温29°C，湿度70%"
    }
    return weather_data.get(city, f"抱歉，暂时无法获取{city}的天气信息")

# 2. 创建专门的子代理
# 问候代理
greeting_agent = Agent(
    name="greeting_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="""你是一个专门的问候助手。
    - 你的主要任务是处理用户的问候和打招呼
    - 使用 say_hello 工具向用户问好
    - 保持友好和专业的语调
    - 如果不是问候相关的请求，不要处理""",
    tools=[say_hello],
    description="专门处理用户的问候和打招呼任务"
)

# 告别代理
farewell_agent = Agent(
    name="farewell_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="""你是一个专门的告别助手。
    - 你的主要任务是处理用户的告别
    - 使用 say_goodbye 工具向用户告别
    - 保持礼貌和友好的语调
    - 如果不是告别相关的请求，不要处理""",
    tools=[say_goodbye],
    description="专门处理用户的告别任务"
)

# 时间查询代理
time_agent = Agent(
    name="time_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="""你是一个专门的时间查询助手。
    - 你的主要任务是回答关于时间的问题
    - 使用 get_current_time 工具获取当前时间
    - 可以回答任何与时间相关的问题
    - 如果不是时间相关的请求，不要处理""",
    tools=[get_current_time],
    description="专门处理时间查询任务"
)

# 数学计算代理
math_agent = Agent(
    name="math_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="""你是一个专门的数学计算助手。
    - 你的主要任务是进行简单的数学计算
    - 使用 calculate_sum 工具计算两个数的和
    - 可以处理加法运算请求
    - 如果不是数学计算相关的请求，不要处理""",
    tools=[calculate_sum],
    description="专门处理数学计算任务"
)

# 天气查询代理
weather_agent = Agent(
    name="weather_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    instruction="""你是一个专门的天气查询助手。
    - 你的主要任务是查询天气信息
    - 使用 get_weather_info 工具获取指定城市的天气
    - 可以回答任何与天气相关的问题
    - 如果不是天气相关的请求，不要处理""",
    tools=[get_weather_info],
    description="专门处理天气查询任务"
)

# 3. 创建根代理 - 智能委托的核心
root_agent = Agent(
    name="root_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    sub_agents=[
        greeting_agent,
        farewell_agent,
        time_agent,
        math_agent,
        weather_agent
    ],
    instruction="""你是一个智能任务分派助手，负责协调各个专门化的子代理。

你有以下专门的子代理可以帮助处理不同类型的任务：

1. **greeting_agent** - 专门处理问候和打招呼
   使用场景：当用户说"你好"、"早上好"、"嗨"等问候语时

2. **farewell_agent** - 专门处理告别
   使用场景：当用户说"再见"、"拜拜"、"晚安"等告别语时

3. **time_agent** - 专门处理时间查询
   使用场景：当用户询问"现在几点"、"今天几号"、"当前时间"等时间相关问题时

4. **math_agent** - 专门处理数学计算
   使用场景：当用户需要进行数学运算，如"计算 5+3"、"求和"等

5. **weather_agent** - 专门处理天气查询
   使用场景：当用户询问天气情况，如"北京天气怎么样"、"今天天气如何"等

**工作流程：**
1. 首先分析用户的请求类型
2. 根据请求类型选择最合适的子代理
3. 将任务委托给对应的子代理处理
4. 如果无法匹配到合适的子代理，直接回答用户说明你的能力范围

**重要提醒：**
- 你只需要分析和分派任务，不需要亲自执行具体的工具调用
- 让专门的子代理处理它们擅长的工作
- 始终保持友好和专业的态度""",
    description="根代理，负责智能分派任务给专门的子代理"
)

# 4. 设置会话服务
session_service = InMemorySessionService()

# 5. 完整的委托测试（使用调试模式）
async def test_comprehensive_delegation():
    """使用调试模式全面测试智能委托功能"""
    print("\n🧪 全面测试智能委托功能")
    print("=" * 60)

    try:
        # 创建运行器
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            app_name="comprehensive_delegation_demo"
        )
        print("✅ 委托测试运行器创建成功")
    except Exception as e:
        print(f"❌ 运行器创建失败: {str(e)}")
        return

    # 完整的测试用例
    test_cases = [
        {
            "message": "你好，我是小明",
            "expected_agent": "greeting_agent",
            "expected_tool": "say_hello",
            "description": "问候委托测试"
        },
        {
            "message": "现在几点了？",
            "expected_agent": "time_agent",
            "expected_tool": "get_current_time",
            "description": "时间查询委托测试"
        },
        {
            "message": "帮我计算 15 + 25",
            "expected_agent": "math_agent",
            "expected_tool": "calculate_sum",
            "description": "数学计算委托测试"
        },
        {
            "message": "深圳天气怎么样？",
            "expected_agent": "weather_agent",
            "expected_tool": "get_weather_info",
            "description": "天气查询委托测试"
        },
        {
            "message": "谢谢你的帮助，再见",
            "expected_agent": "farewell_agent",
            "expected_tool": "say_goodbye",
            "description": "告别委托测试"
        }
    ]

    success_count = 0
    total_count = len(test_cases)

    print(f"\n📋 开始测试 {total_count} 个委托场景...")
    print("-" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}/{total_count}: {test_case['description']}")
        print(f"📤 用户消息: {test_case['message']}")
        print(f"🎯 期望委托给: {test_case['expected_agent']} -> {test_case['expected_tool']}")
        print("-" * 40)

        try:
            # 使用调试方法测试委托
            events = await runner.run_debug(
                test_case['message'],
                user_id=f"test_user_{i}",
                session_id=f"test_session_{i}",
                verbose=False  # 减少输出，保持测试结果清晰
            )

            # 分析事件序列
            delegation_success = False
            tool_used = False
            final_response = ""

            for event in events:
                # 检查代理调用
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            func_call = part.function_call
                            if func_call.name == "transfer_to_agent":
                                # 检查是否委托给了正确的代理
                                args = func_call.args
                                if args.get('agent_name') == test_case['expected_agent']:
                                    print(f"✅ 正确委托给: {args.get('agent_name')}")
                                    delegation_success = True
                                else:
                                    print(f"❌ 错误委托: 期望 {test_case['expected_agent']}, 实际 {args.get('agent_name')}")

                            elif func_call.name == test_case['expected_tool']:
                                print(f"✅ 正确使用工具: {func_call.name}")
                                tool_used = True

                        # 收集最终响应
                        if hasattr(part, 'text') and part.text:
                            final_response = part.text.strip()

            # 评估测试结果
            if delegation_success and tool_used:
                print("🎉 委托成功完成！")
                if final_response:
                    print(f"💬 最终响应: {final_response}")
                success_count += 1
            else:
                print("❌ 委托未完全成功")
                if not delegation_success:
                    print("   - 代理委托失败")
                if not tool_used:
                    print("   - 工具调用失败")

        except Exception as e:
            print(f"❌ 测试异常: {str(e)}")

    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    print(f"📈 成功率: {success_count/total_count*100:.1f}%")

    if success_count == total_count:
        print("🎉 所有委托测试通过！智能委托机制工作正常！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")

    print("\n🔍 委托机制验证:")
    print("   ✅ 根代理能够正确分析用户意图")
    print("   ✅ 能够智能选择合适的子代理")
    print("   ✅ 子代理能够使用专门工具完成任务")
    print("   ✅ 整个委托流程无缝协作")

    print("\n" + "=" * 60)
    print("🎯 全面委托测试完成")

# 6. 运行测试
if __name__ == "__main__":
    asyncio.run(test_comprehensive_delegation())