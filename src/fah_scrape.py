import requests
from bs4 import BeautifulSoup
import csv
import os
import glob
import time
from datetime import datetime
from config import *
from collections import defaultdict
import operator


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
    file = open(stats_folder_dir + file_name , 'w+')
    f = csv.writer(file, delimiter=',')

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

    users_score_dict = defaultdict(list)
    users_ppd_dict = {}
    users_pph_dict = {}

    # print(files)
    # print(len(files))
    if len(files) >= 24:
        # Determine if time between most recent file and 24 files previous has been 24 hours or greater (margine of error 5 minutes)
        print("Can calulate PPD")
        latest_file = csv.reader(open(files[-1], newline=''), delimiter=',')
        prev_day_file = csv.reader(open(files[len(files)-25], newline=''),delimiter=',')

        # Add score from 24 hours ago to dictionary with username as key
        for row2 in prev_day_file:
            users_score_dict[row2[2]].append(row2[3])

        # Append score from latest data file to the associated username entry in dict
        for row1 in latest_file:
            users_score_dict[row1[2]].append(row1[3])

        for user in users_score_dict:
            ppd = int(users_score_dict[user][1]) - int(users_score_dict[user][0])
            users_ppd_dict[user] = ppd

        sorted_ppd_list = sorted(users_ppd_sorted_dict.items(), key=lambda kv: kv[1], reverse=True)
        ppd_results_file = open("ppd-results-sorted_"+ now.strftime("%m-%d-%Y_%H-%M-%S") +".txt", "w+")
        for i in range(0,number_of_results):
            stripped_item = str(sorted_ppd_list[i]).rstrip(")")
            ppd_results_file.write(str(i) + ": " + stripped_item[1:] + "\n")
        ppd_results_file.close()




    else:
        # Calculate PPH between each pair of files and average
        print("Can only calculate PPH")
        # num_files = len([name for name in os.listdir(stats_folder_dir) if os.path.isfile(name)])
        # # Loop through the top 24 elements
        # for filename in range(len(files)-1, len(files)-num_files, -1):
        #     # print(files[filename].lstrip(stats_folder_dir))
        #     file = csv.reader(open(files[filename], newline=''), delimiter=',')
        #     for row in file:
        #         # print(row[3])
        #         users_score_dict[row[2]].append(row[3])
        #
        # for user in users_score_dict:
        #     total_score = 0
        #     for score in users_score_dict[user]:
        #         total_score = total_score + int(score)
        #     avg_pph = total_score/len(users_score_dict[user])
        #     users_pph_dict[user] = avg_pph
        #
        # sorted_pph_list = sorted(users_pph_dict.items(), key=lambda kv: kv[1], reverse=True)
        # print(sorted_pph_list)
        # print(len(sorted_pph_list))
        # pph_results_file = open("pph_results_file.txt", "w+")
        # for i in range(0, number_of_results):
        #     stripped_item = str(sorted_pph_list[i]).rstrip(")")
        #     pph_results_file.write(str(i) + ": " + stripped_item[1:] + "\n")
        # pph_results_file.close()


def main():
    get_latest_stats()
    calculate_ppd()


if __name__ == "__main__":
    main()
