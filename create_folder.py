import os
import time
def create(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print('文件夹创建完成  ' + path)

time_now = time.strftime("%Y-%m-%d", time.localtime())
print(time_now[:10])
path = time_now
create(path)
youtube_path = "youtube_videos"
douyin_path = "douyin_videos"
output_path = "ouput_videos"
srt_path = "srt_file"
audio_path = "audio_file"
create(path+'/'+youtube_path)
create(path+'/'+douyin_path)
create(path+'/'+output_path)
create(path+'/'+srt_path)
create(path+'/'+audio_path)