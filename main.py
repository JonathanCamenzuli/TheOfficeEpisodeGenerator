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
import sqlite3

# Dependencies
import imdb
from dotenv import load_dotenv

asciiTitlePath = "./images/ascii_title.txt"


class asciiArt():
    """Class concerned with dealing with the ASCII art related to the
       operation of the script itself.
    """

    def getASCII(self):
        """Prints all the ASCII art
        """
        with open(asciiTitlePath) as f:
            asciiTitleContents = f.read()
            print(asciiTitleContents + "\n")

    def loadingRod(self):
        """Prints the loading animation. Usef while obtaining the
           episode list from IMDB
        """
        for load in itertools.cycle([".  ", ".. ", "...", " ..", "  .", "   "]):
            if done:
                break
            sys.stdout.write(
                "\r Episodes list not found - Obtaining Episodes List from IMDb  " + load)
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
        loadingProcess = threading.Thread(target=asciiArt.loadingRod)
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
        if (sStr == "S06"):
            if (epStr == "E13"):
                # Prompt the user if extended version
                # of episode should be played
                inputStr = input(
                    "Do you want to open an extended version of S06E13? (Y/N): ")
                if inputStr == 'Y' or inputStr == 'y':
                    epStr = epStr + " - EXTENDED"
                else:
                    pass
        return sStr, epStr


class fileDir():
    """Class which contains functions related to file operations
    """

    def __init__(self):
        load_dotenv()
        self.dir_path = os.getenv("THE_OFFICE_ROOT_PATH")

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
        pathToOpen = self.dir_path + "\\" + sStr + "\\" + sStr + epStr + ".mp4"
        os.startfile(pathToOpen)

    def revertDir(self):
        """Revert cwd to original dir of script
        """
        os.chdir(parPath + "\\TheOfficeEpisodeGenerator\\")


if __name__ == "__main__":

    asciiArt = asciiArt()
    episodeList = episodeList()
    fileDir = fileDir()

    vidsPresentStr = input("Are episodes present in your file system? (Y/N): ")

    if vidsPresentStr == "Y" or vidsPresentStr == "y":
        vidsPresent = True
    else:
        vidsPresent = False

    while (True):

        # Clear CLI
        os.system('cls' if os.name == 'nt' else 'clear')
        asciiArt.getASCII()

        # Check if file exists
        filePath = pathlib.PurePath("episode_list.txt")
        if pathlib.Path(filePath).is_file():
            pass
        else:
            done = False
            episodeList.createEpList(done)

        selEp = episodeList.loadEpList()

        if vidsPresent == True:
            # Parse string and episode number from line
            sStr = selEp[:3]
            epStr = selEp[3:6]

            # parPath = fileDir.gotoParentDir()
            sStr, epStr = episodeList.modifyEpString(sStr, epStr)
            fileDir.openEpisode()

        print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
        inputStr = input("Enter an input: ")
        if inputStr == 'Q' or inputStr == 'q':
            quit()
        else:
            pass

        # if vidsPresent == True:
        #     fileDir.revertDir()
