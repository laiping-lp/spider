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

    def douyin_search_video(self, search_keywords, max_results=600):
        keywords = search_keywords
        search_keywords = quote(search_keywords)
        print(search_keywords)
        
        try:
            # 读取抖音cookies
            with open('E:\Desktop\code\SOP1\sop\douyin_cookies.txt', 'r', encoding='utf-8')as file:
                cookies = file.read()
        except:
            cookies = None
            raise Exception(f'请复制抖音cookies到 douyin_cookies.txt!!!')
        
        headers = {
            'authority': 'www.douyin.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'referer': 'https://www.douyin.com/search/%E7%83%AD%E9%97%A8?publish_time=0&sort_type=0&source=switch_tab&type=video',
            'cookie': cookies
        }
        
        all_results = []
        offset = 0
        count = 20  # 每次请求的数量
        
        while offset < max_results:
            url = f'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword={search_keywords}&search_source=switch_tab&query_correct_type=1&is_filter_search=0&from_group_id=&offset={offset}&count={count}&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=107.0.0.0&browser_online=true&engine_name=Blink&engine_version=107.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7163531063863133732'
            
            res = requests.get(url=url, headers=headers)
            if res is not None:
                target = json.loads(res.text)
                print(f"当前offset: {offset}, 获取到 {len(target.get('data', []))} 条数据")
                
                if target['status_code'] >= 300:
                    print(f"请求失败，状态码: {target['status_code']}")
                    break
                    
                # if not target.get('data'):
                #     print("没有更多数据了")
                #     break
                    
                videos = target['data']
                results = []
                for video in videos:
                    video = video['aweme_info']
                    temp = {}
                    temp['author'] = video['author']['nickname']
                    temp['video_title'] = video['desc']
                    temp['comment'] = video['statistics']['comment_count']
                    temp['digg'] = video['statistics']['digg_count']
                    temp['share'] = video['statistics']['share_count']
                    temp['collect'] = video['statistics']['collect_count']
                    temp['video_url'] = video['share_info']['share_url']
                    timestamp = video['create_time']
                    # 转换为 UTC 时间
                    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    # 转换为北京时间（UTC+8）
                    beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
                    temp['video_create_time'] = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
                    temp['flower_count'] = video['author']['follower_count']
                    temp['sec_uid'] = video['author']['sec_uid']
                    # temp['ip_position'] = get_ip(temp['sec_uid'])
                    # url_user = f"https://www.douyin.com/aweme/v1/web/user/profile/other/?sec_uid={temp['sec_uid']}"
                    # user_res = requests.get(url=url_user, headers=headers)
                    # user_target = json.loads(user_res.text)
                    
                    results.append(temp)
                
                all_results.extend(results)
                
                # if not target.get('has_more', 0):
                #     print("没有更多数据了")
                #     break
                    
                offset += count
                # 避免请求过于频繁，可以适当加个延迟
                time.sleep(1)
            else:
                raise Exception(f'tiktok: 更新: {search_keywords} 失败!!! 请检查接口')
        
        return all_results


if __name__ == '__main__':
    date = time.strftime("%Y-%m-%d", time.localtime())
    crawler = Crawlers()
    crawler.douyin_search_video('乡村故事')


