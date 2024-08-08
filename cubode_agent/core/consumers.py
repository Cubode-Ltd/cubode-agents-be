import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import asyncio
from datetime import datetime
from django.template.loader import get_template
from django.utils.html import format_html

from django.template import Context, Template


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.channel_name)
        await self.accept()
        await self.channel_layer.group_add("agent_tasks", self.channel_name) # Add to group to send messages later

    async def disconnect(self, close_code):
        pass

    async def agent_message(self, event):
        
        message = event['message']['message']
        html = self.render_html(message)
        
        await self.send(text_data=html)

    def render_html(self, new_message):
        template_string = """
        <cb-container id="dynamic-content-ws" hx-swap-oob="outerHTML">
            {{ new_message|safe }}
        </cb-container>
        """
        template = Template(template_string)
        context = Context({"new_message": new_message})
        return template.render(context)
