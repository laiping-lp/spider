chromedriver.exe 将该文件放置在虚拟环境目录下
run.py 文件用于运行以下多个文件
create_folder.py 按每日日期生成相应文件夹用于存储各类视频
crawlers_videos.py 文件用于抓取抖音/YouTube网站视频并下载（运行此文件时需要挂梯子）
main.py 用于对抖音下载的小说推文视频进行字幕提取,生成srt文件
sop.py 文件用于文案改写,合成音频,合成视频
click.py 模拟点击剪映生成最终视频并发布,在对于第一个视频的选择时时，需要选择视频路径以及导出路径，之后默认上述路径。其中字幕识别的时间为120s和导出时间为90s，如不合理请更改（注：上述文件的鼠标点击坐标均为1920x1080尺寸下坐标，如有疑问可联系我修改，并且运行此文件时，需先打开软件，并登录抖音账号，且需保证后一个窗口为剪映窗口）
requirements.txt 为项目所需依赖
运行顺序
1.用git clone下载转字幕文件于本目录下
git clone git@github.com:YaoFANGUK/video-subtitle-generator.git
将此目录下的main.py 替换 video-subtitle-generator/backend/main.py main.py
2.创建虚拟环境
conda create -n sop python=3.9
3.安装依赖文件
pip install -r requirements.txt
（若有安装失败，麻烦手动安装一下）
安装torch最好手动安装
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
4.进入虚拟环境
conda activate sop
5.进入项目所在目录
cd path
6.将chromedriver.exe文件放置在虚拟环境目录下
7.运行run.py 一步到位
8.运行完run.py文件生成视频后，运行click.py文件实现剪映操作
click.py位于上一级目录