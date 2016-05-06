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
        os.mkdir(FILE_PATH)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误
        print 'mkdir ok'
    return 0


file_path('combine')
file_path('temp')
file_path('out')


class Application(Frame):
    def get_input_title(self, path):
        file = os.path.basename(path)
        file_name = os.path.splitext(file)[0]
        return file_name

    def get_input_format(self, path):
        format = os.path.basename(path).split('.')[-1]
        return format

    def combine_video(self, dir="combine"):
        video1 = ''
        video2 = ''
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                if video1 == '':
                    video1 = path
                else:
                    video2 = path
        input_title1 = self.get_input_title(video1)
        input_title2 = self.get_input_title(video2)
        input_format=self.get_input_format(video1)
        output = input_title1 + input_title2
        output_format=input_format
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_1.ts|temp/" + output + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + "."+output_format
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        print(u'合并完毕前往out查看')
        return 0

    def createWidgets(self):
        self.ssycom = Button(self)
        self.ssycom["text"] = "合并视频",
        self.ssycom["command"] = self.combine_video
        self.ssycom.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
w = Label(root, text="watermarking")
w.pack()
app = Application(master=root)
doc = Label(root, text="需合并的两个文件放置于combine文件夹", fg="red")
doc.pack()
app.mainloop()