import time
from loguru import logger
def read_sys_prompt(prompt_path):
    with open(prompt_path, "r") as file:
        return {"role":"system","content":file.read()}

def read_human_prompt(prompt_path,**kwargs):
    with open(prompt_path, "r") as file:
        prompt = file.read()
        if kwargs:
            prompt = prompt.format(**kwargs)
        return {"role":"user","content":prompt}
    

def write_netlist(netlist:dict, file_path):
    # 将字符串中的 \n 替换为实际的换行符
    netlist_str = ""
    for key,value in netlist.items():
        netlist_str += f"{value}\n"
    
    # 添加控制命令部分
    control_commands = """
.control
ac dec 30 0.01 1000k
settype decibel out
plot vdb(out) xlimit 0.01 100k ylabel 'smalkl signal gain'
settype phase out
plot cph(out) xlimit 0.01 100k ylabel 'phase (in rad)'
let outd = 180/PI*cph(out)
settype phase outd
plot outd xlimit 0.01 100k ylabel 'phase'
.endc

.end
"""
    
    # 检查网表是否已经包含.end，如果有则在其前添加控制命令
    if ".end" in netlist_str.lower():
        netlist_str = netlist_str.replace(".end", control_commands)
    else:
        # 如果没有.end，直接在末尾添加控制命令
        netlist_str += control_commands
    
    with open(file_path, "w") as file:
        file.write(netlist_str)
    


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 调用被装饰的函数
        end_time = time.time()  # 记录结束时间
        logger.info(f"函数 '{func.__name__}' 的运行时间: {end_time - start_time:.4f} 秒")
        return result  # 返回函数的结果
    return wrapper 