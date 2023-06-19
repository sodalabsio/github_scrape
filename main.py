import os, csv, time
from query import Query
from locations import dict_of_locations
from datetime import datetime, timedelta
import logging, sys


# Change the following:
## dict_of_locations in locations.py
## START_DATE
## END_DATE
## INTERVAL
## PATH_DIR

PATH_DIR = './data/'
START_DATE = datetime(2009, 1, 1)  # (YEAR, MONTH, DAY)
END_DATE = datetime(2023, 4, 11)  # (YEAR, MONTH, DAY)
INTERVAL = 15  # NUMBER OF DAYS TO ITERATE OVER SCRAPE QUERY

present_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to info
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# create file handler and set level to debug
file_handler = logging.FileHandler(f'./logs/log_{present_time}.txt')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def create_date_blocks(start_date=START_DATE, end_date=END_DATE, interval=INTERVAL):
    """Create date blocks"""
    blocks = []
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + timedelta(days=interval)
        if next_date > end_date:
            next_date = end_date
        
        block_str = f"{current_date:%Y-%m-%d}..{next_date:%Y-%m-%d}"
        blocks.append(block_str)
        current_date = next_date + timedelta(days=1)
    
    return blocks


def write_csv(csv_path:str, location:str, date_range:str):
    cursor = None
    iter = 0
    field_names = [
        'login', 
        'name',
        'location',
        'company',
        'followers',
        'following',
        'repositories',
        'createdAt',
        'updatedAt'
        ]
    with open(csv_path, mode='a+', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()     
        
        # Loop through the pages of search results
        while True:
            iter += 1
            # Send the GraphQL request and get json
            my_query = Query(location, date_range, cursor)
            response = my_query.get_response_json()
            
            logger.info(f"page number: {iter}")

            # Check for errors in the response
            if 'errors' in response:
                logger.info(response['errors'])
                break
            
            # Extract the user data from the response
            data = response['data']['search']
            user_count = data['userCount']
            end_cursor = data['pageInfo']['endCursor']
            has_next_page = data['pageInfo']['hasNextPage']
            users = data['edges']
            
            logger.info(f"number of users in this page: {len(users)}")
            logger.info(f"total users: {user_count}")
            
            # Write the user data to the CSV file
            count_write_rows = 0
            for user in users:
                row = {}
                
                try:
                    row['login'] = user['node']['login']
                except KeyError:
                    # logger.info("failed to write this row")
                    continue

                row['name'] = user['node']['name']
                row['location'] = user['node']['location']
                row['company'] = user['node']['company']
                row['followers'] = user['node']['followers']['totalCount']
                row['following'] = user['node']['following']['totalCount']
                row['repositories'] = user['node']['repositories']['totalCount']
                row['createdAt'] = user['node'].get('createdAt')
                row['updatedAt'] = user['node'].get('updatedAt')

                writer.writerow(row)
                count_write_rows += 1
            
            # logger.info(end_cursor)
            logger.info(f"number of rows written: {count_write_rows}\n\n\n")
            
            wait_time = my_query.get_wait_time()
            logger.info(f"wait_time: {wait_time}\n")
            time.sleep(wait_time)
            
            # Break out of the loop if there are no more pages
            if not has_next_page:
                break
            cursor = end_cursor


def main():
    for country in dict_of_locations.keys():
        # create the folder for the country if does not exist
        path_country = os.path.join(PATH_DIR, country)
        if not os.path.exists(path_country):
            os.makedirs(path_country)
        
        for location in dict_of_locations[country]:
            csv_path = os.path.join(path_country, f'github_users_{location}.csv')
            date_blocks = create_date_blocks()
            
            logger.info(f"***{location}***")
            
            for date_range in date_blocks:
                logger.info(f'* {date_range} *')
                write_csv(csv_path, location, date_range)


if __name__ == "__main__":
    main()
