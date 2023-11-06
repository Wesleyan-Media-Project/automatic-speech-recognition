# Run the following bash code in terminal to make ffmpeg accessible
# export PATH=/software/ffmpeg:/software/ffmpeg/bin:$PATH

import os
from shlex import quote

path_mp4 = "/home/jyao01/github/google_2022/data/mp4_c/"
path_wav = "/home/jyao01/github/google_2022/data/wav_c/"

os.chdir("/home/jyao01/github/google_2022/data/mp4_c/")

#quote() helps escape special symbols in filenames
for filename in os.listdir(path_mp4):
    if (filename.endswith(".mp4")):
        root_name = filename.split('.')[0] 
        print(filename)
        os.system("ffmpeg -i " + quote(filename) + ' ' + path_wav +quote(root_name)+'.wav')
    else:
        continue


