import json
from random import randint
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Table, BuyIn
from ..users.models import Profile
from .constants import *

class TableConsumer(AsyncWebsocketConsumer):
    message_counter = 0
    message_event = asyncio.Event()
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.round = PREFLOP
    #     self.game_in_process = False

    async def connect(self):
        self.table = await Table.objects.aget(id=self.scope['url_route']['kwargs']['table_id'])
        self.room_group_name = f'table{self.table.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.auth_user_init()

        await self.accept()
        print(self.channel_name, self.auth_user)
        await self.channel_layer.group_send(
            self.room_group_name,
              {
                  'type': 'join',
                  'channel_name': self.channel_name
              }
        )

    async def auth_user_init(self):
        self.auth_user = self.scope['user']
        self.auth_user_stack = (await BuyIn.objects.aget(id=self.table.buy_in_id)).amount
        self.auth_user_image = (await Profile.objects.aget(id=self.auth_user.id)).image.url


    def seating_arrangement(self):
        seats = json.loads(self.table.seats)
        for seat, username in enumerate(seats):
            if username == self.auth_user.username:
                auth_user_seat = seat
        if auth_user_seat == 0:
            self.seats = seats
        else:
            self.seats = [EMPTY for i in seats]
            for seat, username in enumerate(seats):
                self.seats[seat - auth_user_seat] = username
        return self.seats

    async def receive(self, text_data):
        text_data_json = json.loads(text_data) 
        if text_data_json['type'] == 'join':
            print(self.channel_name, self.auth_user)
            self.table = await Table.objects.aget(id=self.scope['url_route']['kwargs']['table_id'])
            await self.channel_layer.send(
            self.channel_name,
                {
                    'type': 'seats_arrangement',
                    'seats': self.seating_arrangement()
                }
            )
            print(type(self).message_counter, self.table.n_players)
            type(self).message_counter += 1
            print(type(self).message_counter, self.table.n_players)
            print(self.auth_user.username, self.table.n_players)
            if type(self).message_counter == self.table.n_players:
                type(self).message_counter = 0
                type(self).message_event.set()
            else:
                await type(self).message_event.wait()
                type(self).message_event.clear()

            player_info = {'type': 'player_info',
                           'username': self.auth_user.username,
                           'stack': self.auth_user_stack,
                           'image': self.auth_user_image,
                          }
            if text_data_json['channel_name'] == self.channel_name:
                await self.channel_layer.group_send(self.room_group_name, player_info)
            else:
                await self.channel_layer.send(self.room_group_name, player_info)

        # action = text_data_json['action']
        # username = text_data_json['username']

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'player_action',
        #         'action': action,
        #         'username': username,
        #     }
        # )


    async def player_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_info',
            'username': event['username'],
            'stack': event['stack'],
            'image': event['image'],
        }))

    async def join(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def seats_arrangement(self, event):
        await self.send(text_data=json.dumps({
            'type': 'seats_arrangement',
            'seats': event['seats'],
        }))

    async def update_seats_arrangement(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update_seats_arrangement',
        }))


    async def player_action(self, event):
        action = event['action']
        username = event['username']
        user = User.objects.get(username=username)

        await self.send(text_data=json.dumps({
            'type': 'player_action',
            'action': action,
            'username': username,
            'image': user.profile.image.url,

        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )    