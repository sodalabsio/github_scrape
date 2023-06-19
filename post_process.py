import os
import pandas as pd
from glob import glob
from locations import dict_of_locations


PATH_DIR = './data/'

def main():
    """Main function"""
    
    # iterate over countries
    for country in dict_of_locations.keys():
        # define the path of the countries
        path_dir_country = os.path.join(PATH_DIR, country)
        
        # empty dataframe to append dataframes iteratively
        df_merge = pd.DataFrame()

        # read the csv files and append all into a pandas dataframe
        for csv_file_path in glob(os.path.join(path_dir_country, "*.csv")):
            df = pd.read_csv(csv_file_path)
            df_merge = df_merge.append(df, ignore_index=True)
        
        # remove duplicates and header rows
        df_merge.drop_duplicates(subset=['login'], inplace=True, ignore_index=True)

        # write to csv
        df_merge.to_csv(os.path.join(PATH_DIR, f"github_users_merged_{country}.csv"))

if __name__ == "__main__":
    main()
