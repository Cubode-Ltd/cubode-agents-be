#celery
from celery import shared_task
import os
# Channel send
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#ai
from ai.chart_generator import ChartGenerator
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

#data handling
import json

groq_api_key = os.environ.get("GROQ_API")

@shared_task
def generate_web_component(metadata: dict):

    model = {
            "name": "llama3-70b-8192",
            "provider":  "Groq",
            "temperature": 0.0
     }

    charts = ChartGenerator(metadata=metadata, 
                   model=model, auto=True)
    
    message = {
    "status": "AI inference Complete", 
    "message": charts.result
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