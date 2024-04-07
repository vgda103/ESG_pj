# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
# from urllib.request import urlparse
import urllib.request as ur
from scrapy.pipelines.files import FilesPipeline
import re

class EsgReportPipeline:
    def process_item(self, item, spider):
        return item

class KsaFilePipeline(FilesPipeline):
    def file_path(self, request, item, response=None, info=None):
        # return 'files/' + os.path.basename(ur.urlparse(request.url).path)
        report_no = re.sub(r'[^0-9]', '', ur.urlparse(request.url).query)
        return 'files/' + report_no + '.pdf'    