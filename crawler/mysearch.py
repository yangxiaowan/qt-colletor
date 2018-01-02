# author : YangWan
import requests
class MySearch(object):

    '''
    使用get方法获得页面资源
    参数: 页面url 和编码
    '''
    def get_content_whitget(self, url_path, encoding):
        headers = {"Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
                   'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
                   "Accept-Language": "zh-CN,zh;q=0.9"
                   }
        res = requests.get(url_path, headers = headers)
        res.encoding = encoding
        return res

    #形成爬取连接
    def genrate_pageurl(self):
        pass

    #解析页面内容
    def parse_result_page(self, result):
        pass

    #解析推荐搜索
    def parse_recommend_search(self):
        pass

    #解析其他搜索
    def parse_other_search(self):
        pass
