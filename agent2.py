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
class OutputParserAgent:
    def __init__(self,prompt:dict=None):
        self.messages = []
        if prompt is not None:
            self.messages.append(prompt)
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    def get_response(self,messages):
        completion = self.client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            response_format={"type": "json_object"},
            # tools=self._tool,
        )
        if completion.choices[0].message.content is None:
            completion.choices[0].message.content = ""
        return completion.choices[0].message
    

    def invoke(self,prompt):
        current_messages = self.messages.copy()
        current_messages.append(prompt)
        logger.trace(prompt)
        
        assistant_message = self.get_response(current_messages)
        logger.trace(assistant_message.content)
        return json.loads(assistant_message.content)


if __name__ == "__main__":
    agent = OutputParserAgent(read_sys_prompt("prompt/sys1_prompt.txt"))  
    # print(agent.invoke(read_human_prompt("prompt/human_prompt.txt")))
    print(agent.invoke({"role":"user","content":"""
根据计算，我们得到了用于RC高通滤波器的电容 \(C_{high}\) 为约 198.94 nF 和用于RC低通滤波器的电容 \(C_{low}\) 为约 132.63 nF。现在我们可以将这些值代入到网表中以构建完整的无源RC带通滤波器。

下面是结合了上述参数后的完整SPICE网表：

```spice
* RC High Pass Filter
Vinput in 0 AC 1
C_high in out 198.94nF
R_high out 0 1k

* RC Low Pass Filter
X_lowpass out 0 R_low C_low
.model R_low RES (R=1k)
.model C_low CAP (C=132.63nF)

* Analysis
.ac dec 100 100 10k
.print ac v(out)
.end
```

请注意，在这个网表里，我使用了子电路 `.model` 来定义低通滤波器中的电阻和电容，这是因为直接在连接中指定元件值可能会导致格式上的不一致。然而，为了更清晰地表示级联结构，下面是一种更直观的方式，不使用子电路模型：

```spice
* RC High Pass Filter
Vinput in 0 AC 1
C_high in high_pass_out 198.94nF
R_high high_pass_out 0 1k

* RC Low Pass Filter
R_low high_pass_out low_pass_out 1k
C_low low_pass_out 0 132.63nF

* AC analysis
.ac dec 100 100 10k
.print ac v(low_pass_out)
.end
```

在这段代码中，`in` 是输入节点，`high_pass_out` 是高通滤波器的输出同时也是低通滤波器的输入，而 `low_pass_out` 则是最终带通滤波器的输出。AC分析部分设置为从100Hz到10kHz进行100点对数扫描，这应该能很好地展示所设计的带通滤波器特性。
    """}))

