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
    print(episodes[rand_episode])

    print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
    inputStr = input("Enter an input: ")
    if inputStr == 'Q' or inputStr == 'q':
        quit()
    elif inputStr == 'R' or inputStr == 'r':
        pass