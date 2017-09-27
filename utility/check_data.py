import pickle
import os
import pandas as pd

project_data_path = "project_data"
training_data_path = os.path.join("data", "Training_data","Stocks")
complete_data_path = os.path.join("data", "Complete_data", "stocks")


def check_folder(file_name):
    df = pd.read_csv(file_name)
    count = 0
    for null_count in df.isnull().sum():
        count += null_count
    if count > 0 or len(df['Date']) == 0:
        print("{} has some missing value".format(file_name))
        os.remove(file_name)

def check_data():
    complete_file_list = os.listdir(complete_data_path)
    sp_500_file_list = os.listdir(training_data_path)
    for complete_file_index in complete_file_list:
        check_folder(os.path.join(complete_data_path, complete_file_index))

    for sp_500_file_index in sp_500_file_list:
        check_folder(os.path.join(training_data_path, sp_500_file_index))