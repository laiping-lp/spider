import json
import time
import datetime
import requests
import random
from selenium import webdriver
import re
from urllib.parse import quote
import configparser
# from pytube import YouTube
from bs4 import BeautifulSoup

from datetime import datetime, timezone, timedelta
from ip import get_ip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

config = configparser.ConfigParser()
config.read('E:\Desktop\code\SOP1\sop\config.ini', encoding='utf-8')
crawlers_config = config['Crawlers']
path_config = config['Path']
# 请求时最大线程数
MAX_THREAD = int(crawlers_config['Max_thread'])
# tiktok douyin 关键字搜索视频结果分页,最多为3
MAX_PAGE = int(crawlers_config['Max_page'])


class Crawlers(object):
    def __init__(self):
        print(f'初始化爬虫...')
        self.tiktok_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
        self.tiktok_api_headers = {'user-agent': 'com.ss.android.ugc.trill/2613 (Linux; U; Android 10; en_US; Pixel 4; Build/QQ3A.200805.001; Cronet/58.0.2991.0)'}
        self.info = {'video_id': None, 'video_title': None, 'video_url': None, 'audio_url': None, 'update_timestamp': None}
        self.youtube_results = []
        self.tiktok_results = []
        self.douyin_results = []
        # self.arg = sys.argv[1]
        if crawlers_config['Proxy_switch'] == 'False':
            self.proxy = None
        elif crawlers_config['Use_socks5_proxy'] == 'True':
            self.proxy = {"http": crawlers_config['Socks5_proxy'], "https": crawlers_config['Socks5_proxy']}
        elif crawlers_config['Use_simple_proxy'] == 'True':
            self.proxy = {"http": 'http://' + crawlers_config['Socks5_proxy'], "https": 'https://' + crawlers_config['Socks5_proxy']}
        else:
            self.proxy = None
        # 初始化 Selenium WebDriver
        self.driver = self._init_selenium_driver()

    def _init_selenium_driver(self):
        """初始化 Chrome WebDriver"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
        
        # 如果需要代理，可以在这里设置
        if crawlers_config['Proxy_switch'] == 'True':
            if crawlers_config['Use_socks5_proxy'] == 'True':
                options.add_argument(f"--proxy-server=socks5://{crawlers_config['Socks5_proxy']}")
            elif crawlers_config['Use_simple_proxy'] == 'True':
                options.add_argument(f"--proxy-server=http://{crawlers_config['Socks5_proxy']}")
        
        # 无头模式（headless=True 表示不显示浏览器窗口）
        options.headless = False
        
        # 自动下载并安装 ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # 加载抖音 Cookies（如果有）
        try:
            with open('E:\Desktop\code\SOP1\sop\douyin_cookies.txt', 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                driver.get("https://www.douyin.com")
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except:
            print("未找到或无法加载抖音 Cookies，将以无登录状态访问")
        
        return driver

    def douyin_search_video(self, search_keywords, max_results=50):
        """使用 Selenium 模拟滚动获取抖音搜索结果"""
        search_keywords = quote(search_keywords)
        search_url = f"https://www.douyin.com/search/{search_keywords}?type=video"
        
        self.driver.get(search_url)
        time.sleep(5)  # 等待页面加载

        results = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while len(results) < max_results:
            # 模拟滚动
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待新内容加载
            
            # 检查是否滚动到底部
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("已滚动到底部，无法加载更多内容")
                break
            last_height = new_height
            
            # 提取当前页面的视频信息
            video_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "EKREid")]')
            for video in video_elements:
                try:
                    title = video.find_element(By.XPATH, './/span[contains(@class, "jjKJTfR1")]').text
                    video_url = video.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    author = video.find_element(By.XPATH, './/span[contains(@class, "Nu66P_ba")]').text
                    
                    results.append({
                        'author': author,
                        'video_title': title,
                        'video_url': video_url
                    })
                    
                    if len(results) >= max_results:
                        break
                except Exception as e:
                    print(f"提取视频信息失败: {e}")
                    continue
        
        return results[:max_results]  # 确保不超过最大数量

if __name__ == '__main__':
    date = time.strftime("%Y-%m-%d", time.localtime())
    crawler = Crawlers()
    results = crawler.douyin_search_video('乡村故事', max_results=30)
    print(f"获取到 {len(results)} 条结果:")
    for idx, item in enumerate(results, 1):
        print(f"{idx}. {item['video_title']} - {item['author']} ({item['video_url']})")