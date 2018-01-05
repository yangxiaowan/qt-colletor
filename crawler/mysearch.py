# author : YangWan
import requests
class MySearch(object):
    # 搜索排名
    page_index = 0

    # 档期解析页面
    cur_parse_page = 0

    # 其他搜索字段; 包括推荐搜索 90%的人还搜索了什么之类的
    other_search_dit = {}

    relate_search_list = {}

    website_start_url = None

    domain_url = None

    # 是否进行了相关搜索的解析
    relate_search_parseflag = False

    # 是否进行推荐搜索的解析
    recommend_search_parseflag = False

    '''
    使用get方法获得页面资源
    参数: 页面url 和编码
    '''

    @staticmethod
    def get_content_whitget(url_path, encoding):
        headers = {"Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
                   'User-Agent': "Mozilla 5.0 (Windows NT 10.0; Win32; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
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
