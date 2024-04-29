import pandas as pd
import random
import requests
import re
from bs4 import BeautifulSoup
import random
import requests
import time

def get_title(soup):
    # 获取标题元素并提取文本
    title_element = soup.find('h2')
    if title_element:
        return title_element.text.strip()
    else:
        return None

def get_summary(html_content):
    soup = html_content
    # 获取项目概况元素
    project_summary_element = soup.find('blockquote')

    # 提取项目概况文本
    if project_summary_element:
        return project_summary_element.text.strip()
    elif soup.find(string=re.compile('项目概况')):
        parent_element = soup.find(string=re.compile('项目概况')).find_parent()

        if parent_element.name == 'td':
            return '项目概况         ' +soup.find('div', class_='vF_detail_content').find('table').find_all('tr')[1].text.strip()
        else:
            return '项目概况         ' +parent_element.find_all_next()[0].get_text().strip()
    else:
        text = html_content.find().get_text()
        end_pos = text.find('一、')
        if end_pos == -1:
            return None  # 如果未找到 end_pattern，返回 None
        # 从 end_pattern 的位置向前查找最近的 start_pattern
        start_pos = text.rfind('招标公告', 0, end_pos)
        if start_pos == -1:
            return None  # 如果未找到 start_pattern，返回 None
        # 返回 start_pattern 和 end_pattern 之间的内容
        return '项目概况         ' + text[start_pos + len('招标公告'):end_pos].strip()


def get_contents(html_content, start_pattern, end_pattern):
    """
    从指定标签中提取内容，并删除最后几行。

    参数:
    - tag: 要提取内容的标签

    返回:
    - 提取并处理后的内容字符串，如果未找到指定标签则返回空字符串
    """

    if html_content.find('strong', string=re.compile(f'{start_pattern}')):
        tag = html_content.find('strong', string=re.compile(f'{start_pattern}'))
        # 查找指定标签下的所有内容
        contents = tag.find_all_next(lambda tag: tag.name == 'p' or tag.name == 'table' or tag.name == 'strong')
        # 将所有内容组合成一个字符串
        title = tag.find_parent().get_text()
        text = title + "\n" + ""
        for content in contents:
            if content.name == 'p':
                if content.name == 'p':
                    text += content.get_text(strip=True) + "\n"
                else:
                    text += content.get_text(strip=True)
            elif content.name == 'table':
                if content.find('thead'):
                    header_cells = content.find('thead').find_all('th')
                    data_cells = content.find('tbody').find('tr').find_all('td')
                    data_dict = {}
                    for header, data in zip(header_cells, data_cells):
                        data_dict[header.text.strip()] = data.text.strip()
                    data_dict = str(data_dict)
                    text += data_dict + "\n"
                else:
                    header_cells = content.find('tbody').find_all('tr')[0].find_all('td')
                    data_cells = content.find('tbody').find_all('tr')[1].find_all('td')
                    data_dict = {}
                    for header, data in zip(header_cells, data_cells):
                        data_dict[header.text.strip()] = data.text.strip()
                    data_dict = str(data_dict)
                    if len(content.find('tbody').find_all('tr')) >= 3:
                        other = content.find('tbody').find_all('tr')[2].text.strip()
                        text += data_dict + other + "\n"
                    text += data_dict + "\n"
            elif content.name == 'strong':
                break

        # 删除最后几行的内容
        text_lines = text.splitlines()
        # 去除空行
        text_lines = [line for line in text_lines if line.strip()]
        text = '\n'.join(text_lines)
        return text
    elif html_content.find().get_text().find(start_pattern):
        if html_content.find().get_text().find(end_pattern):
            text = html_content.find().get_text()
            end_pos = text.find(end_pattern)
            if end_pos == -1:
                return None  # 如果未找到 end_pattern，返回 None
            # 从 end_pattern 的位置向前查找最近的 start_pattern
            start_pos = text.rfind(start_pattern, 0, end_pos)
            if start_pos == -1:
                return None  # 如果未找到 start_pattern，返回 None
            # 返回 start_pattern 和 end_pattern 之间的内容
            return f'{start_pattern}' + text[start_pos + len(start_pattern):end_pos]
        else:
            text = html_content.find().get_text()
            end_pos = text.find('主办单位')
            if end_pos == -1:
                return None  # 如果未找到 end_pattern，返回 None
            # 从 end_pattern 的位置向前查找最近的 start_pattern
            start_pos = text.rfind(start_pattern, 0, end_pos)
            if start_pos == -1:
                return None  # 如果未找到 start_pattern，返回 None
            # 返回 start_pattern 和 end_pattern 之间的内容
            return f'{start_pattern}' + text[start_pos + len(start_pattern):end_pos]
    else:
        return 'NA'

def get_links(html_content):
    # 使用正则表达式找到包含 "相关附件：" 文本的标签
    attachment_tag = html_content.find(string=re.compile(r'(相关附件：|附件信息：)'))
    # 如果找到了相关标签
    if attachment_tag:
        # 找到父节点
        parent_tag = attachment_tag.find_parent()
        # 如果父节点存在，则继续后续操作
        if parent_tag:
            # 找到父节点后面的兄弟节点
            sibling_tags = parent_tag.find_next_siblings()
            # 存储附件链接的列表
            attachment_links = []
            # 遍历所有兄弟节点
            for sibling in sibling_tags:
                # 找到当前兄弟节点下的所有链接标签
                links = sibling.find_all('a')
                # 将链接添加到 attachment_links 列表中
                for link in links:
                    attachment_links.append(link.get('href'))
        else:
            # 如果父节点不存在，则返回 NA 或其他你想要的值
            attachment_links = 'NA'
    elif html_content.find(string=re.compile('附件：')):
        id = html_content.find(string=re.compile('附件：')).find_parent().find_next('a').get('id')
        if id:
            attachment_links = ['https://download.ccgp.gov.cn/oss/download?uuid=' + id,]
        else:
            attachment_links = 'NA'

    else:
        # 如果找不到相关标签，则返回 NA 或其他你想要的值
        attachment_links = 'NA'

    return attachment_links


class CCGPcountent:
    def __init__(self):
        """
        初始化 CCGPScraper 实例
        """
        self.headers_list = [
            {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
            }, {
                'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
            }, {
                'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
            }, {
                'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
            }, {
                'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
            }, {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
            }, {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }, {
                'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
            }, {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            },    {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/21.3.2.140 Yowser/2.5 Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
            },
            {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
            },
            {
                'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'
            },
            {
                'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
            },
            {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G988U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
            }
        ]

    def fetch_ccgp_contents(self,urls_list):
        """
        遍历每个 URL，发送请求并获取响应，最后返回一个包含 BeautifulSoup 对象的列表。

        参数:
        - urls_list: 包含所有需要抓取的 URLs 的列表。
        - headers_list: 包含多个请求头的列表，用于随机选择以模拟不同的用户代理。

        返回:
        - responses: 一个包含每个 URL 请求返回的 BeautifulSoup 对象的列表。
        """
        responses = []
        count = 0
        for url in urls_list:
            count += 1
            headers = random.choice(self.headers_list)  # 随机选择一个请求头
            try:
                response = requests.get(url, headers=headers)  # 发送请求
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, 'html.parser')  # 解析 HTML
                    responses.append(soup)  # 将 BeautifulSoup 对象添加到列表中
                    print(f"第{count}页请求成功, URL: {url}")
                else:
                    responses.append('')
                    print(f"第{count}页请求失败: {response.status_code}, URL: {url}")

            except requests.RequestException as e:
                print(f"第{count}页请求错误: {e}, URL: {url}")
                responses.append(None)  # 出错时添加 None 以保持列表长度一致
            interval = random.randint(1, 5)  # 生成一个随机间隔时间
            time.sleep(interval)  # 等待随机时间
        return responses



