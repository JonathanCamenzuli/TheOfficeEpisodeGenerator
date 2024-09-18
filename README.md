<img src="/assets/TheOfficeEpisodeGeneratorLogo.png" alt="The Office Episode Generator Logo">

\
![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![TMDB](https://img.shields.io/badge/TMDB%20API-0d253f?style=flat&logo=themoviedatabase&logoColor=%230d253f&logoSize=auto&logoHeight=75&logoWidth=25&labelColor=%23ffffff)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

A Python-based program that generates and opens a random episode from The Office (U.S). Episode information is obtained from the TMDB API and stored in an SQLite database.

# Setup
The [PowerShell script](set_up_env.ps1) has been added to automate the setup of a virtual environment, and add creation of an alias in PowerShell in order to easily call the script.

That being said, the follow environment variables are required for the proper functioning of the program:
- `TMDB_API_KEY`: The API Read Access Token from TMDB. This can be obtained [here](https://www.themoviedb.org/settings/api). Kindly note that an account with TMDB is required for said Token.
- `EPISODES_AVAILABLE`: Used for indicating whether episodes are available to be opened. `"True"`/`"False"` used.
- `THE_OFFICE_ROOT_PATH`: The absolute path for the root directory which includes the episodes. In Windows, this is included as `"C:\\...\\EpisodesFolder"`. In *nix, this is included as `"/home/.../EpisodesFolder"`.

Once the script is executed for the first time, it attempts to obtain the episode list from TMDB as highlighted [below](#methodology).

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
- This project is licensed under the terms specified in the [`LICENSE`](/LICENSE) file
- This project uses the TMDB API but is not endorsed or certified by TMDB
- I am not affiliated with NBC, *The Office*, or any other motion picture, television corporation, or their parent or affiliate companies. All motion pictures, products, and brands mentioned and featured in this program and repository are the respective trademarks and copyrights of their respective owners.
