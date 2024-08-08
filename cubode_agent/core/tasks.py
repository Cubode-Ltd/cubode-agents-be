#celery
from celery import shared_task
import os
# Channel send
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#ai
# from ai.chart_generator import ChartGenerator
from ai.main import ChartComponentGenerator

# from langchain_core.prompts import PromptTemplate
# from pydantic import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from langchain_groq import ChatGroq

#data handling
import json

groq_api_key = os.environ.get("GROQ_API")

@shared_task
def generate_web_component(metadata: dict, hash: str, file_name: str):

    #Set models
    models = {
            "llama3_70B_tool_use": "llama3-groq-70b-8192-tool-use-preview",
            "llama3_8B_tool_use": "llama3-groq-8b-8192-tool-use-preview",
            "llama3.1_405B": "llama-3.1-405b-reasoning"
        }
    model = models['llama3_70B_tool_use']

    #Package csv file upload
    csv_file = {
        "hash": hash,
        "file_name": file_name
    }
    #Generate web components
    response = ChartComponentGenerator(csv_file=csv_file, metadata=metadata, 
                            model=model, auto=True)
    
    message = {
    "status": "AI inference Complete", 
    "message": response.result
    }
    
    # Use Channels layer to send the message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'agent_tasks',
        {
            "type": 'agent_message',  # This corresponds to the consumer method to call
            "message": message
        }
        
    )