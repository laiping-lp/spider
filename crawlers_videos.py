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
import pandas as pd
from tqdm import tqdm
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

    def douyin_search_video(self, search_keywords,count=20, offset=20):
        # keywords = search_keywords
        search_keywords = quote(search_keywords)
        print(search_keywords)
        url = f'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword={search_keywords}&search_source=switch_tab&query_correct_type=1&is_filter_search=0&from_group_id=&offset={offset}&count={count}&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=107.0.0.0&browser_online=true&engine_name=Blink&engine_version=107.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7163531063863133732'
        
        # url = f'https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword={search_keywords}&search_source=switch_tab&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=30&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=107.0.0.0&browser_online=true&engine_name=Blink&engine_version=107.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7163531063863133732'
        # 
        # url = "https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword=%E4%B9%A1%E6%9D%91%E6%95%85%E4%BA%8B&search_source=switch_tab&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=20&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=107.0.0.0&browser_online=true&engine_name=Blink&engine_version=107.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7163531063863133732"
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
        res = requests.get(url=url, headers=headers)
        has_more = 0
        if res is not None:
            # target = json.loads(res)
            target = json.loads(res.text)
            # print(len(target['data']))
            if target['status_code'] < 300:
                if 'has_more' in target.keys():
                    if target['has_more'] == 1:
                        has_more = 1
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
                    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
                    temp['video_create_time'] = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
                    temp['flower_count'] = video['author']['follower_count']
                    temp['sec_uid'] = video['author']['sec_uid']
                    temp['ip_position'] = get_ip(temp['sec_uid'])
                    results.append(temp)
                return results, has_more
            else:
                raise Exception(f'tiktok: 更新: {search_keywords} 失败!!! 接口返回异常')
        else:
            raise Exception(f'tiktok: 更新: {search_keywords} 失败!!! 请检查接口')

    

if __name__ == '__main__':
    date = time.strftime("%Y-%m-%d", time.localtime())
    crawler = Crawlers()
    all_results = []  # Initialize a list to store all results
    keywords = ['农村生活','我的乡村生活','田园生活']
    keywords = ['我的乡村生活','田园生活']
    keywords = ['田园生活']
    for keyword in keywords:
        all_results = []  # Initialize a list to store all results
        for i in tqdm(range(30, 100)):
            results, _ = crawler.douyin_search_video(keyword, count=i, offset=0)

            if len(results) == 0:
                print(f'抖音: 更新: {keyword} 失败!!! 接口返回异常')
                print(i)
                break
            
            # Append the current batch of results to the main list
            all_results.extend(results)

        # Convert all accumulated results to DataFrame at once
        if all_results:  # Only proceed if we have data
            df = pd.DataFrame(all_results)
            
            # Define column order
            columns = [
                'author', 
                'video_title', 
                'video_create_time',
                'digg', 
                'comment', 
                'share', 
                'collect',
                'flower_count',
                'sec_uid',
                'video_url',
                'ip_position'
            ]
            
            df = df[columns]  # Reorder columns
            
            # Save to Excel
            excel_filename = f"E:\Desktop\code\data\{keyword}_douyin_video_data.xlsx"
            df.to_excel(excel_filename, index=False)
            
            print(f"数据已保存到 {excel_filename}")
            print(f"总共爬取了 {len(all_results)} 条数据")
        else:
            print("没有获取到任何数据")


# import time
# import pandas as pd
# from tqdm import tqdm
# import os

# def load_existing_data(filepath):
#     """Load existing data if file exists"""
#     if os.path.exists(filepath):
#         return pd.read_excel(filepath)
#     return pd.DataFrame()

# def main():
#     date = time.strftime("%Y-%m-%d", time.localtime())
#     crawler = Crawlers()
#     keywords = ['农村生活', '我的乡村生活', '田园生活']
    
#     for keyword in keywords:
#         all_results = []  # Reset for each keyword
#         excel_filename = f"E:\\Desktop\\code\\data\\{keyword}_douyin_video_data.xlsx"
        
#         # Load existing data
#         existing_df = load_existing_data(excel_filename)
#         existing_videos = set(existing_df['video_url']) if not existing_df.empty else set()
        
#         # Crawl new data
#         for i in tqdm(range(0, 100), desc=f"Crawling {keyword}"):
#             results, _ = crawler.douyin_search_video(keyword, count=20, offset=i)
            
#             if len(results) == 0:
#                 print(f'抖音: {keyword} 第 {i} 页无数据')
#                 break
            
#             # Filter out duplicates
#             new_results = [r for r in results if r['video_url'] not in existing_videos]
#             all_results.extend(new_results)
            
#             # Update existing videos set to avoid duplicates within current crawl
#             existing_videos.update(r['video_url'] for r in new_results)

#         # Process and save data
#         if all_results:
#             # Create DataFrame for new data
#             new_df = pd.DataFrame(all_results)
            
#             # Define column order
#             columns = [
#                 'author', 
#                 'video_title', 
#                 'video_create_time',
#                 'digg', 
#                 'comment', 
#                 'share', 
#                 'collect',
#                 'flower_count',
#                 'sec_uid',
#                 'video_url',
#                 # 'ip_position'
#             ]
#             new_df = new_df[columns]
            
#             # Combine with existing data
#             final_df = pd.concat([existing_df, new_df], ignore_index=True) if not existing_df.empty else new_df
            
#             # Save to Excel
#             final_df.to_excel(excel_filename, index=False)
            
#             print(f"{keyword} 数据已保存到 {excel_filename}")
#             print(f"新增 {len(new_df)} 条数据，总计 {len(final_df)} 条数据")
#         else:
#             print(f"{keyword} 没有获取到新数据")

# if __name__ == '__main__':
#     main()


# import time
# import pandas as pd
# from tqdm import tqdm
# import os

# def load_existing_data(filepath):
#     """加载已有数据（如果文件存在）"""
#     if os.path.exists(filepath):
#         return pd.read_excel(filepath)
#     return pd.DataFrame()

# def remove_duplicates_in_current_crawl(results, existing_urls):
#     """去重：剔除当前批次中已存在的URL，并更新existing_urls"""
#     unique_results = []
#     for item in results:
#         if item['video_url'] not in existing_urls:
#             unique_results.append(item)
#             existing_urls.add(item['video_url'])  # 更新已有URL集合
#     return unique_results

# def main():
#     date = time.strftime("%Y-%m-%d", time.localtime())
#     crawler = Crawlers()
#     keywords = ['农村故事', '我的乡村生活', '田园生活']
    
#     for keyword in keywords:
#         all_results = []  # 存储当前爬取的所有数据（已去重）
#         excel_filename = f"E:\\Desktop\\code\\data\\{keyword}_douyin_video_data.xlsx"
        
#         # 1. 加载历史数据，并提取已有视频URL（用于去重）
#         existing_df = load_existing_data(excel_filename)
#         existing_urls = set(existing_df['video_url']) if not existing_df.empty else set()
        
#         # 2. 爬取新数据（带进度条）
#         for i in tqdm(range(0, 100), desc=f"正在爬取 {keyword}"):
#             results, _ = crawler.douyin_search_video(keyword, count=30, offset=0)
            
#             if not results:  # 如果无数据，终止爬取
#                 print(f"抖音: {keyword} 第 {i} 页无数据，终止爬取")
#                 break
            
#             # 3. 当前批次去重（剔除已爬取的视频）
#             unique_results = remove_duplicates_in_current_crawl(results, existing_urls)
#             all_results.extend(unique_results)  # 加入总结果
#             time.sleep(100)  # 控制爬取频率
#             break

#         # 4. 合并新旧数据并保存
#         if all_results:
#             new_df = pd.DataFrame(all_results)
            
#             # 定义列顺序
#             columns = [
#                 'author', 
#                 'video_title', 
#                 'video_create_time',
#                 'digg', 
#                 'comment', 
#                 'share', 
#                 'collect',
#                 'flower_count',
#                 'sec_uid',
#                 'video_url',
#                 # 'ip_position'
#             ]
#             new_df = new_df[columns]  # 按指定顺序排列列
            
#             # 合并新旧数据
#             final_df = pd.concat([existing_df, new_df], ignore_index=True)
            
#             # 保存到Excel
#             final_df.to_excel(excel_filename, index=False)
            
#             print(f"[{date}] {keyword}: 新增 {len(new_df)} 条数据，总计 {len(final_df)} 条数据")
#         else:
#             print(f"[{date}] {keyword}: 无新增数据")

# if __name__ == '__main__':
#     main()