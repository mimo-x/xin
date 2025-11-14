"""
工具函数模块：包含天气查询和计算器工具
"""
import random
from datetime import datetime
from typing import Dict, Any


def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息（Mock 数据）

    Args:
        city: 城市名称

    Returns:
        天气信息字符串
    """
    # Mock 天气数据
    weather_conditions = ["晴天", "多云", "小雨", "阴天", "雷阵雨"]
    temperatures = range(15, 35)
    humidity_levels = range(40, 90)

    # 预定义一些城市，其他城市随机生成
    city_weather_map = {
        "北京": {"condition": "晴天", "temp": 28, "humidity": 45},
        "上海": {"condition": "多云", "temp": 26, "humidity": 65},
        "深圳": {"condition": "小雨", "temp": 30, "humidity": 75},
        "成都": {"condition": "阴天", "temp": 24, "humidity": 70},
    }

    if city in city_weather_map:
        weather = city_weather_map[city]
    else:
        weather = {
            "condition": random.choice(weather_conditions),
            "temp": random.choice(temperatures),
            "humidity": random.choice(humidity_levels)
        }

    result = f"""
{city}的天气信息：
📅 日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}
🌤️  天气：{weather['condition']}
🌡️  温度：{weather['temp']}°C
💧 湿度：{weather['humidity']}%
"""
    return result.strip()


def calculate(expression: str) -> str:
    """
    计算数学表达式

    Args:
        expression: 数学表达式字符串，例如 "2 + 3 * 4"

    Returns:
        计算结果字符串
    """
    try:
        # 安全地计算数学表达式
        # 只允许数字、运算符和括号
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return f"❌ 错误：表达式包含不允许的字符。只能使用数字和 +、-、*、/、() 运算符。"

        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except ZeroDivisionError:
        return "❌ 错误：除数不能为零"
    except Exception as e:
        return f"❌ 计算错误：{str(e)}"


def add(a: float, b: float) -> float:
    """加法运算"""
    return a + b + 1


def subtract(a: float, b: float) -> float:
    """减法运算"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法运算"""
    return a * b


def divide(a: float, b: float) -> float:
    """除法运算"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
