import yaml
import os
import json 

from groq import Groq
from ai.tools.tools import BarChartTool, ScatterChartTool, LineChartTool, PieChartTool, ToolContext, run_check
groq_api_key = os.environ.get("GROQ_API")

class ChartComponentGenerator():
    def __init__(self, csv_file: dict, metadata: dict, model: dict, auto: bool=False):
        """
        Initializes the Chart Generator instance.

        Args:
            data (dict): Information of the data file from the front end
            metadata (dict): The netadata extracted from the uploaded dataset
            model (dict): details about the language model to use. Example:
                    {
                    name: "llama3-70b-8192"
                    }
            auto (bool, optional): Whether to automatically describe the data upon initialization. Defaults to False.
        """
        ## -- Set params -- ##
        #Data
        self.hash = csv_file["hash"]
        self.filename = csv_file["file_name"]
        self.data = metadata

        #Model
        self.model = model
        #Prompts
        with open('./ai/prompts/prompts.yaml', 'r') as file:
            self.prompts = yaml.safe_load(file)
        #Tool Definitions
        with open('./ai/tools/tool_definitions.json', 'r') as file:
            self.tool_definitions = json.load(file)
        
        #Create Groq Client
        self.client = Groq(api_key=groq_api_key)
        
        if auto:
            self.result = self.generate_components()

    def build_base_prompts(self):
        """Builds the base prompts used for creating messages. These prompts are not dynamic.

        Returns:
            system_prompt(str): System prompt used for the system message
            user_prompt(str): User prompt used for the user message
        """
        system_prompt = self.prompts['prompts']['system']
        user_prompt = self.prompts['prompts']['user']
        user_prompt = user_prompt.format(data_types=self.data['Data Types'], 
                                         sample=self.data['Sample'], unique_categories=self.data['Unique Categories'])
        check_prompt = self.prompts['prompts']['check']['base']
        check_prompt = check_prompt.format(data_types=self.data['Data Types'], 
                                         sample=self.data['Sample'])
        return system_prompt, user_prompt, check_prompt
    
    def build_chart_prompts(self, chart):
        """Builds the user prompt specific to the chart that is to be generated

        Args:
            chart (str): The chart to generate

        Returns:
            str: The dynamic chart formatted prompt
        """

        prompt_chart_base = self.prompts['prompts']['charts']['base']
        prompt_chart_attrs = self.prompts['prompts']['charts'][chart]['attributes']
        prompt_chart_opts = self.prompts['prompts']['charts'][chart]['options']
        prompt_chart_conds = self.prompts['prompts']['conditions'].format(chart_type=chart)

        prompt_chart = prompt_chart_base.format(chart_type=chart, attributes=prompt_chart_attrs, 
                                            options=prompt_chart_opts, conditions = prompt_chart_conds
                                            )
        
        return prompt_chart


    def build_messages(self, system_prompt, user_prompt):
        """Builds the role based messaging system from string prompts for inference LLM

        Args:
            system_prompt (str): System role context
            user_prompt (str): User role context

        Returns:
            list: List of role based messages
        """
        
        messages =[
            {
                "role": "system",
                "content": system_prompt
            },
                        {
                "role": "user",
                "content": user_prompt
            },

        ]

        return messages

    def inference(self, tools, messages):
        """Runs chat inferencing on the groq client

        Args:
            tools (dict): Definitions of tools
            messages (list): List of message objects for LLM context

        Returns:
            response_tool_calls(list): List of tool calls to make
        """
        response_raw = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="required",
            max_tokens=4096
            )
        response_message = response_raw.choices[0].message
        response_tool_calls = response_message.tool_calls

        return response_tool_calls
    
    def run_tool_strategy(self, strategies, name, args):
        """
        Execute a tool strategy based on the given name.

        Args:
            strategies (Dict[str, callable]): A dictionary of available strategies.
            name (str): The name of the strategy to execute.
            args (Dict[str, Any]): Arguments to pass to the strategy.

        Returns:
            Optional[Any]: The result of the strategy execution, or None if no strategy is found.
        """
        strategy = strategies.get(name)
        
        if not strategy:
            print(f"No strategy found for function: {name}")
            return None
        
        context = ToolContext(strategy)
        return context.execute_strategy(
            hash=self.hash,
            filename=self.filename,
            args=args
        )
    def run_check_tool(self, check_prompt, check_tool):
        
        messages = self.build_messages("You are a helpful assistant", check_prompt)
        response_tool_calls = self.inference(check_tool, messages)

        for tool_call in response_tool_calls:
            function_to_call = run_check
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                is_possible=function_args.get("is_possible")
            )
            if not function_response:
                break

        return function_response

    def inference_ai(self):
        
        available_strategies = {
            "create_bar_chart": BarChartTool(),
            "create_line_chart": LineChartTool(),
            "create_scatter_chart": ScatterChartTool(),
            "create_pie_chart": PieChartTool()
        }
        # ['bar', 'line', 'scatter', 'pie']
        charts = ['bar', 'line', 'scatter', 'pie']

        responses = {}

        base_system_prompt, base_user_prompt, base_check_prompt  = self.build_base_prompts()
        chart_check_prompt = self.prompts['prompts']['check']['chart']

        for chart in charts:
            
            # CHECK IF ITS POSSIBLE FOR THE CHART TO BE CREATED
            chart_check_prompt = chart_check_prompt.format(chart_type=chart)
            check_prompt = base_check_prompt + chart_check_prompt
            is_possible = self.run_check_tool(check_prompt, [self.tool_definitions['check']])

            if is_possible:
                
                #GENERATE THE CHART COMPONENT
                tools = [self.tool_definitions[chart]]

                responses[chart] = {}

                prompt_chart = self.build_chart_prompts(chart)

                user_prompt = base_user_prompt + prompt_chart

                messages = self.build_messages(base_system_prompt, user_prompt)

                response_tool_calls = self.inference(tools, messages)

                if response_tool_calls:
                    # Iterate over tool calls and execute the corresponding strategy
                    for i, tool_call in enumerate(response_tool_calls):
                        func_name = tool_call.function.name
                        func_args = json.loads(tool_call.function.arguments)
                        func_out = self.run_tool_strategy(available_strategies, func_name, func_args)
                        responses[chart][f'toolcall{i}_result'] = json.loads(func_out)['response']

        return responses
        
    def generate_components(self):

        result = self.inference_ai()

        first_component = {key: list(sub_dict.values())[0] if sub_dict else None for key, sub_dict in result.items()}
        components = "\n".join(value for value in first_component.values() if value is not None)

        return components
        