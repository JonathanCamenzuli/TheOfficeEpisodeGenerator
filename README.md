<img src="/gitImages/TheOfficeEpisodeGeneratorLogo.png" alt="The Office Episode Generator Logo">

A Python-based program that generates and opens a random episode from The Office (U.S).

# Requirements and Dependencies

This program makes use of the following packages:

- [Cinemagoer](https://github.com/cinemagoer/cinemagoer) (formerly known as *IMDbPY*)
- [Python Imaging Library](https://github.com/python-pillow/Pillow)
- [Pyfiglet](https://github.com/pwaller/pyfiglet)

```
python3 -m pip install cinemagoer
```

```
python3 -m pip install Pillow
```

```
python3 -m pip install pyfiglet
```
# Changelog - 01/04/2022
- Added functionality that opens the selected episode in the default chosen video player.

# Methodology

An instance from the Cinemagoer class is created. The `movieID` for *The Office (U.S)* is then used to load all the episodes of the series from IMDb. All the episodes are placed into a text file. Furthermore, after that text file is created, that text file will be used to display a random line which in this case displays the episode in said line.

```python
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
```

<img src="/gitImages/loadingDisplaying.gif" alt="Program Functioning">

The random episode is then opened by the preferred video player.

```python
path_to_open = par_path + "\\" + s_str + "\\" + s_str + ep_str + ".mp4"
os.startfile(path_to_open)
```

# Disclaimer

I am not affiliated with either NBC, The Office, IMDb or any other motion picture or television corporation, parent or affiliate corporation. All motion pictures, products and brands mentioned and featured in this program and repository are the respective trademarks and copyrights of their owners.
