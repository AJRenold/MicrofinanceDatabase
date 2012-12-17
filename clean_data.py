## import data from csv

import csv

def clean_data(file_path,report_date):

    rfile = open(file_path,'rU')
    data = csv.reader(rfile)
    w_file = open(str(file_path[:file_path.index('.')]) + str(report_date) + '.csv','w')

    def convert_date(vlist):
        """takes a list and finds the dates to convert them
        to numerical date values e.g. 1-dec-2012 to YYYY-MM-DD"""

        for y in range(len(vlist)):
            if isinstance(vlist[y],str) and "-" in vlist[y]:
                if vlist[y].find('-') == 1:
                    vlist[y] = "0" + vlist[y]
                if vlist[y][3:6] == 'Jan':
                    vlist[y] = vlist[y][:3] + '01' + vlist[y][6:]
                if vlist[y][3:6] == 'Feb':
                    vlist[y] = vlist[y][:3] + '02' + vlist[y][6:]
                if vlist[y][3:6] == 'Mar':
                    vlist[y] = vlist[y][:3] + '03' + vlist[y][6:]
                if vlist[y][3:6] == 'Apr':
                    vlist[y] = vlist[y][:3] + '04' + vlist[y][6:]
                if vlist[y][3:6] == 'May':
                    vlist[y] = vlist[y][:3] + '05' + vlist[y][6:]
                if vlist[y][3:6] == 'Jun':
                    vlist[y] = vlist[y][:3] + '06' + vlist[y][6:]                
                if vlist[y][3:6] == 'Jul':
                    vlist[y] = vlist[y][:3] + '07' + vlist[y][6:]
                if vlist[y][3:6] == 'Aug':
                    vlist[y] = vlist[y][:3] + '08' + vlist[y][6:]
                if vlist[y][3:6] == 'Sep':
                    vlist[y] = vlist[y][:3] + '09' + vlist[y][6:]
                if vlist[y][3:6] == 'Oct':
                    vlist[y] = vlist[y][:3] + '10' + vlist[y][6:]
                if vlist[y][3:6] == 'Nov':
                    vlist[y] = vlist[y][:3] + '11' + vlist[y][6:]
                if vlist[y][3:6] == 'Dec':
                    vlist[y] = vlist[y][:3] + '12' + vlist[y][6:]

                vlist[y] = "20" + vlist[y][6:8] + vlist[y][2:6] + vlist[y][0:2]

        return vlist               
                                    
    i = 0
    for line in data: ## reads rows as array
         if i > 3: ## skip first 3 rows
            for y in range(len(line)): ## iter row items replace / , and ""
                while '/' in line[y]:
                    line[y] = line[y].replace('/',"")
                while ',' in line[y]:
                    line[y] = line[y].replace(',',"")
                if line[y] == "":
                    line[y] = 0
            line = convert_date(line) ## convert dates in line
            line.append(report_date) ## append report_date column
            line.append(report_date + line[0]) ## append LoanIDDate column
            line.append(str(line[3])[0:2]) ## append BranchID column
            line.append('\n') ## append new line
            line = ','.join([str(z) for z in line]) ## join array in string by ,
            if line.find('Total') == -1:
                w_file.write(line) ## write string to csv if Total not in line (avoids total row)

         i += 1
