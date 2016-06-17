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


file_path('combine')
file_path('download')
file_path('download/720')
file_path('download/1080')
file_path('mask2')
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
        print format
        return format

    def split_video_for_1_mask(self, input_path='download/20150115.mp4', start='00:00:20', end="00:01:00"):  # 第一段视频
        input_title = self.get_input_title(input_path)
        output_title = input_title
        print output_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + " -t " + end + " -i " + input_path + " -vcodec copy -acodec copy -y " + "mask2/" + output_title + "." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_1_combine(self, input_path='download/20150115.mp4', start='00:01:00'):  # 第二段视频
        end = '00:16:00'
        input_title = self.get_input_title(input_path)
        output_title = input_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + " -t " + end + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "combine/" + output_title + "_2." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_2_combine(self, input_path='download/20150115.mp4', start='00:18:00'):  # 第三段视频##############################广告后重叠部分控制00:08:00
        input_title = self.get_input_title(input_path)
        output_title = input_title
        input_format = self.get_input_format(input_path)
        output_format = input_format
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "combine/" + output_title + "_3." + output_format
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def just_2_mask(self, video_path='mask2/1.mp4'):  # 对第一段40秒视频加水印
        input_title = self.get_input_title(video_path)
        output_title = input_title
        input_format = self.get_input_format(video_path)
        output_format = input_format
        cmd_line = "ffmpeg -y -t 40 -i " + video_path + " -i temp/watermark.png -i temp/daleloogn.png -filter_complex \"overlay=x=if(lt(mod(t\,20)\,10)\,W-w-10\,NAN ):y=H-h-10,overlay=x=if(gt(mod(t\,20)\,10)\,W-w-10\,NAN ) :y=H-h-10\" -strict -2 combine/" + output_title + "_1." + output_format
        print(cmd_line)

        os.system(cmd_line)
        return 0

    def combine_4b_video(self, video0='temp/720.mp4', video1='download/1.mp4', video2='download/2.mp4',
                         video3='download/3.mp4'):
        input_title = self.get_input_title(video1)
        output_title = input_title.split("_")[0]
        input_format = self.get_input_format(video1)
        output_format = input_format
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_0.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_1.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_2.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_3.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output_title + "_0.ts|temp/" + output_title + "_1.ts|temp/" + output_title + "_2.ts|temp/" + output_title + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output_title + "_b." + output_format
        print(cmd_line)

        os.system(cmd_line)
        os.remove("temp/" + output_title + "_0.ts")
        os.remove("temp/" + output_title + "_1.ts")
        os.remove("temp/" + output_title + "_2.ts")
        os.remove("temp/" + output_title + "_3.ts")
        out = "out/" + output_title + "_b." + output_format
        return out

    def combine_4a_video(self, video0='temp/720.mp4', video1='download/1.mp4', video2='download/2.mp4',
                         video3='download/3.mp4'):

        input_title = self.get_input_title(video1)
        output_title = input_title.split("_")[0]
        input_format = self.get_input_format(video1)
        output_format = input_format
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_0.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_1.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_2.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_3.ts"

        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output_title + "_0.ts|temp/" + output_title + "_1.ts|temp/" + output_title + "_2.ts|temp/" + output_title + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output_title + "_a." + output_format
        print(cmd_line)

        os.system(cmd_line)
        os.remove("temp/" + output_title + "_0.ts")
        os.remove("temp/" + output_title + "_1.ts")
        os.remove("temp/" + output_title + "_2.ts")
        os.remove("temp/" + output_title + "_3.ts")
        out = "out/" + output_title + "_a." + output_format
        return out

    def combine_3a_video(self,  video1='download/1.mp4', video2='download/2.mp4',
                             video3='download/3.mp4'):
        input_title = self.get_input_title(video1)
        output_title = input_title.split("_")[0]
        input_format = self.get_input_format(video1)
        output_format = input_format
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output_title + "_3.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output_title + "_1.ts|temp/" + output_title + "_2.ts|temp/" + output_title + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output_title + "_a." + output_format
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output_title + "_1.ts")
        os.remove("temp/" + output_title + "_2.ts")
        os.remove("temp/" + output_title + "_3.ts")
        out = "out/" + output_title + "_a." + output_format
        return out

    def generatGIF(self, PATH='VIDEO——PATH'):  # 生成GIF封面图 时间为从00:02:20开始截取3秒钟
        start_time = "00:02:20"  # 时间为从00:02:20开始
        dur_time = "9"  # 截取9秒钟
        random_title = str(random.randint(0, 1000))
        cmd_line = "ffmpeg -ss " + start_time + " -t " + dur_time + " -i " + PATH + " -r 1 -s 480*270 -f gif out/" + random_title + ".gif"
        print cmd_line
        os.system(cmd_line)
        gif_path = "out/" + random_title + ".gif"
        return gif_path

    def batch_mask720drm(self, dir='download/720'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                temp_title = "temp" + str(random.randint(1, 10000))
                temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                os.rename(path, temp_path)
                print path
                print(temp_path)
                gif_path = self.generatGIF(temp_path)
                gif_formal_path = "out/" + original_name + ".gif"
                os.rename(gif_path, gif_formal_path)
                self.split_video_for_1_mask(temp_path)
                self.split_video_for_2_1_combine(temp_path)
                self.split_video_for_2_2_combine(temp_path)
                os.rename(temp_path, path)
                # os.remove(path)
                file = temp_title + "." + output_format
                self.just_2_mask('mask2/' + file)
                os.remove('mask2/' + file)
                video0 = 'temp/720.mp4'  ##################################################720################
                video1 = "combine/" + file.split('.')[0] + "_1." + output_format
                video2 = "combine/" + file.split('.')[0] + "_2." + output_format
                video3 = "combine/" + file.split('.')[0] + "_3." + output_format
                path = self.combine_4a_video(video1, video2, video0, video3)#含片头
                # path = self.combine_3a_video(video1, video2, video3)#不含广告
                ori_path = os.path.dirname(path) + "/" + original_name + "acfun." + output_format
                os.rename(path, ori_path)
                path = self.combine_4b_video(video0, video1, video2, video3)
                ori_path = os.path.dirname(path) + "/" + original_name + "baidu." + output_format#含片头
                os.rename(path, ori_path)
                os.remove(video1)
                os.remove(video2)
                os.remove(video3)
        print u"水印制作完毕，前往out文件夹查看"
        return 0

    def batch_mask1080whd(self, dir='download/1080'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                input_format = self.get_input_format(path)
                output_format = input_format
                original_name = self.get_input_title(path)
                temp_title = "temp" + str(random.randint(1, 10000))
                temp_path = os.path.dirname(path) + "/" + temp_title + "." + output_format
                os.rename(path, temp_path)
                print path
                print(temp_path)
                gif_path = self.generatGIF(temp_path)
                gif_formal_path = "out/" + original_name + ".gif"
                os.rename(gif_path, gif_formal_path)
                self.split_video_for_1_mask(temp_path)
                self.split_video_for_2_1_combine(temp_path)
                self.split_video_for_2_2_combine(temp_path)
                os.rename(temp_path, path)
                # os.remove(path)
                file = temp_title + "." + output_format
                self.just_2_mask('mask2/' + file)
                os.remove('mask2/' + file)
                video0 = 'temp/1080.mp4'  ###################################################1080#######################
                video1 = "combine/" + file.split('.')[0] + "_1." + output_format
                video2 = "combine/" + file.split('.')[0] + "_2." + output_format
                video3 = "combine/" + file.split('.')[0] + "_3." + output_format
                path = self.combine_4a_video(video1, video2, video0, video3)#含片头
                # path = self.combine_3a_video(video1, video2, video3)  # 不含广告
                ori_path = os.path.dirname(path) + "/" + original_name + "acfun." + output_format
                os.rename(path, ori_path)
                path = self.combine_4b_video(video0, video1, video2, video3)
                ori_path = os.path.dirname(path) + "/" + original_name + "baidu." + output_format#含片头
                os.rename(path, ori_path)
                os.remove(video1)
                os.remove(video2)
                os.remove(video3)
        print u"水印制作完毕，前往out文件夹查看"
        return 0

    def createWidgets(self):
        self.ssy720 = Button(self)
        self.ssy720["text"] = "720加水印",
        self.ssy720["command"] = self.batch_mask720drm
        self.ssy720.pack({"side": "left"})
        self.ssy1080 = Button(self)
        self.ssy1080["text"] = "1080加水印",
        self.ssy1080["command"] = self.batch_mask1080whd
        self.ssy1080.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
w = Label(root, text="watermarking")
w.pack()
app = Application(master=root)
doc = Label(root, text="视频放置于【720】文件夹或者【1080】文件夹", fg="red")
doc.pack()
app.mainloop()
