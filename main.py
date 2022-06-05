import random
import os
import sys
import time
import threading
import itertools
import pathlib

# Dependencies
from PIL import Image
import imdb
import pyfiglet

class asciiArt():
# Get overall ASCII art
    def getASCII(self):
        self.getIntroLogo()
        self.getTitle()

    # Convert "images/logo.png" into ASCII art
    def getIntroLogo(self):
        # Pass the image as command line argument
        imagePath = "images/logo.png"
        img = Image.open(imagePath)

        # Resize the image
        width, height = img.size
        aspect_ratio = height / width
        newWidth = 110 # orig: 120
        newHeight = aspect_ratio * newWidth * 0.55
        img = img.resize((newWidth, int(newHeight)))

        # Convert image to greyscale format
        img = img.convert('L')

        pixels = img.getdata()

        # Replace each pixel with a character from array
        chars = ["@", "O", "#", "$", "%", "&", "*", "!", "~", "·", " "]
        newPixels = [chars[pixel//25] for pixel in pixels]
        newPixels = ''.join(newPixels)

        # Split string of chars into multiple strings of length equal to new width and create a list
        newPixelsCount = len(newPixels)
        asciiImage = [newPixels[index:index + newWidth] for index in range(0, newPixelsCount, newWidth)]
        asciiImage = "\n".join(asciiImage)
        print(asciiImage)

    # Print "Episode Generator" string
    def getTitle(self):
        bottomText = pyfiglet.figlet_format("Episode Generator", font = "bubble" )
        print(bottomText)

    # Function that plays loading animation while
    # loading episode list
    def loadingRod(self):
        for load in itertools.cycle([".  ",".. ","..."," ..", "  .", "   "]):
            if done:
                break
            sys.stdout.write("\r Episodes list not found - Obtaining Episodes List from IMDb  " + load)
            sys.stdout.flush()
            time.sleep(.1)

class episodeList():

    # Function that loads episode list
    def getEpList(self):
        imdbInstance = imdb.IMDb()
        imdbCode = "0386676"

        series = imdbInstance.get_movie(imdbCode)
        imdbInstance.update(series, 'episodes')
        episodes = series.data['episodes']
        with open("episode_list.txt", "w") as f:
            for i in episodes.keys():
                for j in episodes[i]:
                    title = episodes[i][j]['title']
                    if j < 10:
                        epNum = "E0" + str(j)
                    else:
                        epNum = "E" + str(j)
                    f.write("S0" + str(i) + epNum + " : " + title + "\n")

    def createEpList(self, done):
        loadingProcess = threading.Thread(target = asciiArt.loadingRod)
        loadingProcess.start()
        self.getEpList()
        time.sleep(10)
        done = True
        print("\n\nEpisodes list successfully created!\n\n")

    def loadEpList(self):
        # Open episode list and obtain episode name
        # from randomised line
        file = open("episode_list.txt")
        episodes = file.readlines()
        randEpisode = random.randint(0, 187)
        selEp = episodes[randEpisode]
        print(episodes[randEpisode])
        return selEp

    def modifyEpString(self, sStr, epStr):
        
        # Change episode string if there is two-part
        # episode available
        if ((sStr == "S03") and (epStr == "E12" or epStr == "E13")):
            epStr = "E12E13"
        elif (sStr == "S04"):
            if (epStr == "E01" or epStr == "E02"):
                epStr = "E01E02"
            elif (epStr == "E03" or epStr == "E04"):
                epStr = "E03E04"
            elif (epStr == "E05" or epStr == "E06"):
                epStr = "E05E06"
            elif (epStr == "E07" or epStr == "E08"):
                epStr = "E07E08"
            elif (epStr == "E18" or epStr == "E19"):
                epStr = "E18E19"
        elif (sStr == "S06"):
            if (epStr == "E04" or epStr == "E05"):
                epStr = "E04E05"
            elif (epStr == "E13"):

                # Prompt the user if extended version
                # of episode should be played
                inputStr = input("Do you want to open an extended version of S06E13? (Y/N): ")
                if inputStr == 'Y' or inputStr == 'y':
                    epStr = epStr + " - EXTENDED"
                else:
                    pass
            elif (epStr == "E17" or epStr == "E18"):
                epStr = "E17E18"        
        elif (sStr == "S07"):
            if (epStr == "E11" or epStr == "E12"):
                epStr = "E11E12"
            elif (epStr == "E25" or epStr == "E26"):
                epStr = "E25E26"
        
        return sStr, epStr

class pathClass():
    def gotoParentDir(self):
        # Changing directory to parent directory
        currPath = os.path.dirname(os.getcwd())
        os.chdir(currPath)
        parPath = os.getcwd()

        return parPath

    def openEpisode(self):
        # Open video in specified path
        pathToOpen = parPath + "\\" + sStr + "\\" + sStr + epStr + ".mp4"
        os.startfile(pathToOpen)

    def revertDir(self):
        # Revert path to old directory
        os.chdir(parPath + "\\TheOfficeEpisodeGenerator\\")


if __name__ == "__main__":

    asciiArt = asciiArt()
    episodeList = episodeList()
    pathClass = pathClass()

    while (True):

        # Clear CLI
        os.system('clear')

        # Print ASCII art
        asciiArt.getASCII()

        # Check if file exists
        filePath = pathlib.Path("episode_list.txt")
        if filePath.is_file():
            pass
        else:
            # Creating Episode List
            done = False
            episodeList.createEpList(done)

        # Open episode list and obtain episode name
        # from randomised line
        selEp = episodeList.loadEpList()

        # Parse string and episode number from line
        sStr = selEp[:3]
        epStr = selEp[3:6]

        parPath = pathClass.gotoParentDir()
        sStr, epStr = episodeList.modifyEpString(sStr, epStr)
        pathClass.openEpisode()

        print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
        inputStr = input("Enter an input: ")
        if inputStr == 'Q' or inputStr == 'q':
            quit()
        else:
            pass

        pathClass.revertDir()