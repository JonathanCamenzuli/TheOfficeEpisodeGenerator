import random
import os
import sys
import time
import threading
import itertools
import pathlib

# Dependencies
import asciiArt
import imdb

def loadingRod():
    for load in itertools.cycle([".  ",".. ","..."," ..", "  .", "   "]):
        if done:
            break
        sys.stdout.write("\r Episodes list not found - Obtaining Episodes List from IMDb  " + load)
        sys.stdout.flush()
        time.sleep(.1)

def loadEpList():
    imdb_instance = imdb.IMDb()
    imdb_code = "0386676"

    series = imdb_instance.get_movie(imdb_code)
    imdb_instance.update(series, 'episodes')
    episodes = series.data['episodes']
    with open("episode_list.txt", "w") as f:
        for i in episodes.keys():
            for j in episodes[i]:
                title = episodes[i][j]['title']
                if j < 10:
                    ep_num = "E0" + str(j)
                else:
                    ep_num = "E" + str(j)
                f.write("S0" + str(i) + ep_num + " : " + title + "\n")

while (True):
    os.system('clear')
    asciiArt.getASCII()
    rand_episode = random.randint(0, 187)

    file_path = pathlib.Path("episode_list.txt")

    if file_path.is_file():
        pass
    else:
        done = False
        loadingProcess = threading.Thread(target = loadingRod)
        loadingProcess.start()
        loadEpList()
        time.sleep(10)
        done = True
        print("\n\nEpisodes list successfully created!\n\n")

    file = open("episode_list.txt")
    episodes = file.readlines()
    sel_ep = episodes[rand_episode]
    print(episodes[rand_episode])

    s_str = sel_ep[:3]
    ep_str = sel_ep[3:6]

    curr_path = os.path.dirname(os.getcwd())
    os.chdir(curr_path)
    par_path = os.getcwd()

    if ((s_str == "S03") and (ep_str == "E12" or ep_str == "E13")):
        ep_str = "E12E13"
    elif (s_str == "S04"):
        if (ep_str == "E01" or ep_str == "E02"):
            ep_str = "E01E02"
        elif (ep_str == "E03" or ep_str == "E04"):
            ep_str = "E03E04"
        elif (ep_str == "E05" or ep_str == "E06"):
            ep_str = "E05E06"
        elif (ep_str == "E07" or ep_str == "E08"):
            ep_str = "E07E08"
        elif (ep_str == "E18" or ep_str == "E19"):
            ep_str = "E18E19"
    elif (s_str == "S06"):
        if (ep_str == "E04" or ep_str == "E05"):
            ep_str = "E04E05"
        elif (ep_str == "E13"):
            input_str = input("Do you want to open an extended version of S06E13? (Y/N): ")
            if input_str == 'Y' or input_str == 'y':
                ep_str = ep_str + " - EXTENDED"
            else:
                pass
        elif (ep_str == "E17" or ep_str == "E18"):
            ep_str = "E17E18"        
    elif (s_str == "S07"):
        if (ep_str == "E11" or ep_str == "E12"):
            ep_str = "E11E12"
        elif (ep_str == "E25" or ep_str == "E26"):
            ep_str = "E25E26"

    path_to_open = par_path + "\\" + s_str + "\\" + s_str + ep_str + ".mp4"

    os.startfile(path_to_open)

    print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
    input_str = input("Enter an input: ")
    if input_str == 'Q' or input_str == 'q':
        quit()
    else:
        pass

    os.chdir(par_path + "\\TheOfficeEpisodeGenerator\\")