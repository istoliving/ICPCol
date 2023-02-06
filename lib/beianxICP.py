import requests

from lib.ua import get_user_agent
from bs4 import BeautifulSoup


class BeianX:
    def __init__(self, method):
        self.cookies = None
        self.headers = {
            "User-Agent": get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers",
            "Connection": "close"
        }
        self.method = method

    def cookies(self):
        """
        获取Cookie值
        """
        target = "https://www.beianx.cn/search/"
        resp = requests.get(target, headers=self.headers, verify=False)
        self.cookies = requests.utils.dict_from_cookiejar(resp.cookies)
        return

    def format(self, data_list):
        all_list = []
        for list in data_list:
            new_list = []
            new_list.append(list[0])
            new_list.append(list[4].replace("www.", ""))
            new_list.append(list[2].split("-")[0])
            new_list.append(list[2])
            new_list.append('')
            new_list.append('')
            new_list.append(list[6])
            new_list.append(list[5])
            all_list.append(new_list)
        return all_list

    def query(self, target):
        """
        获取ICP备案信息
        """
        if self.method == 'single':
            print('[√] 正在使用第三方备案网站进行查询')
        try:
            target = "https://www.beianx.cn/search/" + target
            requests.packages.urllib3.disable_warnings()
            resp = requests.get(target, headers=self.headers, verify=False)
        except Exception as e:
            print(e)
        html = resp.text
        bf = BeautifulSoup(html, 'html.parser')
        data_list = []
        trs = bf.find_all('tr')
        for tr in trs:
            index = 0
            tds = tr.find_all('td')
            data = []
            for td in tds:
                if index > 0:
                    data.append(td.text.strip())
                else:
                    index += 1
            if len(data) != 0:
                data_list.append(data)
        if len(data_list) == 0:
            print("查询对象共发现 0 个已备案域名")
        return self.format(data_list)