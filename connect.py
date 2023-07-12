import json
from config import *
import asyncio
import aio_pika
from pika.adapters.asyncio_connection import AsyncioConnection
import aio_pika
import logging
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from typing import Any
import ast
import time
from main import SupperParserVita

data_info_in_json = []


async def on_message(body_str, class_main):
        r = ast.literal_eval(body_str)
        info = [r['id'], r['site'], r['task_id']]
        # city = r['main']['city']
        # region = r['main']['region']
        city = r['main']
        print(city)

        for main_urls_one in r['urls']:
            all_my_urls = await class_main.start_parser(urlss=main_urls_one, city=city, info=info)

            print(all_my_urls)

        # Добавить эту информацию после прохождения каждого url



async def rebbitmq_conn_main():
    class_main = SupperParserVita()
    connection = await aio_pika.connect_robust(
        f'amqp://{mqlogin}:{mqpassword}@{mqhost}/',
    )
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue("vitaexpress")
        while True:
            msg = await queue.get(no_ack=False)
            if msg:
                body_str = msg.body.decode('UTF-8')
                print(body_str)
                await on_message(body_str, class_main)
            else:
                await asyncio.sleep(10)
        # await queue.consume(on_message, no_ack=False, arguments=[class_main])

        #print(" [*] Waiting for messages. To exit press CTRL+C")
        #await asyncio.Future()


asyncio.run(rebbitmq_conn_main())



