# 导入必要的模块
import json
import os
import math

from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger

from utils import read_sys_prompt,read_human_prompt
from config import log_config

load_dotenv()
class CalculationAgent:
    def __init__(self,prompt:dict=None):
        self.messages = []
        if prompt is not None:
            self.messages.append(prompt)
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    
    def get_response_with_tool(self,messages):
        completion = self.client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            # response_format={"type": "json_object"},
            tools=self._tool,
            tool_choice="auto",
        )
        if completion.choices[0].message.content is None:
            completion.choices[0].message.content = ""
        return completion.choices[0].message

    def invoke(self,prompt):
        current_messages = self.messages.copy()
        current_messages.append(prompt)
        logger.trace(prompt)
        
        i = 1
        assistant_message = self.get_response_with_tool(current_messages)
        current_messages.append(assistant_message)
        # 如果工具调用为空，则返回当前消息
        if assistant_message.tool_calls == None:
            logger.trace("No tool call")
            logger.trace(assistant_message)
            return assistant_message.content
        
        # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
        while assistant_message.tool_calls != None:
            logger.trace(assistant_message)
            tool_info = {
                "content": "",
                "role": "tool",
                "tool_call_id": assistant_message.tool_calls[0].id,
            }
            if assistant_message.tool_calls[0].function.name == "calculate_capacitor":
                tool_info["content"] = self.calculate_capacitor(**json.loads(assistant_message.tool_calls[0].function.arguments))
                logger.trace(f"第{i}次工具输出信息:{tool_info['content']}")
                current_messages.append(tool_info)
            assistant_message = self.get_response_with_tool(current_messages)
            current_messages.append(assistant_message)
            i += 1

        logger.trace(current_messages[-1])
        return current_messages[-1].content
        # return self.messages[-1]["content"]
        # print(self.messages[-1].model_dump_json())
        # print(self.messages[-1].content)
    
    def calculate_capacitor(self, name: str, cutoff_frequency: float, R: float):
        C = 1 / (2 * math.pi * cutoff_frequency * R)
        return f"{name}的电容值为{C}F"
    
    
    
    _tool = [
        {
            "type": "function",
            "function": {
                "name": "calculate_capacitor",
                "description": "calculate the capacitance of an RC filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string","description": "the name of the capacitor"},
                        "cutoff_frequency": {"type": "number","description": "the cutoff frequency, unit Hz"},
                        "R": {"type": "number","description": "the resistance, unit Ohm"}
                    },
                    "required": ["name","cutoff_frequency","R"]
                }
            }
        },
    ]

if __name__ == "__main__":
    agent = CalculationAgent(read_sys_prompt("prompt/sys_prompt.txt"))  
    # print(agent.invoke(read_human_prompt("prompt/human_prompt.txt")))
    print(agent.invoke(read_human_prompt("prompt/human_prompt.txt",center_frequency=100,bandwidth=40)))

