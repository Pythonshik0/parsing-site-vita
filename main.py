import datetime
import json
import asyncio
import time
import ast
import asyncpg
from playwright.async_api import async_playwright
from connect import *
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

#Сделать функции которая привязанна к классу, а не к playwright, чтобы запускать отдельно через start_parser
#функация должна запускать браузер, но не закрывать его, так как async with async_playwright() as p закрывает функцию после прохождения ее цикла

data_1 = []

class SupperParserVita():
    l = 0
    page = None

    async def making_a_request(self, urlss, info, city):

            try:
                s = datetime.datetime.now()
                address = []
                js = f'''() => {{return fetch("{urlss}").then(response => {{return response.text();}})}}'''
                a = await self.page.evaluate(js)
                e = a.split(r'"products": [')[1].split(r']')[0]
                res = json.loads(e)

                if res['name'] != None:
                    main_id_name_price = ([res['id'], res['name'], res['price']])
                    g_id = res['id']
                    #print(g_id)
                    js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                    main_address = await self.page.evaluate(js_city)


                    for i in main_address['TODAY_RESULT']['RESULT']:
                        main_address_g = i['address']
                        address.append(main_address_g)

                    address_and_inp = address + main_id_name_price
                    print(address)
                    print(main_id_name_price)
                    #print(address_and_inp)
                else:
                    if '_' in urlss:
                        urlss = urlss.replace('_', '-')
                        address = []
                        js = f'''() => {{return fetch("{urlss}").then(response => {{return response.text();}})}}'''
                        a = await self.page.evaluate(js)
                        e = a.split(r'"products": [')[1].split(r']')[0]
                        res = json.loads(e)
                        main_id_name_price = ([res['id'], res['name'], res['price']])
                        g_id = res['id']
                        # print(g_id)
                        js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                        main_address = await self.page.evaluate(js_city)

                        for i in main_address['TODAY_RESULT']['RESULT']:
                            main_address_g = i['address']
                            address.append(main_address_g)

                        address_and_inp = address + main_id_name_price
                        print(address_and_inp)

                    elif '-' in urlss:
                        urlss = urlss.replace('-', '_')
                        address = []
                        js = f'''() => {{return fetch("{urlss}").then(response => {{return response.text();}})}}'''
                        a = await self.page.evaluate(js)
                        e = a.split(r'"products": [')[1].split(r']')[0]
                        res = json.loads(e)
                        main_id_name_price = ([res['id'], res['name'], res['price']])
                        g_id = res['id']
                        # print(g_id)
                        js_city = f'''() => {{return fetch("https://vitaexpress.ru/ajax/ajax-city-pharms.php?pick_type=COMMON_DAYS_SINGLE_PRODUCT&check_product={g_id}").then(response => {{return response.json();}})}}'''
                        main_address = await self.page.evaluate(js_city)

                        for i in main_address['TODAY_RESULT']['RESULT']:
                            main_address_g = i['address']
                            address.append(main_address_g)

                        address_and_inp = address + main_id_name_price
                        print(address_and_inp)

                    else:
                        print(f'Error in {urlss}, address = {address}, json page = {res}')

                print(datetime.datetime.now() - s)
            except Exception as err:
                if 'TypeError: string indices must be integers' in err.args[0]:
                    print(err)
                elif 'playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.' in err.args[0]:
                    print(err)

    async def start_browser(self, city):
        if self.page:
            #print(self.page)
            print('Browser open')
        else:
            url = "https://vitaexpress.ru"
            browser = await self.p.firefox.launch(proxy={"server": "http://192.168.0.201:3132", "username": "artmax", "password": "artmax"},headless=False)
            context = await browser.new_context(base_url="https://vitaexpress.ru")
            self.page = await context.new_page()
            with open("vita_cookie_city.json", "r") as f:
                cities = json.loads(f.read())
                aa = [{"name": 'sec-ch-ua-platform', "value": '"Linux"', "path": "/", "domain": "vitaexpress.ru"},
                      cities[city['region']][city['city']]]

            await context.add_cookies(aa)
            await self.page.goto(url, wait_until='domcontentloaded', timeout=60000)
            #await self.page.reload()


    async def start_parser(self, urlss, info, city):
        self.p = await async_playwright().start()
        await asyncio.gather(asyncio.create_task(self.start_browser(city)))
        self.l = self.l + 1
        tasks = []
        for _ in range(5):
            tasks.append(asyncio.create_task(self.making_a_request(urlss, info, city)))
        await asyncio.gather(*tasks)



if __name__ == "__main__":
    r = SupperParserVita()
    start = datetime.datetime.now()
    asyncio.run(r.start_parser())
    print(datetime.datetime.now() - start)




        # l = list(self.headers.keys())
            # #print(l)
            # new_header = {}
            # random.shuffle(l)
            # for n in l:
            #     new_header.update({n: self.headers[n]})
            #     #new_header.update({'Referer': 'https://www.google.com'})
            # print(new_header)
            # self.cookie = await page.context.cookies()
            #
            # a = map(dict, self.cookie)
            #my_tuple = tuple(a)
            # print(a)
            # print(my_tuple)
            #cookie_dict = {}
            #fetch("https://vitaexpress.ru/")
            #{{"headers": {{"Accept": "application/json"}},"method": "GET"}})

            # cookies = httpx.Cookies()
            # for cook in my_tuple:
            #     cookies.set(name=cook['name'], value=cook['value'], domain=cook['domain'], path=cook['path'])
            # ssl_config = httpx._config.SSLConfig()
            # ssl_context = ssl_config.load_ssl_context()
            # ssl_context.options |= getattr(ssl, "PROTOCOL_TLS_CLIENT_v1_3", 0)
            # async with httpx.AsyncClient(cookies=cookies, headers=new_header,
            #                              verify=ssl_context,
            #                              follow_redirects=True) as client:
            #     r = await client.get("https://vitaexpress.ru")
            #     print(r.status_code)
