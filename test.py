import os
from random import randint


def generatGIF(PATH='VIDEOPATH'):
    cmd_line = "ffmpeg -ss 00:02:20 -t 10 -i " + PATH + " -r 1 -s 320*240 -f gif out/" + str(randint(0,1000)) + ".gif"
    print cmd_line
    print "**"
    os.system(cmd_line)
    return 0
generatGIF('download/1080/test.mp4')
