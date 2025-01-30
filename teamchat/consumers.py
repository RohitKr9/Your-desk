import json 
from channels.consumer import AsyncConsumer

class OneToOneConsumer(AsyncConsumer):

    async def connect(self):
        curr_user = self.scope['user']
        curr_user_id = curr_user['id']
        url = self.scope['path']
        other_user_id = url.strip('/').split('/')[-1]
        curr_user = int(curr_user)
        other_user_id = int(other_user_id)
        self.room_name = f"{min(curr_user_id, other_user_id)}-{max(curr_user, other_user_id)}"
        self.group_name =  self.room_name

        await self.channel_layer.group_add(self.room_name, self.group_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_name, self.group_name)

    async def receive(self, text_msg):
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close(code = 4001)

        text_msg_dict = json.loads(text_msg)
        message = text_msg_dict["message"]

        await self.channel_layer.group_send(
            self.group_name,{
                "type":"chat.message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(
            text_data = json.dumps(message)
        )
