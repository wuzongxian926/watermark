# -*- coding: utf-8 -*-
import os
from Tkinter import *
import random
import time

reload(sys)
sys.setdefaultencoding('utf8')
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
        out = "out/" + output_title + u"_上集." + output_format
        return out

    def split_video_b(self, input_path='split/video.mp4', start='00:45:00'):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        output_format = self.get_input_format(input_path)
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " \
                   + "out/" + output_title + u"_下集." + output_format
        print(cmd_line)
        os.system(cmd_line)
        out = "out/" + output_title + u"_下集." + output_format
        return out

    def split_video(self, input_dir='split', split_time="02:25:00"):  # 仅需修改此处分割时间即可 *****************
        for parent, dirname, filename in os.walk(input_dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                temp_title = "temp" + str(random.randint(1, 100))
                temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                os.rename(path, temp_path)
                out_path = self.split_video_a(temp_path, split_time)
                ori_path = os.path.dirname(out_path) + "/" + original_name + "_上." + output_format
                os.rename(out_path, ori_path)
                out_path = self.split_video_b(temp_path, split_time)
                ori_path = os.path.dirname(out_path) + "/" + original_name + "_下." + output_format
                os.rename(out_path, ori_path)
                os.rename(temp_path, path)
        print u"视频分割完毕，到out文件夹查看"
        return 0

    def get_total_time(self, temp_path):
        cmd_line = "ffmpeg -i " + temp_path + "  2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
        duration = os.popen(cmd_line).readlines()[0][0:8]

        return duration

    def get_time_list(self, duration, N):
        time_list = []
        start_time = "00:00:00"
        time_list.append(start_time)
        end_time = duration
        s_start_time = time.mktime(time.strptime(start_time, '%H:%M:%S'))
        s_end_time = time.mktime(time.strptime(end_time, '%H:%M:%S'))
        total_s = s_end_time - s_start_time
        segment_one = total_s / N
        for n_i in range(N - 1):
            end_segment = (n_i + 1) * segment_one + s_start_time
            print end_segment
            print "*****************"
            end_segment_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_segment))[-8:]
            print end_segment_time
            time_list.append(end_segment_time)
        time_list.append(end_time)

        return time_list

    def split_extract_video(self, input_path, start_time, end_time, segmentsNO):

        input_title = self.get_input_title(input_path)
        output_title = input_title
        output_format = self.get_input_format(input_path)
        print end_time
        print input_path
        print output_title
        print str(segmentsNO)
        print output_format
        cmd_line = "ffmpeg -ss " + str(start_time) + " -i " + input_path + \
                   " -vcodec copy -acodec copy " + " -t " + str(end_time) + " -y " + "out/" + output_title + str(
            segmentsNO) + u"集." + output_format
        print(cmd_line)
        os.system(cmd_line)
        out = "out/" + output_title + str(segmentsNO) + u"集." + output_format
        return out

    def split_n_video(self, input_dir='split'):  # 仅需修改此处分割时间即可 *****************
        N = self.contents.get()
        N = int(N)

        print N
        print('the N is : ', self.contents.get())
        for parent, dirname, filename in os.walk(input_dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                temp_title = "temp" + str(random.randint(1, 100))
                temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                os.rename(path, temp_path)
                duration = self.get_total_time(temp_path)
                print N
                time_list = self.get_time_list(duration, N)
                for i_N in range(N):
                    out_path = self.split_extract_video(temp_path, time_list[i_N], time_list[1], i_N + 1)
                    ori_path = os.path.dirname(out_path) + "/" + original_name + str(i_N + 1) + "." + output_format
                    os.rename(out_path, ori_path)
                os.rename(temp_path, path)
        print u"视频分割完毕，到out文件夹查看"
        return 0

    def extract_video(self, input_dir='split'):  # 仅需修改此处分割时间即可 *****************
        start = self.contentsstart.get()
        end = self.contentsend.get()

        for parent, dirname, filename in os.walk(input_dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                temp_title = "temp" + str(random.randint(1, 100))
                temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                os.rename(path, temp_path)

                out_path = self.split_extract_video(temp_path, start, end, 101)
                ori_path = os.path.dirname(out_path) + "/" + original_name + str(101) + "." + output_format
                os.rename(out_path, ori_path)
                os.rename(temp_path, path)
        print u"视频提取完毕，到out文件夹查看"
        return 0

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.createWidgets()

        self.lable_infoN = Label(self, text="输入等分割段数N进行分割")
        self.lable_infoN.pack()
        self.entrythingy = Entry(self)
        self.entrythingy.pack()

        self.button = Button(self, text="1.开始N等分",
                             command=self.split_n_video)
        self.button.pack()

        self.contents = StringVar()
        self.contents.set("2")
        self.entrythingy.config(textvariable=self.contents)
        ##################################################################
        self.lable_info = Label(self, text="输入起始时间如00:06:08")
        self.lable_info.pack()
        self.entrystart = Entry(self)
        self.entrystart.pack()
        self.contentsstart = StringVar()
        self.contentsstart.set("00:06:08")
        self.entrystart.config(textvariable=self.contentsstart)

        self.lable_info2 = Label(self, text="输入持续时间00:10:00")
        self.lable_info2.pack()
        self.entryend = Entry(self)
        self.entryend.pack()
        self.contentsend = StringVar()
        self.contentsend.set("00:10:00")
        self.entryend.config(textvariable=self.contentsend)

        self.buttonstart = Button(self, text="2.开始提取片段", command=self.extract_video)
        self.buttonstart.pack()

    def createWidgets(self):

        pass


root = Tk()

w = Label(root, text="视频分割")
w.pack()
app = Application(master=root)
doc = Label(root, text="视频放置于split文件夹 ", fg="red")
doc.pack()
app.mainloop()
