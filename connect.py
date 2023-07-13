import json
from config import *
import asyncio
import aio_pika
from pika.adapters.asyncio_connection import AsyncioConnection
import aio_pika
from aio_pika import connect
import ast
import time
from main import SupperParserVita
from queue import Queue




async def on_message(body_str, class_main):
    r = ast.literal_eval(body_str)
    #print(r)
    task_id = r['task_id']
    info = [r['id'], r['site'], r['task_id']]
    info_name_site = r['site']
    city = r['main']
    list_urls = list(r['urls'].keys())
    #print(list_urls)
    await class_main.start_parser(city=city, info=info_name_site, list_urls=list_urls, task_id=task_id)


async def rebbitmq_conn_main():
    class_main = SupperParserVita()
    connection = await aio_pika.connect_robust(f'amqp://{mqlogin}:{mqpassword}@{mqhost}/')
    async with connection:
        channel = await connection.channel()
        #await channel.set_qos(prefetch_count=2)
        queue = await channel.declare_queue("vitaexpress")

        while True:
            msg = await queue.get(no_ack=False)
            if msg:
                body_str = msg.body.decode('UTF-8')
                #print(body_str)
                await on_message(body_str, class_main)
            else:
                await asyncio.sleep(20)

asyncio.run(rebbitmq_conn_main())



