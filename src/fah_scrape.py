import requests
from bs4 import BeautifulSoup
import csv
import os
import glob
import time
from datetime import datetime
from config import *


#####################################################
# Function      : get_latest_stats
# Description   : Gets the latest stats from the specified page and stores data in a CSV
#####################################################
def get_latest_stats():
    # Getting page HTML
    page = requests.get(fah_stats_page)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Finding the table and getting all rows
    members_table = soup.find(class_='members')
    members_table_entries = members_table.find_all('tr')

    # Creating CSV file
    f = csv.writer(open(stats_folder_dir + file_name , 'w'))

    # Getting the string contents of each row and storing in CSV
    for entry in members_table_entries[1:]:
        entry_text = entry.get_text()
        lines = entry_text.split('\n')
        rank = int(lines[1])
        team_rank = int(lines[2])
        name = lines[3]
        score = int(lines[4])
        work_units = int(lines[5])
        f.writerow([rank,team_rank,name,score,work_units])

#####################################################
# Function      : calculate_ppd
# Description   : Calculates the average PPD of all folders in the team using up to the previous 24 sets of stats.
#####################################################
def calculate_ppd():
    # files = glob.glob(stats_folder_dir)
    files = os.listdir(stats_folder_dir)
    files = glob.glob(stats_folder_dir + "*.csv")
    files.sort(key=os.path.getmtime)

    print(files)
    print(len(files))
    if len(files) >= 24:
        # Determine if time between most recent file and 24 files previous has been 24 hours or greater (margine of error 5 minutes)
        print("Can calulate PPD")

    else:
        # Calculate PPH between each pair of files and average
        print("Can only calculate PPH")




def main():
    get_latest_stats()
    calculate_ppd()


if __name__ == "__main__":
    main()
