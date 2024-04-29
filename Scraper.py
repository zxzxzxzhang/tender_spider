import pandas as pd
import random
import requests
import re
from bs4 import BeautifulSoup
from page_utils import CCGPScraper
from utils import CCGPcountent, get_title, get_summary, get_contents, get_links
import datetime

start_time = datetime.datetime.now()

start_page = 1
end_page = 20
biaoshu = pd.DataFrame({},columns=['标题', '项目概况', '一', '二', '三', '四', '五', '六', '七', '八','九','附件链接', '链接'])

a = CCGPScraper()
all_urls = a.get_urls(start_page,end_page)
ccgp_content = CCGPcountent()
ccgp_content = ccgp_content.fetch_ccgp_contents(all_urls)

for i in range(len(ccgp_content)):
    try:
        # 检查 ccgp_content[i] 是否为空
        if ccgp_content[i] is None:
            print('第', i, '页为空，跳过处理。')
            continue
        title = get_title(ccgp_content[i])
        summary = get_summary(ccgp_content[i])
        tag1_text = get_contents(ccgp_content[i],'一、', '二、')
        tag2_text = get_contents(ccgp_content[i],'二、', '三、')
        tag3_text = get_contents(ccgp_content[i],'三、', '四、')
        tag4_text = get_contents(ccgp_content[i],'四、', '五、')
        tag5_text = get_contents(ccgp_content[i],'五、', '六、')
        tag6_text = get_contents(ccgp_content[i],'六、', '七、')
        tag7_text = get_contents(ccgp_content[i],'七、', '八、')
        tag8_text = get_contents(ccgp_content[i],'八、', '九、')
        tag9_text = get_contents(ccgp_content[i],'九、', '十、')
        links = get_links(ccgp_content[i])
        biaoshu.loc[i] = [title, summary, tag1_text, tag2_text, tag3_text, tag4_text, tag5_text, tag6_text, tag7_text, tag8_text, tag9_text, links, all_urls[i]]
        print('第', i, '页处理完成')
    except Exception as e:
        print('处理第', i, '页时出现异常：', e)

biaoshu.to_excel(f'招标信息第{start_page}页到{end_page}页.xlsx', index=False)

# 记录处理结束时间
end_time = datetime.datetime.now()
print('处理结束时间：', end_time)
# 计算总共用时
duration = end_time - start_time
print('总共用时：', duration)