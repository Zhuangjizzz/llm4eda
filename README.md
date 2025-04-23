# llm4eda

## Project Overview
This project is designed for the llm4eda class and involves simulating an RC bandpass filter using ngspice. The project utilizes agents to calculate and parse outputs, generating netlists for simulation.

## Setup&Run Instructions
1. **Clone the repository**
   ```bash
   git clone git@github.com:Zhuangjizzz/llm4eda.git
   cd llm4eda
   ```

2. **Install dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file in the root directory and configure necessary environment variables if required.

## Usage
1. **Run the Simulation**
   Execute the main script to start the simulation process:
   ```bash
   python main.py
   ```
   Follow the prompts to input the desired center frequency and bandwidth for the RC bandpass filter.

2. **Simulation Process**
   - The `calculation_process` function uses `CalculationAgent` to compute results based on system and human prompts.
   - The `output_process` function parses the results and generates a netlist using `OutputParserAgent`.
   - The `run_simulation` function executes the ngspice simulation on the generated netlist.

3. **User Interaction**
   After each simulation, you will be prompted to confirm if the results are satisfactory. You can adjust the parameters and rerun the simulation if needed.