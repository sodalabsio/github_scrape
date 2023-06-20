# GitHub Scraper
Source code for scraping GitHub public user data across locations and time periods. We scrape the following attributes at user-level for a defined set of locations (`location`) and span of time-period (`createdAt`):

1. `login`: The user's username.
2. `name`: The user's full name.
3. `location`: The user's location.
4. `company`: The user's company name.
5. `followers`: The number of followers the user has.
6. `following`: The numbers of users the user is following.
7. `repositories`: A list of user's repositories.
8. `createdAt`: The date and time the user's account was created.
9. `updatedAt`: The date and time the user's account was last updated. 

Read more on the user-level attributes in the official GitHub documentation here: https://docs.github.com/en/graphql/reference/objects#user


## Run

```
# Clone the repo
git clone https://github.com/sodalabsio/github_scrape

cd ./github_scrape

# Set up conda env
conda create -n github_scrape
conda activate github_scrape
pip install -r requirements.txt

# Define GITHUB_TOKEN environment variable
touch .env
cat - > .env
GITHUB_TOKEN=<paste your github token>
<Press Ctrl+d>


# Run the scraper
python main.py

# Post-processing script: remove duplicates and redundant column-headers
python post_process.py
```


## Configure

You may want to modify the following arguments to adjust the locations and time-period of interest:
- In the file `locations.py`, you can add the countries and their locations across which you want to scrape the user data in the following manner:
    - `dict_of_locations`: 
    `{"country_1": [location1_1, location1_2, ..., location1_n], 
      "country_2": [location2_1, location2_2, ..., location2_n], ...}`
- In the file `main.py`, you can modify the following arguments:
    - `START_DATE`: The first date in `createdAt` defining the time-period of interest for scraping.
    - `END_DATE`: The last date in `createdAt` defining the time-period of interest for scraping.
    - `INTERVAL`: Number of days per query. We query users who belong to a location in a batch-wise fashion iteratively on a fixed time interval. Each query fetches users who created an account falling in the range of dates defined by `INTERVAL` (integer). Larger range (i.e. higher integer value for `INTERVAL`) would mean potentially fetching more users per query, risking hitting the rate limit (read about it [here](https://docs.github.com/en/rest/search?apiVersion=2022-11-28#about-the-search-api)).
    - `PATH_DIR`: Folder where the output of the scraper (`.csv` file) would be stored. By default, it is `./data/`. Refer the directory tree of one example run in `./data/` in this repo.