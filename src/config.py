from datetime import datetime

now = datetime.now()

fah_stats_page = "https://apps.foldingathome.org/teamstats/team223518.html"
stats_folder_dir = "../fah_stats/"
file_name = 'ltt_folding_stats_'+ now.strftime("%m-%d-%Y_%H-%M-%S") +'.csv'
