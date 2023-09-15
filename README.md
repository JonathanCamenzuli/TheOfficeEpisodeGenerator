<img src="/assets/TheOfficeEpisodeGeneratorLogo.png" alt="The Office Episode Generator Logo">

A Python-based program that generates and opens a random episode from The Office (U.S). Episode information is obtained from the TMDB API and stored in an SQLite database.

# Requirements and Dependencies

This program makes use of the following packages:

- [requests](https://github.com/psf/requests)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

The packages can be collectively installed by making use of the included `requirements.txt` file.

```
python3 -m pip install -r requirements.txt
```

# Environmental Variables
- `TMDB_API_KEY`: The API Read Access Token from TMDB. This can be obtained [here](https://www.themoviedb.org/settings/api)
- `EPISODES_AVAILABLE`: Used for indicating whether episodes are available to be opened. `"True"`/`"False"` used.
- `THE_OFFICE_ROOT_PATH`: The absolute path for the root directory which includes the episodes. In Windows, this is included as `"C:\\...\\EpisodesFolder"`. In *nix, this is included as `"/home/.../EpisodesFolder"`.

# Changelog - 15/09/2023
- Depreciated the use of the Cinemagoer package
- Replaced the Cinemagoer package with the TMDB API
- Episodes are now stored and accessed in an SQLite database

# Methodology

Episode data is obtained for each season from the TMDB API. Each episode is stored inserted into a newly created SQLite database. The following episode information is stored:
- Season Number
- Episode Number
- Episode Name
- Episode Overview

After the creation of the database, a random episode is picked by making use of a query. The information from the selected row is displayed and used for opening the episode (if `EPISODES_AVAILABLE` is enabled)

```python
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
```

[//]: # (<img src="/assets/loadingDisplaying.gif" alt="Program Functioning">)

# Disclaimers
- This project is distributed under terms of the GNU General Public License v2.0. For more information, please look at the license file found in `./LICENSE`
- I am not affiliated with either NBC, The Office or any other motion picture or television corporation, parent or affiliate corporation. All motion pictures, products and brands mentioned and featured in this program and repository are the respective trademarks and copyrights of their owners.
