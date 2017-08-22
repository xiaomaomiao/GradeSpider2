import os
import sys
from scrapy import cmdline
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
cmdline.execute(['scrapy','crawl','hhu'])
