"""
TheOfficeEpisodeGenerator - A Python script that provides a random
episode from the popular mockumentary sitcom, The Office (U.S)
Copyright (C) 2022 Jonathan Camenzuli

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

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
    """Class concerned with dealing with the ASCII art related to the
       operation of the script itself.
    """

    def getASCII(self):
        """Prints all the ASCII art
        """
        self.getIntroLogo()
        self.getTitle()

    def getIntroLogo(self):
        """Converts the image found in `images/logo.png` into ASCII
           text to print on the CLI
        """

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

    def getTitle(self):
        """Print the `Episode Generator` string.
        """
        bottomText = pyfiglet.figlet_format("Episode Generator", font = "bubble" )
        print(bottomText)

    def loadingRod(self):
        """Prints the loading animation. Usef while obtaining the
           episode list from IMDB
        """
        for load in itertools.cycle([".  ",".. ","..."," ..", "  .", "   "]):
            if done:
                break
            sys.stdout.write("\r Episodes list not found - Obtaining Episodes List from IMDb  " + load)
            sys.stdout.flush()
            time.sleep(.1)

class episodeList():
    """Class concerned with anything that has to do with the
       episode list which is found `./episode_list.txt`, if
       available.
    """

    def getEpList(self):
        """Obtains the episode list from IMDB into a text file
           named `episode_list.txt`
        """
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
        """Method that indicates that the episode list is getting
           generated in the CLI
        """
        loadingProcess = threading.Thread(target = asciiArt.loadingRod)
        loadingProcess.start()
        self.getEpList()
        time.sleep(10)
        done = True
        print("\n\nEpisodes list successfully created!\n\n")

    def loadEpList(self):
        """Opens `episode_list.txt` and selects a random line
           from the text file

        Returns:
            String: `selEp` is the string contains the
            episode selected
        """
        file = open("episode_list.txt")
        episodes = file.readlines()
        randEpisode = random.randint(0, 187)
        selEp = episodes[randEpisode]
        print(episodes[randEpisode])
        return selEp

    def modifyEpString(self, sStr, epStr):
        """Checks if there is an extended/two-part episode for
           the selected episode

        Args:
            sStr (String): is the string which corresponds to a
            particular season
            epStr (String): is the string which corresponds to a
            particular episode

        Returns:
            Strings: Modified `sStr` and `epStr` (if applicable)
        """
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

class fileDir():
    """Class which contains functions related to file operations
    """
    def gotoParentDir(self):
        """Changes cwd to parent directory

        Returns:
            String: The new cwd, in this case,
            the parent dir of original directory
        """
        currPath = os.path.dirname(os.getcwd())
        os.chdir(currPath)
        parPath = os.getcwd()

        return parPath

    def openEpisode(self):
        """Opens the episode in the specified path,
           with the help of `sStr` and `epStr`
        """
        pathToOpen = parPath + "\\" + sStr + "\\" + sStr + epStr + ".mp4"
        os.startfile(pathToOpen)

    def revertDir(self):
        """Revert cwd to original dir of script
        """
        os.chdir(parPath + "\\TheOfficeEpisodeGenerator\\")

if __name__ == "__main__":

    asciiArt = asciiArt()
    episodeList = episodeList()
    fileDir = fileDir()

    while (True):

        # Clear CLI
        os.system('clear')
        asciiArt.getASCII()

        # Check if file exists
        filePath = pathlib.Path("episode_list.txt")
        if filePath.is_file():
            pass
        else:
            done = False
            episodeList.createEpList(done)

        selEp = episodeList.loadEpList()

        # Parse string and episode number from line
        sStr = selEp[:3]
        epStr = selEp[3:6]

        parPath = fileDir.gotoParentDir()
        sStr, epStr = episodeList.modifyEpString(sStr, epStr)
        fileDir.openEpisode()

        print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
        inputStr = input("Enter an input: ")
        if inputStr == 'Q' or inputStr == 'q':
            quit()
        else:
            pass

        fileDir.revertDir()