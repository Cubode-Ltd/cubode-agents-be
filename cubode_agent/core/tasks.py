#celery
from celery import shared_task

# Channel send
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def add(args):

    out = args['x'] + args['y']

    message = {
    "status": "web component creation done", 
    "message": out,
    }

    print(message)

    # Use Channels layer to send the message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'agent_tasks',
        {
            "type": 'agent_message',  # This corresponds to the consumer method to call
            "message": message
        }
    )

    
