
---

# 招标信息爬虫

该项目是一个用于CCGP网站的招标信息的爬虫工具为后续RAG做基础，使用了 Requests 来进行网页内容的异步抓取，同时使用 BeautifulSoup 对网页内容进行解析。

## 功能特点

- 支持指定起止页码范围进行内容抓取。
- 结果保存为 Excel 文件，方便后续分析和处理。
- 保存文件格式如下

| 标题 | 项目概况 | 一 | 二 | 三 | 四 | 五 | 六 | 七 | 八 | 九 | 附件链接 | 链接 |
|------|---------|----|----|----|----|----|----|----|----|----|----------|------|
| xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx |


## 安装依赖

在运行代码之前，请确保已安装以下依赖：

- python==3.10
- beautifulsoup4==4.12.3
- pandas==2.2.1
- requests==2.31.0

你可以使用以下命令安装 Python 依赖：

```bash
pip install beautifulsoup4==4.12.3
pip install pandas==2.2.1
pip install requests==2.31.0
```

## 使用方法

1. 运行 run.py 文件,变量设置：
* start_page 开始爬取的页码
* end_page 结束爬取的页码
* wait1 随机时间间隔的最小值
* wait2 随机时间间隔的最大值

## 示例

以下是一个示例 (run.py)，爬取第 1 页到第 2 页，并将结果保存为 Excel 文件：

```python
from Scraper_all import main

start_page = 1
end_page = 2
wait1 = 1
wait2 = 1

main(start_page = start_page, end_page = end_page, wait1 = wait1, wait2 = wait2)
```
---
