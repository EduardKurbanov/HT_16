# import scrapy
# from scrapy.crawler import CrawlerProcess
# from datetime import timedelta, datetime
# from bs4 import BeautifulSoup
#
#
# class VikkaSpider(scrapy.Spider):
#     name = 'vikka'
#     allowed_domains = ['www.vikka.ua']
#     start_urls = ['https://www.vikka.ua']
#
#     def menu(self):
#         while True:
#             try:
#                 print("*" * 100)
#                 print("database starts from 01.12.2014.")
#                 print("*" * 100)
#
#                 day = int(input("1. enter the day of the week in the range -> 1–31. -> "))
#                 if day in range(1, 31 + 1):
#
#                     mounth = int(input("2. enter the month in the range -> 1–12. -> "))
#                     if mounth in range(1, 12 + 1):
#
#                         year = int(
#                             input(f"3. enter the month in the range -> 2014–{datetime.now().year} -> "))
#                         if year <= datetime.now().year:
#                             start_date = datetime(year, mounth, day)
#
#                             return f"https://www.vikka.ua/{start_date.strftime('%Y')}/{start_date.strftime('%m')}/{start_date.strftime('%d')}/"
#
#                         else:
#                             print(
#                                 f"you have exceeded the current year limit or entered an incorrect number -> {year}")
#                     else:
#                         print(
#                             f"<you have exceeded the month limit of the year or entered a wrong number -> {mounth}.>")
#                 else:
#                     print(
#                         f"<you have exceeded the limit of the day of the month or entered a wrong number - > {day}.>")
#
#             except Exception as err:
#                 print(f"<error -> {err}>")
#
#     def start_requests(self):
#         start_urls = "https://www.vikka.ua/2022/01/14/"
#
#         yield scrapy.Request(
#             url=start_urls,
#             callback=self.pars_news
#         )
#
#     def pars_news(self, response):
#         newses = response.xpath('//*[@class="item-cat-post d-flex"]')
#         for news in newses:
#             date = news.xpath('.//*[@class="post-info-style"]/text()').extract_first()
#             title = news.xpath('.//*[@class="title-cat-post"]/a/text()').extract_first()
#             link = news.xpath('.//*[@class="title-cat-post"]/a/@href').extract_first()
#
#             data = {"date": date, "title": title, "link": link}
#
#             req = scrapy.http.Request(url=link, callback=self.par_news_content)
#             req.meta['data'] = data
#             yield req
#
#     def par_news_content(self, request):
#         data = request.meta['data']
#         sou = BeautifulSoup(request.text, "lxml")
#         ss = sou.find("div", class_="entry-content -margin-b")
#         ss1 = sou.find_all('a', class_="post-tag")
#
#         list_tag = []
#         for tag in ss1:
#             list_tag.append(f"#{'_'.join(tag.text.split())}")
#
#         data['text'] = ss.text.strip()
#         data['tags'] = list_tag
#
#         yield data
#
#
# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(VikkaSpider)
#     process.start()
