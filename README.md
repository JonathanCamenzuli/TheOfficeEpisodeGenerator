<img src="/gitImages/TheOfficeEpisodeGeneratorLogo.png" alt="The Office Episode Generator Logo">

A Python-based program that generates and opens a random episode from The Office (U.S).

# Requirements and Dependencies

This program makes use of the following package:

- [Cinemagoer](https://github.com/cinemagoer/cinemagoer) (formerly known as *IMDbPY*)


```
python3 -m pip install cinemagoer
```

# Environmental Variables

- `THE_OFFICE_ROOT_PATH`: The absolute path for the root directory which includes the episodes. In Windows, this is included as `"C:\\...\\EpisodesFolder"`. In *nix, this is included as `"/home/.../EpisodesFolder"`.

# Changelog - 14/09/2023
- Episodes are now opened through a set path which is defined in environmental variables

# Methodology

An instance from the Cinemagoer class is created. The `movieID` for *The Office (U.S)* is then used to load all the episodes of the series from IMDb. All the episodes are placed into a text file. Furthermore, after that text file is created, that text file will be used to display a random line which in this case displays the episode in said line.

```python
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
```

<img src="/gitImages/loadingDisplaying.gif" alt="Program Functioning">

The random episode is then opened by the preferred video player.

```python
def openEpisode(self):
    pathToOpen = self.dirPath + "\\" + sStr + "\\" + sStr + epStr + ".mp4"
    os.startfile(pathToOpen)
```

# Disclaimers
- This project is distributed under terms of the GNU General Public License v2.0. For more information, please look at the license file found in `./LICENSE`
- I am not affiliated with either NBC, The Office, IMDb or any other motion picture or television corporation, parent or affiliate corporation. All motion pictures, products and brands mentioned and featured in this program and repository are the respective trademarks and copyrights of their owners.
