import time
from LAC import LAC
import pysrt
import random
from moviepy.editor import *
import pyttsx3
import os
import csv
import pandas as pd

class SOP(object):
    def __init__(self):
        print("初始化SOP模块")
    
    # 提取为文本
    def srt_content(self,file_path):
        srt = pysrt.open(file_path)
        content = ''
        for i in range(len(srt)):
            content += srt.data[i].text
            content += '，'
        return srt , content

    # 提取文本中人名
    def lac_username(self,sentences):
        # 装载LAC模型
        user_name_list = []
        lac = LAC(mode="lac")
        lac_result = lac.run(sentences)
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "PER":
                user_name_list.append(lac_result[0][index])
        print("人名提取done！")
        return user_name_list

    # 对文案出现人名去重
    def name_de_weight(self,user_name_list):
        new_lac_user = []
        for i in user_name_list:
            if i not in new_lac_user:
                new_lac_user.append(i)
        with open("name.csv",'a+',encoding="utf-8",newline='') as file:
            writer = csv.writer(file)
            for item in new_lac_user:
                writer.writerow([item])
        print("人名去重done！")
        return new_lac_user

    # 将人名打乱互相替换
    def name_modification(self,srt_path):
        srt , content = self.srt_content(srt_path)
        user_name_list = self.lac_username(content)
        new_lac_user = self.name_de_weight(user_name_list)
        name_lsit = pd.read_csv("name.csv",header=None).values.tolist()
        random.shuffle(name_lsit)
        for old_word, new_word in zip(new_lac_user,name_lsit):
            content = content.replace(old_word,new_word[0])
        print("文案修改done！")
        return content

    # 对文案合成音频
    def subtitle_speech(self,content , audio_file_path):
        engine = pyttsx3.init()
        # 调整频率
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate+50)
        # 调整音量
        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume+0.5)
        engine.save_to_file(content,audio_file_path)
        engine.runAndWait()
        print("音频合成done！")

    # 将音频和视频生成视频
    def videocaption(self,input_video,audio_file_path,out_file):
        #	加载视频
        video = VideoFileClip(input_video)
        # 加载音频
        audio = AudioFileClip(audio_file_path)

        print(audio.duration)
        print(video.duration)
        if audio.duration > video.duration:
            audio = audio.set_duration(video.duration)
        else:
            video = video.set_duration(audio.duration)
        final_clip = video.set_audio(audio)
        final_clip.write_videofile(out_file)
        print("音频视频合成done！")

if __name__ == '__main__':
    sop = SOP()
    date = time.strftime("%Y-%m-%d", time.localtime())
    srt_file_path = date + "/srt_file"
    youtube_path = date + "/youtube_videos"
    output_path = date + "/ouput_videos/"
    audio_path = date + "/audio_file/"
    for srt_path, input_video in zip(os.listdir(srt_file_path),os.listdir(youtube_path)):
        srt_path = srt_file_path + '/' +  srt_path
        input_video = youtube_path + '/' + input_video
        print(srt_path,input_video)
        time_now = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
        audio_file_path = audio_path + time_now +'.mp3' 
        content = sop.name_modification(srt_path)
        sop.subtitle_speech(content , audio_file_path)
        out_file = output_path + time_now +'.mp4'
        sop.videocaption(input_video, audio_file_path, out_file)
        break