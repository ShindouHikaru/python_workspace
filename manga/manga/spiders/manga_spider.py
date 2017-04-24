import scrapy
from manga.settings import *
import sys
from manga.items import *

# javascript:alert($(document).unbind("contextmenu",""));

XPATH_MAP = {
    "eh":{
        "urls": ["https://"],
        "cur_page": "//div[@class='gdtm']/div/a/@href", 
        "next_page": "//div[@class='gtb']/table/tr/td[last()]/a/@href", 
        "img_parse": "//img[@id='img']/@src"
    },
    "cartomad":{
        # Missing scheme in request url: h 是urls必须是List而不是str,而且这个url结果不许加"/"..奇怪
        "urls": ["http://www.cartoonmad.com/comic/1633.html"],
        "cur_page": "//a[contains(., '話')]/@href",  # 默认下载话
        "cur_page_over": "//a[contains(., '卷')]/@href",
        "detail_page": "//option[contains(., '頁')]/@value",  
        "img_parse": "//img[contains(@src, 'cartoonmad.com')]/@src",
        "over_tag": "//img/@src[contains(., 'chap9.gif')]",
        "continued_tag": "//img/@src[contains(., 'chap1.gif')]",
    },
    "dmzj":{
        "cur_page": "", 
        "next_page": "", 
        "img_parse": "//div[@id='center_box']/img/@src",
    },
    "ikanman":{
        "urls": ["http://tw.ikanman.com/comic/2801/"],
        # tr[* = 'X']/following-sibling::tr[1]
        "cur_page": "//span[contains(., '回') and ./i[contains(., 'p')]]/../@href", 
        "next_page": "", 
        "img_parse": "//img[@id='mangaFile']/@src",
        # "not_url_join":True
    },
}
XPATH_TYPE = "cartomad"
# MANGA_NAME = ""
# CHAPTER_NAME = ""

class MangaSpider(scrapy.Spider):
    name = "manga"
    data = XPATH_MAP.get(XPATH_TYPE);
    # start_urls = ["https://e-hentai.org/g/1052044/71cffc9098/"]

    def __init__(self):
        self.headers = HEADERS

    def start_requests(self):
        print(sys.argv[1])
        self.log(self.data.get("urls"))
        urls = self.data.get("urls")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # current page
        cur_xpath = self.data.get("cur_page")
        # if(self.is_exist_over_tag(response)):
        #     cur_xpath = self.data.get("cur_page_over")
        srcs= response.xpath(cur_xpath).extract()
        # srcs = [response.urljoin(x) for x in srcs]
        # for src in srcs:
        #     yield scrapy.Request(url=src, callback=self.parse_detail)
        #     break; # test cut

        # next page
        # srcs = response.xpath(data.get("next_page")).extract()
        # for src in srcs:
        #     yield scrapy.Request(url=src, callback=self.parse)

        # 为毛方法进不去。。妈的打日志都没反应，难道是需要加上yield？不是，是需要加上return
        return self.get_new_req(srcs, self.parse_detail, response)
        # self.get_new_req(next_srcs, self.parse)

    def parse_detail(self, response):
        # 第一页被去重，所以这里直接下载这个第一页，但是这里必须用yield，不然根本进入不到pipeline，握草
        yield self.parse_image(response)
        srcs = response.xpath(self.data.get("detail_page")).extract()
        srcs = [response.urljoin(x) for x in srcs]
        for src in srcs:
            yield scrapy.Request(url=src, callback=self.parse_image) 

    def get_new_req(self, srcs, callback, response):
        # self.log(srcs)
        srcs = [response.urljoin(x) for x in srcs]
        for src in srcs:
            yield scrapy.Request(url=src, callback=callback)

    def parse_image(self, response):
        srcs = response.xpath(self.data.get("img_parse")).extract()
        self.log(srcs)
        title = response.xpath("//title/text()").extract_first().split("-")
        manga_name = title[0].split(" ")[0]
        chapter_name = title[1]
        self.log("downloading " + manga_name + ": " + chapter_name)

        item = MangaItem()
        item["image_urls"] = srcs
        item["chapter_name"] = chapter_name.strip()
        item["manga_name"] = manga_name
        return item

    def is_exist_over_tag(self, resp):
        is_over = len(resp.xpath(self.data.get("over_tag")).extract()) > 0
        return is_over

