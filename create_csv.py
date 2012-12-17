## write data to csv for download to client

import csv
import os

def create_csv(data):
    """ returns (file_basename, server_path, file_size) """
    file_basename = 'branch_output.csv'
    server_path = '/groups/microfinance/csvfordownload/'
    w_file = open(server_path+file_basename,'w')
    w_file.write('Branch,Date,Clients,Portfolio,Portfolio > 1 Day, Portfolio > 30 Days\n')   
    #print(data) 
    for branch in data: ## reads rows as array
        branch_as_str = str(branch[0])
        
        for row in branch[1]:
            date = str(row[0])
            row_as_string = str(row[1:])
            w_file.write(branch_as_str+','+date+','+row_as_string[1:-1] + '\n')

    w_file.close()
    w_file = open(server_path+file_basename,'r')
    file_size = len(w_file.read()) 
    return file_basename, server_path, file_size

