# author : YangWan
import requests
import random
from selenium import webdriver
class MySearch(object):
    # 开始解析页面
    start_parse_index = None

    # 解析结束页面
    end_parse_index = None

    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    # 网站词条解析数组
    content_parse_list = []

    website_start_url = None

    domain_url = None

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    product_item = None

    # driver = webdriver.Chrome(executable_path="C:\\Users\\yangwan\\PycharmProjects\\qt-colletor\\build\\setup\\chromedriver.exe")

    def __init__(self, keyword, start_parse_index=None, end_parse_index=None, pagenum=None):
        self.keyword = keyword
        self.pagenum = pagenum
        if start_parse_index is not None:
            self.start_parse_index = start_parse_index
        else:
            self.start_parse_index = 1

        if end_parse_index is not None:
            self.end_parse_index = end_parse_index
        else:
            self.end_parse_index = pagenum

    '''
    使用get方法获得页面资源
    参数: 页面url 和编码
    '''
    @staticmethod
    def get_content_whitget(url_path, encoding):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        user_agent += str(random.random())
        headers = {"Accept": "*/*",
                   'User-Agent': user_agent,
                   "Accept-Language": "zh-CN,zh;q=0.9"
                   }
        res = requests.get(url_path, headers=headers)
        res.encoding = encoding
        return res

    #形成爬取连接
    def genrate_pageurl(self):
        pass

    #解析页面内容
    def parse_result_page(self, result):
        pass

    #解析相关搜索
    def parse_relate_search(self, relate_div):
        pass

    #解析其他搜索
    def parse_other_search(self, result):
        pass

    def get_product_item(self):
        self.genrate_pageurl()
        if self.product_item is None:
            print("解析异常！！！")
        return self.product_item
