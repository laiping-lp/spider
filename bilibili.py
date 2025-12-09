# import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
#     'Accept': '*/*',
#     'Accept-Encoding': 'identity',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'Connection': 'keep-alive',
#     'Host': 'upos-sz-estgcos.bilivideo.com',
#     'If-Range': "11E2F9B401586C88CC697DB2313368C4",
#     'Origin': 'https://www.bilibili.com',
#     'Range': 'bytes=1072-84831',
#     'Referer': 'https://www.bilibili.com/video/BV1cE411u7jw/?spm_id_from=333.337.search-card.all.click&vd_source=81966291bbf1dec60c87778387a053dd',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'cross-site'
#     }

# # "Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"
# # sec-ch-ua-mobile
# # ?0
# # sec-ch-ua-platform
# # "Windows"
# # sec-fetch-dest
# # empty
# # sec-fetch-mode
# # cors
# # sec-fetch-site
# # cross-site

# # requestUrl = "https://upos-sz-estgcos.bilivideo.com/upgcxcode/28/19/161811928/161811928-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=cc6daf84ffda4641b0d0aff5d9e9af0u&oi=3084839749&deadline=1765300085&gen=playurlv3&os=estgcos&og=cos&mid=398164244&nbs=1&uipk=5&platform=pc&upsig=9abd21026bfe50fdda83c69dcef9c8ad&uparams=e,trid,oi,deadline,gen,os,og,mid,nbs,uipk,platform&bvc=vod&nettype=0&bw=2920223&dl=0&f=u_0_0&agrr=0&buvid=466B8E43-9346-2D2F-0DF5-4C9D4570748B79418infoc&build=0&orderid=0,3"

# requestUrl = "https://upos-sz-estgoss.bilivideo.com/upgcxcode/28/19/161811928/161811928-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&uipk=5&trid=cc6daf84ffda4641b0d0aff5d9e9af0u&oi=3084839749&gen=playurlv3&og=ali&mid=398164244&deadline=1765300085&platform=pc&os=estgoss&upsig=278d3ad004810ec85c80f014a5366397&uparams=e,nbs,uipk,trid,oi,gen,og,mid,deadline,platform,os&bvc=vod&nettype=0&bw=135357&agrr=0&buvid=466B8E43-9346-2D2F-0DF5-4C9D4570748B79418infoc&build=0&dl=0&f=u_0_0&orderid=0,3"
                            

# # 发送请求（时间会稍长）
# resp = requests.get(requestUrl, headers=headers)
# headers = resp.headers
# # 数据保存
# print(resp)
# fo = open("video_audio.m4s", "wb")
# fo.write(resp.content)
# fo.close()
# print("结束")

# TODO 视频网址
url = 'https://www.bilibili.com/video/BV1cE411u7jw/'
headers = {
        # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
        # "Referer": "https://www.bilibili.com/video/BV1454y187Er/",
        "Referer": url,
        # User-Agent 用户代理, 表示浏览器/设备基本身份信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
import requests
# TODO 通过F12查看视频的地址
video_url = 'https://upos-sz-estgcos.bilivideo.com/upgcxcode/28/19/161811928/161811928-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=cc6daf84ffda4641b0d0aff5d9e9af0u&oi=3084839749&deadline=1765300085&gen=playurlv3&os=estgcos&og=cos&mid=398164244&nbs=1&uipk=5&platform=pc&upsig=9abd21026bfe50fdda83c69dcef9c8ad&uparams=e,trid,oi,deadline,gen,os,og,mid,nbs,uipk,platform&bvc=vod&nettype=0&bw=2920223&dl=0&f=u_0_0&agrr=0&buvid=466B8E43-9346-2D2F-0DF5-4C9D4570748B79418infoc&build=0&orderid=0,3'

video_response = requests.get(video_url, headers=headers)
with open('video.mp4', mode='wb') as v:
    v.write(video_response.content)
    
# TODO 通过F12查看音频的地址
audio_url = 'https://upos-sz-estgoss.bilivideo.com/upgcxcode/28/19/161811928/161811928-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&uipk=5&trid=cc6daf84ffda4641b0d0aff5d9e9af0u&oi=3084839749&gen=playurlv3&og=ali&mid=398164244&deadline=1765300085&platform=pc&os=estgoss&upsig=278d3ad004810ec85c80f014a5366397&uparams=e,nbs,uipk,trid,oi,gen,og,mid,deadline,platform,os&bvc=vod&nettype=0&bw=135357&agrr=0&buvid=466B8E43-9346-2D2F-0DF5-4C9D4570748B79418infoc&build=0&dl=0&f=u_0_0&orderid=0,3'
audio_response = requests.get(audio_url, headers=headers)
with open('video_audio.mp3', mode='wb') as v:
    v.write(audio_response.content)
