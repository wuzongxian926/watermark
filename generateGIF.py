# -*- coding: utf-8 -*-
import os
import random
from Tkinter import *

reload(sys)
sys.setdefaultencoding('utf8')
flag = True
print u"你好!"


def file_path(FILE_PATH='/home/wuxy/aaa111/22222'):
    if os.path.isdir(FILE_PATH):
        print 'dir %s exists' % (FILE_PATH)
        pass
    else:
        print  'dir %s not exists' % (FILE_PATH)
        os.mkdir(FILE_PATH)
    return 0


file_path('out')


class Application(Frame):
    def get_input_title(self, path):
        file = os.path.basename(path)
        file_name = os.path.splitext(file)[0]
        return file_name

    def get_input_format(self, path):
        format = os.path.basename(path).split('.')[-1]
        print format
        return format

    def generatGIF(self, PATH='VIDEO——PATH'):  # 生成GIF封面图 时间为从00:02:20开始截取15秒钟
        start_time = "00:02:20"  # 时间为从00:02:20开始
        dur_time = "15"  # 截取15秒钟
        random_title=str(random.randint(0, 1000))
        cmd_line = "ffmpeg -ss " + start_time + " -t " + dur_time + " -i " + PATH + " -r 1 -s 480*270 -f gif out/" + random_title + ".gif"
        print cmd_line
        os.system(cmd_line)
        gif_path="out/" + random_title + ".gif"
        return gif_path

    def batch_generatGIF(self, dir='download'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                if input_format=="mp4":
                    output_format = input_format
                    original_name = self.get_input_title(path)
                    temp_title = "temp" + str(random.randint(1, 10000))
                    temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                    os.rename(path, temp_path)
                    print path
                    print(temp_path)
                    gif_path=self.generatGIF(temp_path)
                    os.rename(temp_path, path)
                    gif_formal_path="out/"+original_name+".gif"
                    os.rename(gif_path,gif_formal_path)
        print u"GIF封面图生成完毕，前往out文件夹查看"
        return 0

    def createWidgets(self):
        self.ssy720 = Button(self)
        self.ssy720["text"] = "生成gif",
        self.ssy720["command"] = self.batch_generatGIF
        self.ssy720.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
w = Label(root, text="watermarking")
w.pack()
app = Application(master=root)
doc = Label(root, text="单独生成GIF封面，视频放置于download文件夹", fg="red")
doc.pack()
app.mainloop()
