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

import os
import sys
import time
import threading
import itertools
import pathlib
import sqlite3

# Dependencies
import requests
from dotenv import load_dotenv

asciiTitlePath = "./assets/ascii_title.txt"


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

    def getEpList(self, conn, cursor):
        """Obtains the episode list from IMDB into a text file
           named `episode_list.txt`
        """

        for season in range(1, 10):
            url = f"https://api.themoviedb.org/3/tv/2316/season/{season}?language=en-US"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
            }

            response = requests.get(url, headers=headers)
            fullEpisodeList = response.json()['episodes']

            for episode in range(len(fullEpisodeList)):
                specificEpisode = fullEpisodeList[episode]
                cursor.execute('''INSERT INTO episodes (season, episode, episodeName, episodeBrief) VALUES (?, ?, ?, ?)''', (
                    season, specificEpisode['episode_number'], specificEpisode['name'], specificEpisode['overview']))

        conn.commit()
        conn.close()

    def createEpList(self, done):
        """Method that indicates that the episode list is getting
           generated in the CLI
        """
        loadingProcess = threading.Thread(target=asciiArt.loadingRod)
        loadingProcess.start()
        f = open("episodes.db", "w")

        conn = sqlite3.connect('episodes.db')
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE episodes (id INTEGER PRIMARY KEY, season INTEGER, episode INTEGER, episodeName TEXT, episodeBrief TEXT)""")

        self.getEpList(conn, cursor)
        time.sleep(10)
        done = True
        print("\n\nFull episode database successfully created!\n\n")

    def loadEpList(self):
        """Opens `episode_list.txt` and selects a random line
           from the text file

        Returns:
            String: `selEp` is the string contains the
            episode selected
        """

        conn = sqlite3.connect('episodes.db')
        cursor = conn.cursor()

        # Retrieve a random episode from the database
        cursor.execute('SELECT * FROM episodes ORDER BY RANDOM() LIMIT 1')
        episode = cursor.fetchone()

        if episode:
            pk, season, episodeNo, episodeName, episodeBrief = episode
            return season, episodeNo, episodeName, episodeBrief
        else:
            print("No episodes found in the database.")
            return None

    def modifyEpString(self, seasonStr, episodeStr):
        """Checks if there is an extended/two-part episode for
           the selected episode

        Args:
            seasonStr (String): is the string which corresponds to a
            particular season
            episodeStr (String): is the string which corresponds to a
            particular episode

        Returns:
            Strings: Modified `sStr` and `epStr` (if applicable)
        """
        if (seasonStr == "S06"):
            if (episodeStr == "E13"):
                # Prompt the user if extended version
                # of episode should be played
                inputStr = input(
                    "Do you want to open an extended version of S06E13? (Y/N): ")
                if inputStr == 'Y' or inputStr == 'y':
                    episodeStr = episodeStr + " - EXTENDED"
                else:
                    pass
        return seasonStr, episodeStr


def openEpisode(season, episode):
    """Opens the episode in the specified path,
        with the help of `season` and `episode`
    """

    dirPath = os.getenv("THE_OFFICE_ROOT_PATH")

    if os.name == 'nt':
        pathToOpen = dirPath + "\\" + season + "\\" + season + episode + ".mp4"
    else:
        pathToOpen = dirPath + "/" + season + "/" + season + episode + ".mp4"
    os.startfile(pathToOpen)


if __name__ == "__main__":

    load_dotenv()

    asciiArt = asciiArt()
    episodeList = episodeList()

    vidsPresent = (os.getenv("EPISODES_AVAILABLE") == "True")

    while (True):

        # Clear CLI
        os.system('cls' if os.name == 'nt' else 'clear')
        asciiArt.getASCII()

        # Check if database exists
        filePath = pathlib.PurePath("episodes.db")

        if pathlib.Path(filePath).is_file():
            pass
        else:
            done = False
            episodeList.createEpList(done)

        season, episodeNo, episodeName, episodeBrief = episodeList.loadEpList()

        if vidsPresent == True:
            # Parse string and episode number from line
            seasonStr = f"S0{season}"
            episodeStr = f"E0{episodeNo}" if episodeNo < 10 else f"E{episodeNo}"

            seasonStr, episodeStr = episodeList.modifyEpString(
                seasonStr, episodeStr)
            openEpisode(seasonStr, episodeStr)

        print(seasonStr + episodeStr + ": " + episodeName + "\n")
        print(episodeBrief + "\n")

        print("-> Enter any key to restart\n-> Enter 'Q' to Quit\n")
        inputStr = input("Enter an input: ")
        if inputStr == 'Q' or inputStr == 'q':
            quit()
        else:
            pass
