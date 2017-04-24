# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
import manga.settings

class MangaPipeline(ImagesPipeline):
    # def open_spider(self, spider):
    #     print("fuck 1")
    #     pass

    # def process_item(self, item, spider):
    #     print("fuck 2")
    #     return item

    # def close_spider(self, spider):
    #     pass

    # def process_item(self, item, spider):
    #     print("wtf")
    #     return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        urls = [x['url'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths

        old_name = os.path.abspath(image_paths[0])
        # 默认放在项目的full下，需要修改哦
        old_name = os.path.join(manga.settings.IMAGES_STORE, "full", os.path.basename(old_name))
        # # rename也是可以移动文件到另一个文件夹的
        target_dir = os.path.join(manga.settings.IMAGES_STORE, item.get("manga_name"), item.get("chapter_name"))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target_name = os.path.join(target_dir, os.path.basename(urls[0]))
        print("finished " + target_name)
        os.rename(old_name, target_name)
        return item













