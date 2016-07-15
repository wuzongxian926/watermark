# -*- coding: utf-8 -*-
import os
import random
from Tkinter import *
import time

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
        os.makedirs(FILE_PATH)
    return 0


file_path('combine')
file_path('out/nodelete')
file_path('split')
file_path('out')
file_path('temp')


class Application(Frame):
    def get_input_title(self, path):
        file = os.path.basename(path)
        file_name = os.path.splitext(file)[0]
        return file_name

    def get_input_format(self, path):
        format = os.path.basename(path).split('.')[-1]
        return format

    def combine_all_video(self, dir="combine"):
        global original_name, path, output_format
        video = []
        video_path = []
        del_true = 0  # 0删除split 1 留下split
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                print path
                input_format = self.get_input_format(path)
                output_format = input_format
                if input_format == "mp4" or input_format == 'MP4':
                    original_name = self.get_input_title(path)
                    video_path.append(path)
                else:
                    print "not mp4 file"
        video_path = sorted(video_path)
        for video_path_item in video_path:
            temp_title = "temp" + str(random.randint(1, 100000))
            temp_path = os.path.dirname(video_path_item) + "/" + temp_title + "." + output_format
            os.rename(video_path_item, temp_path)
            video.append(temp_path)
        if len(video) != 0:
            input_title = self.get_input_title(video[0])
            input_format = self.get_input_format(video[0])
            output = input_title
            output_format = input_format
            number = 1
            for sub_video in video:
                cmd_line = "ffmpeg -i " + sub_video + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_" + str(
                    number) + ".ts"
                os.system(cmd_line)
                if del_true == 0:
                    os.remove(sub_video)
                number += 1
            file_str = ""
            for file_i in range(len(video) - 1):
                file_str += "temp/" + output + "_" + str(file_i + 1) + ".ts|"
            file_str += "temp/" + output + "_" + str(len(video)) + ".ts"
            cmd_line = "ffmpeg -i \"concat:" + file_str + "\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + "." + output_format
            print(cmd_line)
            os.system(cmd_line)
            for temp_i in range(len(video)):
                os.remove("temp/" + output + "_" + str(temp_i + 1) + ".ts")
            output_path = "out/" + output + "." + output_format
            ori_path = os.path.dirname(output_path) + "/" + original_name + "合并." + output_format
            os.rename(output_path, ori_path)
            print(u'合并完毕前往out查看')
        else:
            print u"combine 空"
        return 0

    def split_video_for_1_mask(self, input_path='download/20150115.mp4', start='00:00:20', end="00:01:00"):  # 第一段视频
        input_title = self.get_input_title(input_path)
        output_title = input_title
        print output_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + " -t " + end + " -i " + input_path + " -vcodec copy -acodec copy -y " + "temp/" + output_title + "." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_1_combine(self, input_path='download/20150115.mp4', start='00:01:00'):  # 第二段视频
        end = '00:16:00'
        input_title = self.get_input_title(input_path)
        output_title = input_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + " -t " + end + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "temp/combine_" + output_title + "_2." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_2_combine(self, input_path='download/20150115.mp4',
                                    start='00:18:00'):  # 第三段视频##############################广告后重叠部分控制00:08:00
        input_title = self.get_input_title(input_path)
        output_title = input_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "temp/combine_" + output_title + "_3." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def just_2_mask(self, video_path='temp/mask_1.mp4'):  # 对第一段40秒视频加水印
        input_title = self.get_input_title(video_path)
        output_title = input_title
        input_format = self.get_input_format(video_path)
        output_format = input_format
        cmd_line = "ffmpeg -y -t 40 -i " + video_path + " -i temp/watermark.png -i temp/daleloogn.png -filter_complex \"overlay=x=if(lt(mod(t\,20)\,10)\,W-w-10\,NAN ):y=H-h-10,overlay=x=if(gt(mod(t\,20)\,10)\,W-w-10\,NAN ) :y=H-h-10\" -strict -2 temp/combine_" + output_title + "_1." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def combine_4b_video(self, video0='temp/720.mp4', video1='temp/combine_1.mp4', video2='temp/combine_2.mp4',
                         video3='temp/combine_3.mp4'):
        input_title = self.get_input_title(video1)
        output_title = input_title.split("_")[0]
        input_format = self.get_input_format(video1)
        output_format = input_format
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_0.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_3.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/ts" + output_title + "_0.ts|temp/ts" + output_title + "_1.ts|temp/ts" + output_title + "_2.ts|temp/ts" + output_title + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/out" + output_title + "_b." + output_format
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/ts" + output_title + "_0.ts")
        os.remove("temp/ts" + output_title + "_1.ts")
        os.remove("temp/ts" + output_title + "_2.ts")
        os.remove("temp/ts" + output_title + "_3.ts")
        out = "out/out" + output_title + "_b." + output_format
        return out

    def detect_720_or_1080(self, video_path):
        cmd_line = "ffmpeg -i " + video_path + " 2>&1 | perl -lane 'print $1 if /([0-9]{2,}x[0-9]+)/'"
        print cmd_line
        print os.popen(cmd_line).readlines()
        size = os.popen(cmd_line).readlines()[0]
        return size

    def generatGIF(self, PATH='VIDEO——PATH', start_time="00:08:00"):  # 生成GIF封面图 时间为从00:22:20开始截取2秒钟
        # start_time = "00:00:40"  # 时间为从00:01:08开始
        dur_time = "8"  # 截取2秒钟
        random_title = str(random.randint(0, 1000))
        watermark_path = "temp/acfun.png"
        cmd_line = "ffmpeg -ss " + start_time + " -t " + dur_time + " -i " + PATH + " -r 1 -s 480*270 -vf \"movie=" + watermark_path + " [watermark]; [in][watermark] overlay=x=10:y=H-h-10 [out]\" -f gif out/" + random_title + ".gif"
        # cmd_line = "ffmpeg -ss " + start_time + " -t " + dur_time + " -i " + PATH + " -r 1 -s 480*270 -f gif out/" + random_title + ".gif"
        print cmd_line
        os.system(cmd_line)
        gif_path = "out/" + random_title + ".gif"
        return gif_path

    def batch_generatGIF(self, dir='out'):
        start_time = self.gifcontents.get()
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                if (input_format == "mp4") and not ('nodelete' in path):
                    output_format = input_format
                    original_name = self.get_input_title(path)
                    temp_title = "temp" + str(random.randint(1, 10000))
                    temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                    os.rename(path, temp_path)
                    print path
                    print(temp_path)
                    gif_path = self.generatGIF(temp_path, start_time)
                    os.rename(temp_path, path)
                    gif_formal_path = "out/GIF" + original_name + ".gif"
                    os.rename(gif_path, gif_formal_path)
        print u"GIF封面图生成完毕，前往out文件夹查看"
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
        cmd_line = "ffmpeg -ss " + str(start_time) + " -i " + input_path + \
                   " -vcodec copy -acodec copy " + " -t " + str(end_time) + " -y " + "out/" + output_title + "_" + str(
            segmentsNO) + "part." + output_format
        os.system(cmd_line)
        out = "out/" + output_title + "_"+str(segmentsNO) + "part." + output_format
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

    def createWidgets(self):
        pass

    def generate_acfun(self, temp_path, size, ad_duration_seconds, ssy720contents_point,original_name):
        print (temp_path, size, ad_duration_seconds, ssy720contents_point)
        total_duration = self.get_total_time(temp_path)
        out1 = self.split_extract_video(temp_path, start_time='00:00:20', end_time=ssy720contents_point, segmentsNO=1)
        out2 = self.split_extract_video(temp_path, start_time=ssy720contents_point, end_time=total_duration,
                                        segmentsNO=2)
        print"8*******"
        print out1
        print out2
        if '1080' in size:
            middle_ad = 'temp/1080_' + ad_duration_seconds + '.mp4'
        else:
            middle_ad = 'temp/720_' + ad_duration_seconds + '.mp4'
        input_title = self.get_input_title(out1)
        output_title = input_title.split("_")[0]
        input_format = self.get_input_format(out1)
        output_format = input_format
        cmd_line = "ffmpeg -i " + out1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_0.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + middle_ad + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + out2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/ts" + output_title + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/ts" + output_title + "_0.ts|temp/ts" + output_title + "_1.ts|temp/ts" + output_title + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/out" + output_title + "_a." + output_format
        print(cmd_line)
        os.system(cmd_line)
        dest_path="out/ORIGINAL"+original_name+'.mp4'
        os.rename(temp_path,dest_path)
        os.remove(out1)
        os.remove(out2)
        os.remove("temp/ts" + output_title + "_0.ts")
        os.remove("temp/ts" + output_title + "_1.ts")
        os.remove("temp/ts" + output_title + "_2.ts")
        temp_out_path = "out/out" + output_title + "_a." + output_format
        return temp_out_path

    def batch_mask(self, dir='out'):
        duration_seconds = self.duration_contents.get()
        print duration_seconds
        ssy720contents_point = self.ssy720contents_point.get()
        print ssy720contents_point
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                if (input_format == 'mp4' or input_format == 'MP4') and not ("nodelete" in path) and not (
                            "BAIDU" in original_name) and not (
                            "AcFun" in original_name) and not ("ORIGINAL"in original_name):
                    temp_title = "temp" + str(random.randint(1, 10000))
                    temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                    os.rename(path, temp_path)
                    print path
                    print(temp_path)
                    size = self.detect_720_or_1080(temp_path)
                    gif_path = self.generatGIF(temp_path)
                    gif_formal_path = "out/GIF" + original_name + ".gif"
                    os.rename(gif_path, gif_formal_path)
                    self.split_video_for_1_mask(temp_path)
                    self.split_video_for_2_1_combine(temp_path)
                    self.split_video_for_2_2_combine(temp_path)
                    temp_path = self.generate_acfun(temp_path, size, duration_seconds, ssy720contents_point,original_name)
                    out_path = "out/AcFun" + original_name + "." + output_format
                    os.rename(temp_path, out_path)
                    file = temp_title + "." + output_format
                    self.just_2_mask('temp/' + file)
                    os.remove('temp/' + file)
                    if '1080' in size:
                        video0 = 'temp/1080.mp4'
                    else:
                        video0 = 'temp/720.mp4'
                    video1 = "temp/combine_" + file.split('.')[0] + "_1." + output_format
                    video2 = "temp/combine_" + file.split('.')[0] + "_2." + output_format
                    video3 = "temp/combine_" + file.split('.')[0] + "_3." + output_format
                    path = self.combine_4b_video(video0, video1, video2, video3)
                    ori_path = os.path.dirname(path) + "/BAIDU" + original_name + "." + output_format  # 含片头
                    os.rename(path, ori_path)
                    os.remove(video1)
                    os.remove(video2)
                    os.remove(video3)
                print u"水印制作完毕，前往out文件夹查看"
            else:
                print u"非加水印视频"
        else:
            print u"非加水印对象"
        return 0

    def __init__(self, master=None):
        self.frm=Frame.__init__(self, master)
        
        self.left=Frame(self.frm)
        self.left_top=Frame(self.left)
        self.left_top.pack(side=TOP)
        self.left_down=Frame(self.left)
        self.left_down.pack(side=TOP)
        self.left.pack(side=LEFT)
        
        self.right=Frame(self.frm)
        self.right_top=Frame(self.right)
        self.right_top.pack(side=TOP)
        self.right_down=Frame(self.right)
        self.right_down.pack(side=TOP)
        self.right.pack(side=RIGHT)



        
        self.doc_lable_combine = Label(self.left_top, text="注意：按a、b、c、d、e、f排序", fg="red")
        self.doc_lable_combine.pack(side=TOP)
        self.ssycom = Button(self.left_top)
        self.ssycom["text"] = "合并文件夹所有视频",
        self.ssycom["command"] = self.combine_all_video
        self.ssycom.pack(side=TOP)
        self.doc_lable_combine2 = Label(self.left_top, text="需合并的文件放置于【combine】文件夹", fg="red")
        self.doc_lable_combine2.pack(side=TOP)
        self.doc_seg1 = Label(self.left_top, text="-------------------------------", fg="blue")
        self.doc_seg1.pack(side=TOP)
        
        self.doc = Label(self.left_down, text="输入acfun片头长度5s或10s", fg="red")
        self.doc.pack(side=TOP)
        self.ssy720entrythingy = Entry(self.left_down)
        self.ssy720entrythingy.pack(side=TOP)
        self.duration_contents = StringVar()
        self.duration_contents.set("5s")
        self.ssy720entrythingy.config(textvariable=self.duration_contents)
        self.doc_point = Label(self.left_down, text="输入acfun片头插入位置", fg="red")
        self.doc_point.pack(side=TOP)
        self.ssy720entrythingy_point = Entry(self.left_down)
        self.ssy720entrythingy_point.pack(side=TOP)
        self.ssy720contents_point = StringVar()
        self.ssy720contents_point.set("00:20:20")
        self.ssy720entrythingy_point.config(textvariable=self.ssy720contents_point)
        self.ssy720 = Button(self.left_down)
        self.ssy720["text"] = "自动识别尺寸加水印",
        self.ssy720["command"] = self.batch_mask
        self.ssy720.pack(side=TOP)
        self.doc = Label(self.left_down, text="视频放置于【out】文件夹", fg="red")
        self.doc.pack(side=TOP)
       




        self.doc_lable_seg3 = Label(self.left_down, text="----------------------------------------", fg="green")
        self.doc_lable_seg3.pack(side=TOP)


        self.giflable_infoN = Label(self.left_down, text="输入开始生成时间点", fg="red")
        self.giflable_infoN.pack(side=TOP)
        self.gifentrythingy = Entry(self.left_down)
        self.gifentrythingy.pack(side=TOP)
        self.gifbutton = Button(self.left_down, text="开始单独生成GIF",
                                command=self.batch_generatGIF)
        self.gifbutton.pack(side=TOP)
        self.gifcontents = StringVar()
        self.gifcontents.set("00:06:08")
        self.gifentrythingy.config(textvariable=self.gifcontents)
        self.doc_lable_gif2 = Label(self.left_down, text="视频放置于【out】文件夹", fg="red")
        self.doc_lable_gif2.pack(side=TOP)



        self.doc_lable_split = Label(self.right_top, text="视频放置于【split】文件夹", fg="red")
        self.doc_lable_split.pack(side=TOP)
        self.lable_infoN = Label(self.right_top, text="输入等分割段数N进行分割", fg="red")
        self.lable_infoN.pack(side=TOP)
        self.entrythingy = Entry(self.right_top)
        self.entrythingy.pack(side=TOP)
        self.button = Button(self.right_top, text="1.开始N等分",
                             command=self.split_n_video)
        self.button.pack(side=TOP)
        self.contents = StringVar()
        self.contents.set("2")
        self.entrythingy.config(textvariable=self.contents)
        self.doc_lable_seg4 = Label(self.right_top, text="----------------------************--------------------", fg="green")
        self.doc_lable_seg4.pack(side=TOP)

        self.lable_info = Label(self.right_down, text="输入起始时间如00:06:08", fg="red")
        self.lable_info.pack(side=TOP)
        self.entrystart = Entry(self.right_down)
        self.entrystart.pack(side=TOP)
        self.contentsstart = StringVar()
        self.contentsstart.set("00:06:08")
        self.entrystart.config(textvariable=self.contentsstart)
        self.lable_info2 = Label(self.right_down, text="输入持续时间00:10:00", fg="red")
        self.lable_info2.pack(side=TOP)
        self.entryend = Entry(self.right_down)
        self.entryend.pack(side=TOP)
        self.contentsend = StringVar()
        self.contentsend.set("00:10:00")
        self.entryend.config(textvariable=self.contentsend)
        self.buttonstart = Button(self.right_down, text="2.开始提取片段", command=self.extract_video)
        self.buttonstart.pack(side=TOP)
        self.doc_lable_split = Label(self.right_down, text="视频放置于【split】文件夹 ", fg="red")
        self.doc_lable_split.pack(side=TOP)
        self.doc_lable_seg5 = Label(self.right_down, text="--------------------------------------------------------", fg="green")
        self.doc_lable_seg5.pack(side=TOP)


root = Tk()
root.title("视频简易处理")
app = Application(master=root)
app.mainloop()
