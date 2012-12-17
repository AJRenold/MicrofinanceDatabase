#!/usr/bin/env python

from subprocess import check_output
import flask
from flask import request, redirect, url_for, make_response
from os import environ
import os
from flask import jsonify
from werkzeug import secure_filename
from clean_data import *
from create_csv import *
from datetime import datetime

## Build - delete csv file from db
## Build - API for Loan Officer data

##
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://microfinance:hq7Np2Ex@/microfinance', convert_unicode=True)

##

UPLOAD_FOLDER = '/groups/microfinance/csvfiles'
ALLOWED_EXTENSION = set(['csv'])
app = flask.Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## connection = engine.connect()
## connection.execute("sql command")

@app.route('/')
def index():
    """index page"""
    return flask.render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
	filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION

def read_data(file_path):
    connection = engine.connect()    
    
    file_path = file_path[file_path.index('csvfiles'):]  
  
    connection.execute("LOAD DATA LOCAL INFILE '" + file_path + "' IGNORE INTO TABLE Clients FIELDS TERMINATED BY ',' (@dummy, ClientID, Name)")

    connection.execute("LOAD DATA LOCAL INFILE '" + file_path + "' IGNORE INTO TABLE Loans FIELDS TERMINATED BY ','(LoanID, ClientID, @dummy, LOID, DisbAmount, DisbDate, Category, @dummy, @dummy, @dummy, MatDate, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, BranchID)")

    connection.execute("LOAD DATA LOCAL INFILE '" + file_path + "' IGNORE INTO TABLE LoanVal FIELDS TERMINATED BY ',' (LoanID, @dummy, @dummy, @dummy, @dummy, @dummy, @dummy, NextPmtAmt, NextPmt, Principal, @dummy, LateIntCollected, DaysPD, PDPrincipal, PDInterest, LateInt, PenaltyInt, ReportDate, LoanIDDate)")

    connection.close()

@app.route('/fileupload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
	file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(path)
	    clean_data(path,request.form['report_date'])	   
            os.remove(path)
	    ## function with database connection and mysql script
	    ## takes the csv file path as an arguement
	    read_data(str(path[:path.index('.')] + request.form['report_date'] + '.csv'))
	    
	    return flask.redirect('microfinance/')
    return 'file upload failed'

@app.route('/OrgData',methods=['get'])
def get_org_data():
    connection = engine.connect()

    data = connection.execute("select LoanVal.ReportDate, COUNT(LoanVal.Principal) as 'loanClients', SUM(LoanVal.Principal) as 'principalBalance', SUM(IF( LoanVal.DaysPD > 1, LoanVal.Principal, 0)) as 'principal1Day', SUM(IF( LoanVal.DaysPD > 30, LoanVal.Principal, 0)) as 'Principal30Day' from Branch, Loans, LoanVal where Branch.BranchID = Loans.BranchID and Loans.LoanID = LoanVal.LoanID group by LoanVal.ReportDate;")

    connection.close()

    toJSON = []
    for row in data:
        row_as_dict = dict(row)	
        toJSON.append(row_as_dict)

    for item in toJSON:
        item['ReportDate'] = item['ReportDate'].strftime("%Y-%m-%d")
    
    return jsonify(results = toJSON)

@app.route('/BranchData',methods=['get'])
def get_branch_data():
    connection = engine.connect()
    toJSON = []
    branches = [10,11,12,13,14,15]
    #branch = request.args['branch']
    for branch in branches:
        data = connection.execute("select LoanVal.ReportDate, COUNT(LoanVal.Principal) as 'loanClients', SUM(LoanVal.Principal) as 'principalBalance', SUM(IF( LoanVal.DaysPD > 1, LoanVal.Principal, 0)) as 'principal1Day', SUM(IF( LoanVal.DaysPD > 30, LoanVal.Principal, 0)) as 'Principal30Day' from Loans, LoanVal where Loans.LoanID = LoanVal.LoanID and Loans.BranchID = "+str(branch)+" group by LoanVal.ReportDate;")

        branch_data = []
        for row in data:
            row_as_dict = dict(row) 
            branch_data.append(row_as_dict)
        for item in branch_data:
            item['ReportDate'] = item['ReportDate'].strftime("%Y-%m-%d")

        if branch == 10:
            headoffice = branch_data
        if branch == 11:
            arusha = branch_data
        if branch == 12:
            dar = branch_data
        if branch == 13:
            moshi = branch_data
        if branch == 14:
            tengeru = branch_data
        if branch == 15:
            himo = branch_data

    connection.close()

    return jsonify(ho  = headoffice, ar = arusha, da = dar, mo = moshi, te = tengeru, hi = himo)


@app.route('/BranchDataFile',methods=['get'])
def get_branch_data_file():
    connection = engine.connect()
    branches = [10,11,12,13,14,15]
    #branch = request.args['branch']
    data_for_csv = []
    for branch in branches:
        data = connection.execute("select LoanVal.ReportDate, COUNT(LoanVal.Principal) as 'loanClients', SUM(LoanVal.Principal) as 'principalBalance', SUM(IF( LoanVal.DaysPD > 1, LoanVal.Principal, 0)) as 'principal1Day', SUM(IF( LoanVal.DaysPD > 30, LoanVal.Principal, 0)) as 'Principal30Day' from Loans, LoanVal where Loans.LoanID = LoanVal.LoanID and Loans.BranchID = "+str(branch)+" group by LoanVal.ReportDate;")
        data_for_csv.append([branch,data])

    connection.close()

    (file_basename, server_path, file_size) = create_csv(data_for_csv)

    return_file = open(server_path+file_basename, 'r')

    response = make_response(return_file,200)
    response.headers['Content-Description'] = 'File Transfer'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % file_basename
    response.headers['Content-Length'] = file_size 
    return response


@app.route('/LoanOfficerData',methods=['GET'])
def get_loan_officer_data():

## needs to iterate through dates in db
## needs to accept arg BranchID
    accepted_branches = ['10','11','12','13','14','15']

    branch = request.args['branch']
    if branch not in accepted_branches:
        flask.render_template('index.html'), 404

    connection = engine.connect()
    
    dates = []
    date_query = connection.execute("select distinct ReportDate from LoanVal;")
    for row in date_query:
        row_as_dict = dict(row)
        row_as_dict['ReportDate'] = row_as_dict['ReportDate'].strftime("%Y-%m-%d")
        dates.append(row_as_dict)

    loan_officer_data = []
 
    for date in dates:

        data = connection.execute("select LO.Name, COUNT(LoanVal.Principal) as 'loanClients', SUM(LoanVal.Principal) as 'principalBalance', SUM(IF( LoanVal.DaysPD > 1, LoanVal.Principal, 0)) as 'principal1Day', SUM(IF( LoanVal.DaysPD > 30, LoanVal.Principal, 0)) as 'Principal30Day' from LO, Loans, LoanVal where LO.LOID = Loans.LOID and Loans.LoanID = LoanVal.LoanID and LoanVal.ReportDate = '"+date['ReportDate']+"' and Loans.BranchID = "+branch+" group by LO.Name;")

        temp = []
        for row in data:
            row_as_dict = dict(row)
            temp.append(row_as_dict)
        
        loan_officer_data.append([date['ReportDate'],temp])

    connection.close()

    return jsonify(results = loan_officer_data)

@app.route('/CsvDataFiles',methods=['GET','DELETE'])
def get_csv_files():

    if request.method == 'GET':
        csv_files = []
        for files in os.walk(UPLOAD_FOLDER):
            csv_files.append(files[2])        
        csv_files = csv_files[0]    
    
        return jsonify(files = csv_files)

    if request.method == 'DELETE':
        files_string = request.data
        files_string = files_string.split('&')
        files_delete = [] 
        for item in files_string:
            files_delete.append(item[item.index('=')+1:])
        
        for item in files_delete:
             date = item[item.index('.')-10:item.index('.')]
             os.remove(UPLOAD_FOLDER+'/'+item)
             connection = engine.connect()
             connection.execute("DELETE FROM LoanVal WHERE ReportDate = '" + date + "';")

        connection.close()

        return "Deleted " + ' '.join(files_delete)

if __name__ == "__main__":
    app.run(port=60050)
