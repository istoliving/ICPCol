import base64
import hashlib
import os
import time

import cv2
import requests

from lib.ua import get_user_agent


class Miit:
    def __init__(self, method, proxy):
        self.method = method
        self.proxy = proxy
        self.sign = None
        self.base_header = None
        self.check_data = None
        self.token = None
        self.cookie = None

    def get_cookies(self):
        cookie_headers = {'User-Agent': get_user_agent()}
        for i in range(5):
            try:
                req = requests.get('https://beian.miit.gov.cn/', headers=cookie_headers, timeout=5)
                self.cookie = requests.utils.dict_from_cookiejar(req.cookies)['__jsluid_s']
                if self.method == 'single':
                    print('[√] 获取 cookie 成功')
                return
            except:
                time.sleep(0.5)
        print('[×] 获取Cookie失败，请稍后再试！')
        exit()

    def get_token(self):
        timeStamp = round(time.time() * 1000)
        authSecret = 'testtest' + str(timeStamp)
        authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
        auth_data = {'authKey': authKey, 'timeStamp': timeStamp}
        url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        for i in range(5):
            try:
                t_response = requests.post(url=url, data=auth_data, headers=self.base_header, timeout=5).json()
                self.token = t_response['params']['bussiness']
                if self.method == 'single':
                    print('[√] 获取 token 成功')
                return
            except:
                time.sleep(0.5)
        print('[×] 获取Token失败，请稍后再试！')
        exit()

    def get_check_pic(self):
        url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
        self.base_header['Accept'] = 'application/json, text/plain, */*'
        self.base_header.update({'Content-Length': '0', 'token': self.token})
        for i in range(5):
            try:
                p_request = requests.post(url=url, data='', headers=self.base_header, timeout=5).json()
                p_uuid = p_request['params']['uuid']
                big_image = p_request['params']['bigImage']
                small_image = p_request['params']['smallImage']
                # 解码图片，写入并计算图片缺口位置
                with open('bigImage.jpg', 'wb') as f:
                    f.write(base64.b64decode(big_image))
                with open('smallImage.jpg', 'wb') as f:
                    f.write(base64.b64decode(small_image))
                background_image = cv2.imread('bigImage.jpg', cv2.COLOR_GRAY2RGB)
                fill_image = cv2.imread('smallImage.jpg', cv2.COLOR_GRAY2RGB)
                position_match = cv2.matchTemplate(background_image, fill_image, cv2.TM_CCOEFF_NORMED)
                max_loc = cv2.minMaxLoc(position_match)[3][0]
                mouse_length = max_loc + 1
                os.remove('bigImage.jpg')
                os.remove('smallImage.jpg')
                self.check_data = {'key': p_uuid, 'value': mouse_length}
                if self.method == 'single':
                    print('[√] 计算验证码滑块缺口位置成功')
                return
            except:
                time.sleep(0.5)
        print('[×] 计算验证码滑块缺口位置错误，请稍后再试！')
        exit()

    def get_sign(self):
        check_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
        self.base_header.update({'Content-Length': '60', 'token': self.token, 'Content-Type': 'application/json'})
        for i in range(5):
            try:
                pic_sign = requests.post(check_url, json=self.check_data, headers=self.base_header, timeout=5).json()
                self.sign = pic_sign['params']
                if self.method == 'single':
                    print('[√] 自动破解滑块验证码成功')
                return -1
            except:
                time.sleep(0.5)
        print('[×] 图片验证码破解失败，请稍后再试！')
        exit()

    def get_icp_info(self, info_data, p_uuid):
        """
        获取备案信息
        """
        domain_list = []
        info_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        self.base_header.update({'Content-Length': '78', 'uuid': p_uuid, 'token': self.token, 'sign': self.sign})
        # 请求获取备案信息
        try:
            icp_info = requests.post(url=info_url, json=info_data, headers=self.base_header, proxies=self.proxy, timeout=5).json()
            while icp_info['code'] == 429:
                print("[×] 查询失败，{}".format(icp_info["msg"]))
                is_continue = input('备案查询暂停，可更换IP或代理后输入 c 继续查询，输入其他退出：')
                if is_continue == 'c':
                    icp_info = requests.post(url=info_url, json=info_data, headers=self.base_header, proxies=self.proxy,
                                             timeout=5).json()
                else:
                    exit()
        except requests.exceptions.ConnectTimeout:
            print("连接超时，请检查网络或代理设置！")
            exit()
        except Exception:
            for i in range(3):
                time.sleep(0.5)
                icp_info = requests.post(
                    url=info_url, json=info_data, headers=self.base_header, proxies=self.proxy, timeout=5).json()
                while icp_info['code'] == 429:
                    print("[×] 查询失败，{}".format(icp_info["msg"]))
                    is_continue = input('备案查询暂停，可更换IP或代理后输入 c 继续查询，输入其他退出：')
                    if is_continue == 'c':
                        icp_info = requests.post(
                            url=info_url, json=info_data, headers=self.base_header,proxies=self.proxy,timeout=5).json()
                    else:
                        exit()
        # 处理备案信息
        info = info_data['unitName']
        domain_total = icp_info['params']['total']
        page_total = icp_info['params']['lastPage']
        end_row = icp_info['params']['endRow']
        if self.method == 'single':
            print("查询对象：{} 共有 {} 个已备案域名".format(info, domain_total))
        else:
            print("查询对象共发现 {} 个已备案域名".format(domain_total))
        for i in range(0, page_total):
            print(f"正在查询第{i + 1}页...")
            for k in range(0, end_row + 1):
                info_base = icp_info['params']['list'][k]
                domain_name = info_base['domain']
                domain_type = info_base['natureName']
                domain_licence = info_base['mainLicence']
                website_licence = info_base['serviceLicence']
                domain_status = info_base['limitAccess']
                domain_approve_date = info_base['updateRecordTime']
                domain_owner = info_base['unitName']
                try:
                    domain_content_approved = info_base['contentTypeName']
                    if domain_content_approved == "":
                        domain_content_approved = "无"
                except KeyError:
                    domain_content_approved = "无"
                row_data = domain_owner, domain_name, domain_licence, website_licence, domain_type, domain_content_approved, domain_status, domain_approve_date
                domain_list.append(row_data)
            info_data = {'pageNum': i + 2, 'pageSize': '40', 'unitName': info}
            if icp_info['params']['isLastPage'] is True:
                break
            else:
                icp_info = requests.post(info_url, json=info_data, headers=self.base_header).json()
                end_row = icp_info['params']['endRow']
                time.sleep(1)
        return domain_list

    def query(self, target):
        # 对传入参数进行过滤
        target = target.strip().replace("https://www.", "").replace("http://www.", "").replace("http://", "")
        query_data = {'pageNum': '1', 'pageSize': '40', 'unitName': target}
        # 获取Cookie值
        self.get_cookies()
        self.base_header = {
            'User-Agent': get_user_agent(),
            'Origin': 'https://beian.miit.gov.cn',
            'Referer': 'https://beian.miit.gov.cn/',
            'Cookie': f'__jsluid_s={self.cookie}'
        }
        # 获取token
        self.get_token()
        # 滑块验证码识别
        self.get_check_pic()
        self.get_sign()
        # 请求备案数据
        p_uuid = self.check_data['key']
        domain_list = self.get_icp_info(query_data, p_uuid)
        return domain_list
