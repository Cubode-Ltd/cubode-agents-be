#sys
import os
from dotenv import load_dotenv

#data handling
import pandas as pd
import yaml
from typing import Optional

#LLMs
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

groq_api_key = os.environ.get("GROQ_API")
    
class SuggestedChart(BaseModel):
    main_chart_type: str = Field(description="The suggested type of main category of chart to use")
    sub_chart_type: str = Field(description="The sub chart to use within the main category")
    column1: str = Field(description="The first column that will be plotted in the chart")
    column2: str = Field(description="The second column that will be plotted in the chart")
    column3: Optional[str] = Field(description="The third column that will be plotted in the chart")
    aggregation: str = Field(description="The data aggregation used within the plot")
    chart_title: str = Field(description="Main title of the chart")
    description: str = Field(description="Description of what the chart shows")

class Charts(BaseModel):
        chart_1: SuggestedChart = Field(description="The first chart suggested")
        chart_2: SuggestedChart = Field(description="The second chart suggested")
        chart_3: SuggestedChart = Field(description="The third chart suggested")

class ChartGenerator:
    def __init__(self, csv_file: dict, metadata: dict, model: dict, auto: bool=False):
        """
        Initializes the Chart Generator instance.

        Args:
            data (dict): Information of the data file from the front end
            metadata (dict): The netadata extracted from the uploaded dataset
            model (dict): details about the language model to use. Example:
                    {
                    name: "llama3-70b-8192"
                    provider:  Groq    choices -> [OpenAI, Groq]
                    temperature: 0.0
                    max_tokens: 256
                    }
            auto (bool, optional): Whether to automatically describe the data upon initialization. Defaults to False.
        """
        ## -- Set params -- ##
        #Data
        self.hash = csv_file["hash"]
        self.filename = csv_file["file_name"]
        self.data = metadata

        #LLM
        self.model = model["name"]
        self.temperature = model["temperature"]
        self.provider = model["provider"]
    
        #Prompts
        with open('./ai/prompts.yaml', 'r') as file:
            prompts = yaml.safe_load(file)

        self.base_template = prompts['chart_suggestor']['base']
        self.instructions_template = prompts['chart_suggestor']['instructions']
        self.chart_options_template = prompts["chart_suggestor"]["chart_options"]
        self.input_template = prompts["chart_suggestor"]["new_input"]

        #Load Web Component Templates
        with open('./ai/webcomponents.yaml', 'r') as file:
            webcomponents = yaml.safe_load(file)

        self.wc_templates = webcomponents["web_components"]
        
        if auto:
            self.result = self.create_web_component()

    def create_model(self):

        model = ChatGroq(
            temperature=self.temperature,
            model=self.model,
            api_key= groq_api_key#ENTER YOUR API KEY HERE
        )

        return model
    def create_prompts(self):
         
        self.instructions_template = self.instructions_template.format(chart_options=self.chart_options_template)

        prompt = PromptTemplate(
            template=self.base_template,
            input_variables=["input"],
            partial_variables={
                            "instructions": self.instructions_template},
            )
        return prompt
         
    def create_output_parser(self):
        
        return PydanticOutputParser(pydantic_object=Charts)

    def generate_charts(self):

        prompt = self.create_prompts()
        parser = self.create_output_parser()
        model = self.create_model()

        input = self.input_template.format(schema=self.data['Schema'], data_types=self.data["Data Types"])
        
        chain = self.create_prompts() | self.create_model() | self.create_output_parser()

        node_out = chain.invoke({"input": input, 
                                "format_output_instructions": self.create_output_parser().get_format_instructions()})
        return node_out
    
    def create_web_component(self):
        
        charts = self.generate_charts()

        template = self.wc_templates.get(charts.chart_1.main_chart_type)

        # template = template.format( #aggregation=charts.chart_1.aggregation,
        #                             column_category=charts.chart_1.column1,
        #                             column_values=charts.chart_1.column2,
        #                             title=charts.chart_1.chart_title)
        
        template = template.format(
            hash=self.hash,
            filename=self.filename,
            x_axis_label="x label",
            y_axis_label="y label",
            aggregation="Mean",
            column_category="country",
            column_values="price",
            title="ActualTitle",
            subtitle="Sub title text",
            color_scale="Inferno",
        )

        print("TEMPLATE:    ", template)

        return template