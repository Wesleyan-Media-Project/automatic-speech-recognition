# Trim videos into 2-min long
# Use the following bash code to get ffmpeg
# export PATH=/software/ffmpeg:/software/ffmpeg/bin:$PATH

import os
from tqdm import tqdm


os.chdir("/home/jyao01/github/google_2022/data/mp4") 

path_mp4 = "/home/jyao01/github/google_2022/data/mp4/"
path_mp4_truncated = "/home/jyao01/github/google_2022/data/mp4_c/"

errors_cut =[]
for filename in tqdm(os.listdir(path_mp4)[:]):
    try:
        id = os.path.basename(filename).split('.')[0]
        output = id +'_c.mp4'
        command = "ffmpeg -accurate_seek -ss 00:00:00 -i " + os.path.join(path_mp4, filename) + " -to 00:02:10  -c:v copy -c:a copy " + os.path.join(path_mp4_truncated, output)
        #print(command)
        os.system(command)
    except:
        errors_cut.append(filename)
        pass

