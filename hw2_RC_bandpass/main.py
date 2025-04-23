import os
from agent1 import CalculationAgent
from agent2 import OutputParserAgent
from config import log_config
from utils import read_human_prompt,read_sys_prompt,time_decorator,write_netlist

center_frequency = 100
bandwidth = 40
netlist_file_path = "rc_bandpass.cir"

@time_decorator
def calculation_process():
    sys_prompt = read_sys_prompt("prompt/sys_prompt.txt")
    human_prompt = read_human_prompt("prompt/human_prompt.txt",center_frequency=center_frequency,bandwidth=bandwidth)

    calculation_agent = CalculationAgent(sys_prompt)
    result = calculation_agent.invoke(human_prompt)
    return result

@time_decorator
def output_process(result):
    sys1_prompt = read_sys_prompt("prompt/sys1_prompt.txt")
    output_parser_agent = OutputParserAgent(sys1_prompt)
    netlist = output_parser_agent.invoke({"role":"user","content":result})
    write_netlist(netlist,netlist_file_path)

@time_decorator
def run_simulation():
    print(f"\n正在运行ngspice仿真 {netlist_file_path}...")
    os.system(f"ngspice {netlist_file_path}")
    print("仿真完成！")

if __name__ == "__main__":
    while True:
        # 执行计算过程
        result = calculation_process()
        # 解析输出并生成网表
        output_process(result)
        # 运行仿真
        run_simulation()
        
        # 询问用户是否满意仿真结果
        user_choice = input("\n您对仿真结果满意吗？(y/n): ")
        if user_choice.lower() == 'y':
            print("设计完成！")
            break
        else:
            # 允许用户修改参数
            try:
                new_center = float(input(f"请输入新的中心频率(当前: {center_frequency}): ") or center_frequency)
                new_bandwidth = float(input(f"请输入新的带宽(当前: {bandwidth}): ") or bandwidth)
                center_frequency = new_center
                bandwidth = new_bandwidth
                print(f"参数已更新: 中心频率={center_frequency}, 带宽={bandwidth}")
            except ValueError:
                print("输入无效，使用原参数继续...")