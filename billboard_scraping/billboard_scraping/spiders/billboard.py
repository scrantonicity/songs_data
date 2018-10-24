# run this file as
#
# scrapy runspider scrape.py -t txt -o billboard.txt

from scrapy import Request
from scrapy.spiders import Spider
import string

# Returns a string of the format YYYY-MM-DD
#
# Input: Ints for year, month, and day
# Output: String of the format YYYY-MM-DD
def getDateString(year,month,day):
  year_string = str(year)
  if month < 10:
    month_string = "0" + str(month) 
  else:
    month_string = str(month)
  if day < 10:
    day_string = "0" + str(day)
  else: 
    day_string = str(day)
  return year_string+"-"+month_string+"-"+day_string

# Determines if a day is valid based on day and month
#
# Input: Ints day and month
# Output: Boolean of validity 
def validDate(day,month):
  if day < 29: return True
  short_months = [2,4,6,9,11]
  if month in short_months:
    if month == 2: return False
    if day > 30: return False
  return True

# Gets a list of all of the billboard urls to scrape
#
# Input: none
# Output: List of all urls
def getBillboardURLS():
  urls = []
  url_head = "https://www.billboard.com/charts/hot-100/"
  years = [i for i in range(1959,1960)]
  months = [i for i in range(1,3)]
  days = [i for i in range(1,32)]
  for year in years:
    for month in months:
      for day in days:
        if validDate(day,month):
          date_string = getDateString(year,month,day)
          url = url_head + date_string
          urls.append(url)
  return urls

# Artist responses sometimes contain a nested link and sometimes don't
# This determines which is true, and gets calls the appropriate xpath line
# and returns a string of the artist
#
# Input: response assuming there is no inner link
# Output: string of the artist's name
def getArtist(first_response, response):
  if len(first_response) > 1:
    return response.xpath("//div[contains(@class, 'chart-number-one__artist')]/a/text()").extract()[0].strip()
  else:
    return first_response[0].strip()

class S1(Spider):
  name = 's1'
  USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
  url_index = 0
  # start_urls = ['http://www.billboard.com/charts/billboard-200/1964-01-01','http://www.billboard.com/charts/billboard-200/1964-01-10']
  start_urls = getBillboardURLS()

  def parse(self, response):
    ans = []
    item = {}
    item['date'] = self.start_urls[self.url_index][-10:]
    item['url'] = self.start_urls[self.url_index]
    item['title'] = response.xpath("//div[contains(@class, 'chart-number-one__title')]//text()").extract()[0].strip()
    item['artist'] = getArtist(response.xpath("//div[contains(@class, 'chart-number-one__artist')]/text()").extract(), response)
    # item['weeks_at_one'] = response.xpath("//div[contains(@class, 'chart-number-one__weeks-at-one')]/text()").extract()
    # item['weeks_on_chart'] = response.xpath("//div[contains(@class, 'chart-number-one__weeks-on-chart')]/text()").extract()
    ans.append(item) 
    self.url_index+=1           
    return ans

