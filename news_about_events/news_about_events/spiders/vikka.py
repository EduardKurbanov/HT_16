import scrapy
from scrapy.spiders import Request
from datetime import datetime
from bs4 import BeautifulSoup
from news_about_events.items import NewsAboutEventsItem


class VikkaSpider(scrapy.Spider):
    name = 'vikka'
    allowed_domains = ['www.vikka.ua']
    start_urls = ['https://www.vikka.ua']

    def enter_data(self):
        while True:
            try:
                print("*" * 100)
                print("database starts from 01.12.2014.")
                print("*" * 100)

                day = int(input("1. enter the day of the week in the range -> 1–31. -> "))
                if day in range(1, 31 + 1):

                    mounth = int(input("2. enter the month in the range -> 1–12. -> "))
                    if mounth in range(1, 12 + 1):

                        year = int(
                            input(f"3. enter the month in the range -> 2008–{datetime.now().year} -> "))
                        if 2008 <= int(year) <= int(datetime.now().year):
                            start_date = datetime(year, mounth, day)

                            return [start_date.strftime('%Y'), start_date.strftime('%m'), start_date.strftime('%d')]

                        else:
                            print(
                                f"you have exceeded the current year limit or entered an incorrect number -> {year}")
                            continue
                    else:
                        print(
                            f"<you have exceeded the month limit of the year or entered a wrong number -> {mounth}.>")
                else:
                    print(
                        f"<you have exceeded the limit of the day of the month or entered a wrong number - > {day}.>")

            except Exception as err:
                print(f"<error -> {err}>")

    def start_requests(self):
        year, mounth, day = self.enter_data()
        start_urls = f'https://www.vikka.ua/{year}/{mounth}/{day}/'
        date = f'{year}_{mounth}_{day}'
        yield Request(
            url=start_urls,
            callback=self.pars_news,
            cb_kwargs=dict(date=date)
        )

    def pars_news(self, request, date=None):
        item = NewsAboutEventsItem()
        soup = BeautifulSoup(request.text, "lxml")
        pars_news = soup.find_all("li", class_="item-cat-post d-flex")

        item["date"] = date
        for i in pars_news:
            item["header"] = i.find("h2", class_="title-cat-post").text.strip()
            item["link"] = i.find("a").get("href")
            req = scrapy.http.Request(url=item["link"], callback=self.par_text_tag)
            req.meta['item'] = item.copy()

            yield req

        next_page = soup.find("a", class_="next page-numbers").get("href")
        if next_page is not None:
            req = scrapy.http.Request(url=next_page, callback=self.pars_news, cb_kwargs=dict(date=item["date"]))
            req.meta['item'] = item.copy()
            yield req

    def par_text_tag(self, request):
        data = request.meta['item']
        soup = BeautifulSoup(request.text, "lxml")
        p_text = soup.find("div", class_="entry-content -margin-b")
        p_tag = soup.find_all('a', class_="post-tag")
        data["tag"] = [f"#{'_'.join(tag.text.split())}" for tag in p_tag]
        data["text"] = p_text.text.strip()
        yield data
