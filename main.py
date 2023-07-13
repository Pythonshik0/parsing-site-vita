import datetime
import json
import asyncio
import time
import ast
import asyncpg
from playwright.async_api import async_playwright
from connect import *
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
data_1 = []
save_dbeaver = []


class SupperParserVita():
    l = 0
    page = None

    async def save_in_dbeaver(self, save_dbeaver):
        connection = await asyncpg.connect(host=DB_HOST, user=DB_USER, database=DB_NAME, password=DB_PASSWORD)
        rep = r"\'"
        for save in save_dbeaver:
            command = f'''INSERT INTO products (
                                    pharm,
                                    region,
                                    city,
                                    product_name,
                                    pharm_address,
                                    product_price,
                                    product_count,
                                    product_use_befory,
                                    task_id) VALUES(
                                    '{save['site']}',
                                    '{save['region']}',
                                    '{save['city']}',
                                    E'{save['name'].replace("'", rep)}',
                                    '{save['apteka']}',
                                    '{save['price']}',
                                    '{save['count']}',
                                    '{save['dataGodn']}',
                                    '{save['task_id']}'
                                    );'''

            # star = datetime.datetime.now()
            await connection.execute(command)

        # print(datetime.datetime.now() - star)
        # star = datetime.datetime.now()
        await connection.close()

    async def making_a_request(self, info, city, task_id):
        try:
            while len(self.urls) != 0:
                url = self.urls.pop()
                s = datetime.datetime.now()
                address = []
                js = f'''() => {{return fetch("https://vitaexpress.ru{url}").then(response => {{return response.text();}})}}'''
                #print(js)
                a = await self.page.evaluate(js)
                e = a.split(r'"products": [')[1].split(r']')[0]
                res = json.loads(e)

                g_id = res['id']
                print(url)

                if res['name'] != None:
                    js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                    main_address = await self.page.evaluate(js_city)

                    for i in main_address['TODAY_RESULT']['RESULT']:
                        #main_address_g = i['address']
                        main_name_g = f"{i['name']}, {i['address']}"
                        #print(main_name_g)
                        #address.append(main_address_g)
                        address.append(main_name_g)

                    name = res['name']
                    price = res['price']
                    print(info)
                    print(f"It's passing now url = {url} in {city['region']}{city['city']} , id={g_id} , name={name}, price={price}")
                    for separate_address in address:

                        save_dbeaver.append(
                            {'site': info,
                            'region': city['region'],
                            'city': city['city'],
                            'name': name,
                            'apteka': separate_address,
                            'price': price,
                            'count': '-',
                            'dataGodn': '',
                            'task_id': 555}
                                           )

                    print(save_dbeaver)
                else:
                    if '_' in url:
                        urlss = url.replace('_', '-')

                        js = f'''() => {{return fetch("{urlss}").then(response => {{return response.text();}})}}'''
                        a = await self.page.evaluate(js)
                        e = a.split(r'"products": [')[1].split(r']')[0]
                        res = json.loads(e)
                        g_id = res['id']
                        js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                        main_address = await self.page.evaluate(js_city)

                        for i in main_address['TODAY_RESULT']['RESULT']:
                            main_address_g = i['address']
                            main_name_g = i['name']
                            address.append(main_address_g)
                            address.append(main_name_g)

                        name = res['name']
                        price = res['price']
                        g_id = res['id']
                        print(f"It's passing now url = {urlss} in {city['region']}{city['city']} , id={g_id} , name={name}, price={price}")
                        for separate_address in address:
                            save_dbeaver.append(
                                {'site': info,
                                 'region': city['region'],
                                 'city': city['city'],
                                 'name': name,
                                 'apteka': separate_address,
                                 'price': price,
                                 'count': '-',
                                 'dataGodn': '',
                                 'task_id': 555}
                            )

                        print(save_dbeaver)

                    elif '-' in url:
                        urlss = url.replace('-', '_')

                        js = f'''() => {{return fetch("{urlss}").then(response => {{return response.text();}})}}'''
                        a = await self.page.evaluate(js)
                        e = a.split(r'"products": [')[1].split(r']')[0]
                        res = json.loads(e)
                        g_id = res['id']
                        js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                        main_address = await self.page.evaluate(js_city)
                        #print(main_address)
                        for i in main_address['TODAY_RESULT']['RESULT']:
                            main_address_g = i['address']
                            main_name_g = i['name']
                            address.append(main_address_g)
                            address.append(main_name_g)

                        name = res['name']
                        price = res['price']
                        g_id = res['id']
                        print(f"It's passing now url = {urlss} in {city['region']}{city['city']} , id={g_id} , name={name}, price={price}")
                        for separate_address in address:
                            save_dbeaver.append(
                                {'site': info,
                                 'region': city['region'],
                                 'city': city['city'],
                                 'name': name,
                                 'apteka': separate_address,
                                 'price': price,
                                 'count': '-',
                                 'dataGodn': '',
                                 'task_id': 555}
                            )

                        print(save_dbeaver)

                    else:
                        print(f'Error in url = {url}, address = {address}, json page = {res}')


                print(datetime.datetime.now() - s)
        except Exception as err:
            if 'TypeError: string indices must be integers' in err.args[0]:
                print(err)
            elif 'playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.' in err.args[0]:
                print(err)

        await self.save_in_dbeaver(save_dbeaver)

    async def start_browser(self, city):
        if self.page:
            pass
        else:
            self.p = await async_playwright().start()
            url = "https://vitaexpress.ru"
            browser = await self.p.firefox.launch(proxy={"server": "http://192.168.0.201:3132", "username": "artmax", "password": "artmax"}, headless=False)
            context = await browser.new_context(base_url="https://vitaexpress.ru")
            self.page = await context.new_page()
            with open("vita_cookie_city.json", "r") as f:
                cities = json.loads(f.read())
                aa = [{"name": 'sec-ch-ua-platform', "value": '"Linux"', "path": "/", "domain": "vitaexpress.ru"},
                      cities[city['region']][city['city']]]

            await context.add_cookies(aa)
            await self.page.goto(url, timeout=300000)
            await asyncio.sleep(2)
            await self.page.click(".pointer.help-city__btn.btn.btn-large.btn-primary")
            await asyncio.sleep(2)
            await self.page.goto('https://vitaexpress.ru/product/omez_kaps_10mg_10/', timeout=300000, wait_until='networkidle')


    async def start_parser(self, info, city, list_urls, task_id):
        self.urls = list_urls
        await self.start_browser(city)
        tasks = []
        for _ in range(4):
            tasks.append(asyncio.create_task(self.making_a_request(info, city, task_id)))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    r = SupperParserVita()
    start = datetime.datetime.now()
    asyncio.run(r.start_parser())
    print(datetime.datetime.now() - start)

