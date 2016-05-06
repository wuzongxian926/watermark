# -*- coding: utf-8 -*-
import os
from Tkinter import *

reload(sys)
sys.setdefaultencoding('gbk')
flag = True
print u"你好!"


def file_path(FILE_PATH='/home/wuxy/aaa111/22222'):
    if os.path.isdir(FILE_PATH):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
        print 'dir %s exists' % (FILE_PATH)
        pass
    else:
        print  'dir %s not exists' % (FILE_PATH)
        os.mkdir(FILE_PATH)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误         print 'mkdir ok
    return 0


file_path('split')
file_path('out')


class Application(Frame):
    def get_input_title(self, path):
        file = os.path.basename(path)
        file_name = os.path.splitext(file)[0]
        return file_name

    def get_input_format(self, path):
        format = os.path.basename(path).split('.')[-1]
        return format

    def split_video_a(self, input_path='split/video.mp4', end="00:45:00"):
        start = '00:00:00'
        input_title = self.get_input_title(input_path)
        output_title = input_title
        output_format = self.get_input_format(input_path)
        cmd_line = "ffmpeg -ss " + start + " -t " + end + " -i " + input_path + \
                   " -vcodec copy -acodec copy -y " + "out/" + output_title + u"_上集." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_b(self, input_path='split/video.mp4', start='00:45:00'):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        output_format = self.get_input_format(input_path)
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " \
                   + "out/" + output_title + u"_下集." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video(self, input_dir='split', split_time="00:45:00"):  # 仅需修改此处分割时间即可 *****************
        for parent, dirname, filename in os.walk(input_dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                self.split_video_a(path, split_time)
                self.split_video_b(path, split_time)
        print u"视频分割完毕，到out文件夹查看"
        return 0

    def createWidgets(self):
        self.ssyspl = Button(self)
        self.ssyspl["text"] = u"分割视频",
        self.ssyspl["command"] = self.split_video
        self.ssyspl.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
w = Label(root, text="watermarking")
w.pack()
app = Application(master=root)
doc = Label(root, text="视频放置于split文件夹 ", fg="red")
doc.pack()
app.mainloop()
