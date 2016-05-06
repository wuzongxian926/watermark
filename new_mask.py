# -*- coding: utf-8 -*-
from Tkinter import *
import os

reload(sys)
sys.setdefaultencoding('gbk')
flag = True
print u"你好!"


class Application(Frame):
    def get_title(self, origin_title_str='asdad20151314.mp3'):
        number_title = filter(lambda x: x.isdigit(), origin_title_str)
        title = str(number_title)
        return title

    def get_input_title(self, path):
        file_name = os.path.basename(path)
        input_title = file_name.split('.')[0][0:8]
        return input_title

    def rename(self, dir='download'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                date_8 = str(self.get_title(file))[0:8]
                new_file = date_8 + ".mp4"
                print new_file
                src = os.path.join(parent, file)
                txt_file = open('name.txt', 'a')
                txt_file.write(u'【*】')
                txt_file.write(date_8)
                txt_file.write(file)
                txt_file.write('\n')
                txt_file.close()
                dst = os.path.join(parent, new_file)
                os.rename(src, dst)
        print u"已重命名"
        return 0

    def split_video_for_1_mask(self, input_path='download/20150115.mp4', start='00:00:20', end="00:01:00"):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        cmd_line = "ffmpeg -ss " + start + " -t " + end + " -i " + input_path + " -vcodec copy -acodec copy -y " + "mask2/" + output_title + ".mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_1_combine(self, input_path='download/20150115.mp4', start='00:01:00'):
        end = '00:05:00'
        input_title = self.get_input_title(input_path)
        output_title = input_title
        cmd_line = "ffmpeg -ss " + start + " -t " + end + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "combine/" + output_title + "_2.mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2_2_combine(self, input_path='download/20150115.mp4', start='00:05:00'):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "combine/" + output_title + "_3.mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def just_2_mask(self, video_path='mask2/1.mp4'):
        input_title = self.get_input_title(video_path)
        output_title = input_title
        cmd_line = "ffmpeg -y -t 40 -i " + video_path + " -i temp/watermark.png -i temp/daleloogn.png -filter_complex \"overlay=x=if(lt(mod(t\,20)\,10)\,W-w-10\,NAN ):y=H-h-10,overlay=x=if(gt(mod(t\,20)\,10)\,W-w-10\,NAN ) :y=H-h-10\" -strict -2 combine/" + output_title + "_1.mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def combine_2_video(self, video1='download/1.mp4', video2='download/2.mp4'):
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_1.ts|temp/" + output + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + ".mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        return 0

    def combine_2_video_to_slipt(self, video1='download/1.mp4', video2='download/2.mp4'):
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_1.ts|temp/" + output + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc split/" + output + ".mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        return 0

    def combine_3_video(self, video0='temp/720.mp4', video1='download/1.mp4', video2='download/2.mp4'):
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_0.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_0.ts|temp/" + output + "_1.ts|temp/" + output + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + ".mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_0.ts")
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        return 0

    def combine_4b_video(self, video0='temp/720.mp4', video1='download/1.mp4', video2='download/2.mp4',
                        video3='download/3.mp4'):
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_0.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_3.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_0.ts|temp/" + output + "_1.ts|temp/" + output + "_2.ts|temp/" + output + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + "_b_.mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_0.ts")
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        os.remove("temp/" + output + "_3.ts")
        return 0
    def combine_4a_video(self, video0='temp/720.mp4', video1='download/1.mp4', video2='download/2.mp4',
                        video3='download/3.mp4'):
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video0 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_0.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video3 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_3.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_0.ts|temp/" + output + "_1.ts|temp/" + output + "_2.ts|temp/" + output + "_3.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + "_a_.mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_0.ts")
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        os.remove("temp/" + output + "_3.ts")
        return 0


    def combine_video(self, dir='combine'):
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
        input_title = self.get_input_title(video1)
        output = input_title
        cmd_line = "ffmpeg -i " + video1 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_1.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i " + video2 + " -vcodec copy -acodec copy -vbsf h264_mp4toannexb temp/" + output + "_2.ts"
        os.system(cmd_line)
        cmd_line = "ffmpeg -i \"concat:temp/" + output + "_1.ts|temp/" + output + "_2.ts\"  -vcodec copy -acodec copy -absf aac_adtstoasc out/" + output + ".mp4"
        print(cmd_line)
        os.system(cmd_line)
        os.remove("temp/" + output + "_1.ts")
        os.remove("temp/" + output + "_2.ts")
        os.remove(video1)
        os.remove(video2)
        print(u'合并完毕前往out查看')
        return 0

    def split_video_for_1(self, input_path='download/20150115.mp4', start='00:01:00', end="00:03:00"):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        cmd_line = "ffmpeg -ss " + start + " -t " + end + " -i " + input_path + " -vcodec copy -acodec copy -y " + "out/" + output_title + "_1.mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video_for_2(self, input_path='download/20150115.mp4', start='00:03:00'):
        input_title = self.get_input_title(input_path)
        output_title = input_title
        cmd_line = "ffmpeg -ss " + start + "  -i " + input_path + " -vcodec copy -acodec copy -y " + "out/" + output_title + "_2.mp4"
        print(cmd_line)
        os.system(cmd_line)
        return 0

    def split_video(self, dir='split'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                split_time = '00:25:00'
                self.split_video_for_1(path, start='00:00:00', end=split_time)
                self.split_video_for_2(path, start=split_time)
                print(u'分割完毕前往out查看')
        return 0

    def batch_mask720drm(self, dir='download'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                self.split_video_for_1_mask(path)
                self.split_video_for_2_1_combine(path)
                self.split_video_for_2_2_combine(path)
                # os.remove(path)
                self.just_2_mask('mask2/' + file)
                os.remove('mask2/' + file)
                video0 = 'temp/720.mp4'
                video1 = "combine/" + file.split('.')[0] + "_1.mp4"
                video2 = "combine/" + file.split('.')[0] + "_2.mp4"
                video3 = "combine/" + file.split('.')[0] + "_3.mp4"
                self.combine_4a_video(video1, video2, video0, video3)
                self.combine_4b_video( video0,video1, video2, video3)
                os.remove(video1)
                os.remove(video2)
                os.remove(video3)

        print u"水印制作完毕，前往out文件夹查看"
        return 0

    def batch_mask1080whd(self, dir='download'):
        for parent, dirname, filename in os.walk(dir):
            for file in filename:
                print file
                path = os.path.join(parent, file)
                self.split_video_for_1_mask(path)
                self.split_video_for_2_1_combine(path)
                self.split_video_for_2_2_combine(path)
                # os.remove(path)
                self.just_2_mask('mask2/' + file)
                os.remove('mask2/' + file)
                video0 = 'temp/1080.mp4'
                video1 = "combine/" + file.split('.')[0] + "_1.mp4"
                video2 = "combine/" + file.split('.')[0] + "_2.mp4"
                video3 = "combine/" + file.split('.')[0] + "_3.mp4"
                self.combine_4a_video(video1, video2, video0, video3)
                self.combine_4b_video(video0,video1, video2,  video3)
                os.remove(video1)
                os.remove(video2)
                os.remove(video3)

        print u"水印制作完毕，前往out文件夹查看"
        return 0

    def createWidgets(self):
        self.cmm = Button(self)
        self.cmm["text"] = "1.重命名",
        self.cmm["command"] = self.rename
        self.cmm.pack({"side": "left"})
        self.ssy720 = Button(self)
        self.ssy720["text"] = "2.720加水印",
        self.ssy720["command"] = self.batch_mask720drm
        self.ssy720.pack({"side": "left"})
        self.ssy1080 = Button(self)
        self.ssy1080["text"] = "3.1080加水印",
        self.ssy1080["command"] = self.batch_mask1080whd
        self.ssy1080.pack({"side": "left"})
        self.ssycom = Button(self)
        self.ssycom["text"] = "4.合并视频",
        self.ssycom["command"] = self.combine_video
        self.ssycom.pack({"side": "left"})
        self.ssyspl = Button(self)
        self.ssyspl["text"] = "5.分割视频",
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
doc = Label(root, text="【2】.download文件夹 【4】.combine文件夹 【5】.split文件夹 ", fg="red")
doc.pack()
app.mainloop()
