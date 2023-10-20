
# 1. run this in command line: python3 -m ensurepip
# 2. run /env/venv/bin/python3 -m pip install --upgrade pip
# 3. run pip install -r requirements.txt
# 4. run python crawler.py
# 5. git rm -r lib to remove lib or manually delete lib file before uploading to github

from multiprocessing import Pool
import time
from bs4 import BeautifulSoup
import asyncio
import requests
import sys
from urllib import request
import aiohttp
import json
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    f"{path}/lib/python3.9/site-packages")


class Events:
    def __init__(self, pages, event_set) -> None:
        self.pages = pages
        self.url = []
        self.event_set = event_set

    def generate_urls(self):
        for page in range(self.pages):
            url = f'https://www.eventbrite.com/d/nj--jersey-city/all-events/?page={page}&start_date=2023-10-21&end_date=2023-10-30'
            self.url.append(url)
        return self.url

    def scrape_url(self, url):
        events = set()
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, "html.parser")
        # events = soup.find_all("a", {"class": "event-card-link"})
        response = request.Request(url)
        resp = request.urlopen(response)
        respData = resp.read()
        soup = BeautifulSoup(respData, "html.parser")
        events = soup.find_all("a", {"class": "event-card-link"})

        for event in events:
            self.event_set.add(event['data-event-id'])
        return self.event_set


class async_Event(Events):
    def __init__(self, pages, event_set) -> None:
        super().__init__(pages, event_set)

    async def scrape(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')
                events = soup.find_all("a", {"class": "event-card-link"})
                for event in events:
                    self.event_set.add(event['data-event-id'])
                return self.event_set

    async def main(self):
        start_time = time.time()

        tasks = []

        for url in self.url:
            task = asyncio.create_task(self.scrape(url))
            tasks.append(task)
        await asyncio.gather(*tasks)

        time_difference = time.time() - start_time
        print(f'Async Scraping time: %.2f seconds.' % time_difference)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    ### Multiprocessing ###
    event_ids = set()
    events = Events(20, event_ids)
    url_list = events.generate_urls()

    start = time.time()
    p = Pool(15)
    event_list = p.map(events.scrape_url, url_list)
    final_ids = set()
    for i in range(len(event_list)):
        final_ids = final_ids | event_list[i]
    print(len(final_ids))
    end = time.time()
    print(f'Multiprocessing Scraping time: %.2f seconds.' % (end - start))

    ### Async ###
    event_ids = set()
    a_Event = async_Event(20, event_ids)
    url_list = a_Event.generate_urls()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a_Event.main())
    print(len(event_ids))
    data_str = json.dumps(event_ids, cls=SetEncoder)

    f = open("eventbrite.json", "w")
    f.write(str(data_str))
    f.close()
    p.terminate()
    p.join()


# async def get_events(page):
#     events = set()
#     for i in range(page):
#         url = f"https://www.eventbrite.com/d/nj--jersey-city/all-events/?page={i}&start_date=2023-10-19&end_date=2023-10-22"
#         response = requests.get(url)
#         print(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         events = soup.find_all("a", {"class": "event-card-link"})
#         for event in events:
#             event_ids.add(event['data-event-id'])
#     return events
# sys.path.append("lib")

# event_ids = set()

# start_time = time.time()
# events = asyncio.run(get_events(10))
# print("--- %s seconds ---" % (time.time() - start_time))

# def get_events_no_async(page):
#     events = set()
#     for i in range(page):
#         url = f"https://www.eventbrite.com/d/nj--jersey-city/all-events/?page={i}&start_date=2023-10-19&end_date=2023-10-22"
#         response = requests.get(url)
#         print(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         events = soup.find_all("a", {"class": "event-card-link"})
#         for event in events:
#             event_ids.add(event['data-event-id'])
#     return events

# start_time = time.time()
# with concurrent.futures.ThreadPoolExecutor(5) as executor:
#     events = executor.map(get_events_no_async(10))
# print("--- %s seconds ---" % (time.time() - start_time))


# print(titles)
# print(soup.prettify())  #輸出排版後的HTML內容
# f = open("eventbrite.html", "w")
# f.write(str(soup))
# f.close()


# print(len(event_ids))
# print(event_ids)

# with open('eventbrite.html', 'w') as f:
#     for line in titles:
#         f.write(f"{line}\n")
