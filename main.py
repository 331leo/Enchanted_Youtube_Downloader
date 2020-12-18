from __future__ import unicode_literals
import youtube_dl
import os
import datetime
import time
import wget
import shutil
import math
run_time=str(datetime.datetime.now())[:21].replace(":","_")

_ = os.system("title Youtube Downloader (Made By Leok.kr)")
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def bar_custom(current, total, width=80):
    width=30
    avail_dots = width-2
    shaded_dots = int(math.floor(float(current) / total * avail_dots))
    percent_bar = '[' + '■'*shaded_dots + ' '*(avail_dots-shaded_dots) + ']'
    progress = "%d%% %s [%d / %d]" % (current / total * 100, percent_bar, current, total)
    return progress

def checkffmpeg():
    if not os.path.isfile("ffmpeg.exe"):
        print("필수요소 ffmpeg 다운로드..")
        wget.download("https://leok.kr/file/ffmpeg.exe",bar=bar_custom)
        print("")
    if not os.path.isfile("ffprobe.exe"):
        print("필수요소 ffprobe 다운로드..")
        wget.download("https://leok.kr/file/ffprobe.exe",bar=bar_custom)
        print("")
    clear()

def download_from_file(o_type):
    o_type_human = "음악파일(mp3)"
    if o_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"./downloaed_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif o_type == "mp4":
        o_type_human = "mp4"
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': f"./downloaed_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
        {'key': 'FFmpegMetadata'},],
        }
    elif o_type == "ori_video":
        o_type_human = "원본영상으"
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': f"./downloaed_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{'key': 'FFmpegMetadata'},],
        }

    if not os.path.isfile(f"download.txt"):
        f = open(f"download.txt", "w")
        f.close()
        input(f"download.txt 파일이 존재하지 않습니다.\n해당 파일을 생성하였으니, 해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣으신후 다시 실행해 주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")

    else:
        f=open(f"download.txt","r")
        links = f.readlines()
        f.close()
        if len(links) >= 1:
            if len(links[0]) >= 5:
                print(f"download.txt 를 읽어와, {o_type} 다운로드를 시작합니다.")
                time.sleep(1)
                os.makedirs(f"./downloaed_{o_type}/{run_time}",exist_ok=True)

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(links)
                shutil.move(f"./download.txt",f"./downloaed_{o_type}/{run_time}/!downloaded_{o_type}_links.txt")
                print(f"다운로드가 완료되었습니다.\n프로그램 실행경로의 downloaded_{o_type}/{run_time} 에 저장하였습니다!\ndownload.txt 파일을 초기화 하였습니다!")
                f = open(f"download.txt", "w")
                f.close()
                input("> 엔터를 누르시면 메뉴로 돌아갑니다. ")
            else:
                input(f"download.txt 파일이 비어있습니다.\n해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣어주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")
        else:
            input(f"download.txt 파일이 비어있습니다.\n해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣어주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")


def menu():
    modes=["음악 다운로드 모드", "영상 다운로드 모드"]
    print("프로그램 동작 모드를 선택하세요.")
    print("[1] 음악 다운로드 모드")
    print("[2] 영상 다운로드 모드(포멧: mkv)")
    print("[3] 영상 다운로드 모드(강제 mp4변환, 오래걸림)")
    print("[q] 종료")
    c = input("> ")
    clear()
    if c == "1":
        download_from_file("mp3")
    elif c == "2":
        download_from_file("ori_video")
    elif c == "3":
        download_from_file("mp4")

    elif c == "q":
        return 0
    clear()

checkffmpeg()
clear()
while True:
    if menu() == 0:
        break