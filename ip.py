from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
import time

def get_ip(sec_uid):
    # 设置无头浏览器
    options = Options()
    options.add_argument("--headless")  # 无界面模式
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")

    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    url = f"https://www.douyin.com/user/{sec_uid}"
    driver.get(url)
    # time.sleep(5)  # 等待动态加载

    # 获取页面HTML
    page_html = driver.page_source
    driver.quit()

    # 解析HTML，提取XPath数据
    tree = html.fromstring(page_html)

    # 你的XPath路径
    xpath = "/html/body/div[2]/div[1]/div[4]/div[2]/div/div/div/div[2]/div[2]/p/span[2]"
    data = tree.xpath(xpath + "/text()")  # 提取文本

    # if data:
    #     print("提取到的数据:", data[0].strip())
    # else:
    #     print("XPath 未找到数据，可能页面结构已变化！")
    return data[0].strip().split("：")[1] if data else None

