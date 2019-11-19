import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
#import plotly.offline as pyo

df_original = pd.read_excel('Premium_test.xlsx')
df_xlsx = df_original.copy()
col, row = df_xlsx.shape
df_xlsx.insert(2, 'non_empty_count', (df_xlsx.apply(lambda x: x.count(), axis=1)))
df_xlsx.insert(3, 'Total', (df_xlsx.sum(axis=1) - df_xlsx['non_empty_count']))
df_xlsx.insert(4, 'Average', (df_xlsx['Total'] / (df_xlsx['non_empty_count'] - 2)))
#print(df_xlsx)
df_xlsx_t = df_xlsx.T
df_xlsx_t = df_xlsx_t.reset_index()
df_xlsx_t.rename(columns={'index':'Raw_Date'}, inplace = True)
df_xlsx_t.insert(1, 'Date', (df_xlsx_t.Raw_Date.str.split(",",expand=True,)[0]))
df_xlsx_t.insert(2, 'Time', (df_xlsx_t.Raw_Date.str.split(",",expand=True,)[1]))
#print(df_xlsx_t)


tmp_df_1 = df_xlsx_t.iloc[0:5]
tmp_df_1 = tmp_df_1.drop(columns = ['Raw_Date', 'Time'])
#print(tmp_df_1)
tmp_df_1_t = tmp_df_1.set_index('Date').transpose()
#print(tmp_df_1_t)
tmp_df_2 = df_xlsx_t.iloc[5:df_xlsx_t.shape[0]]
tmp_df_2 = tmp_df_2.reset_index(drop=True)
tmp_df_4 = tmp_df_2.copy()
tmp_df_4 = tmp_df_4.drop(columns = ['Raw_Date', 'Time'])
#print(tmp_df_4)
tmp_df_3 = pd.DataFrame((list(dict.fromkeys(tmp_df_2['Date']))), columns = ['Date'])
tmp_df_2 = tmp_df_2.groupby(tmp_df_2.index // 4).sum()
tmp_df_2 = tmp_df_2.drop(columns = ['Raw_Date', 'Date', 'Time'])
tmp_df_2 = tmp_df_2.div(4)
tmp_df_2 = pd.concat([tmp_df_3,tmp_df_2], axis = 1)
#print(tmp_df_2)
tmp_df_com_avg = tmp_df_1.iloc[4:]
tmp_df_com_avg = tmp_df_com_avg.reset_index(drop=True)
tmp_df_com_avg = tmp_df_com_avg.append([tmp_df_com_avg]*(tmp_df_2.shape[0] - 1),ignore_index=True)
#print(tmp_df_com_avg)
tmp_df_2_t = tmp_df_2.set_index('Date').transpose()
#print(tmp_df_2_t)

def one_stn_all_day_avg(stn_no):
	#one station, all day average
	#station starts from 1
	y = tmp_df_2.iloc[:, stn_no]
	#print(y)
	stn_det = tmp_df_1.iloc[0,(stn_no)] + ': ' + tmp_df_1.iloc[1,(stn_no)]
	x = tmp_df_2.iloc[:, 0]
	z = tmp_df_com_avg.iloc[:, stn_no]
	#print(x)
	#print(z)
	plt.plot(x,y)
	plt.plot(z, 'r--', label='Average')
	plt.legend()
	plt.title('Price for the station ' + stn_det)
	plt.xlabel('Dates')
	plt.ylabel('price in cents')
	plt.show()

def all_stn_one_day_split(day):
	#day strts at 1
	#all station one time
	x = df_xlsx['Address']
	z = df_xlsx['Average']
	#print(x)
	y = df_xlsx.iloc[:, (day + 4) ]
	title = df_xlsx.columns[(day + 4) ]
	#print(y)
	#print (title)
	plt.plot(x,y)
	plt.plot(z, 'r--', label='Average')
	plt.legend()
	plt.title('Prices for all the stations at ' + title)
	plt.xlabel('Address')
	plt.ylabel('price in cents')
	plt.show()

def all_stn_one_day_avg(day):
	#day strts at 1
	#all station one day
	x = df_xlsx['Address']
	#print(x)
	y = tmp_df_2_t.iloc[0:, (day-1) ]
	#print(y)
	z = df_xlsx['Average']
	#print (z)
	title = tmp_df_2_t.columns[(day -1 ) ]
	plt.plot(x,y)
	plt.plot(z, 'r--', label='Average')
	plt.legend()
	plt.title('Prices for all the stations at ' + title)
	plt.show()

def one_stn_n_day_split(stn_no, no_of_days):
	#station starts from 1
	tmp_df = df_xlsx[df_xlsx.columns[-(no_of_days*4):]]
	#print(tmp_df)
	x = tmp_df.iloc[(stn_no-1)]
	x = x.reset_index() 
	x.columns = ['Date', 'Average']
	print(x)
	y = x.copy()
	y.loc[y['Average'] > 0, 'Average'] = df_xlsx['Average'][(stn_no-1)]
	print(y)
	#####average
	title = df_xlsx['Address'][(stn_no-1)]
	#print(title)
	plt.plot(x['Date'],x['Average'])
	plt.plot(y['Date'],y['Average'], 'r--', label='Average')
	plt.legend()
	plt.title('Prices for station '+title+ ' for last ' +str(no_of_days)+ ' days')
	plt.show()

def one_stn_n_day_avg(stn_no, no_of_days):
	tmp_df_avg = tmp_df_2_t[tmp_df_2_t.columns[-(no_of_days):]]
	#print(tmp_df_avg)
	x = tmp_df_avg.iloc[(stn_no-1)]
	x = x.reset_index()
	x.columns = ['Date', 'Average']
	#print(x)
	y = x.copy()
	y.loc[y['Average'] > 0, 'Average'] = tmp_df_1_t['Average'][(stn_no-1)]
	#print(y)
	title = tmp_df_1_t['Address'][(stn_no-1)]
	#print(title)
	plt.plot(x['Date'],x['Average'])
	plt.plot(y['Date'],y['Average'], 'r--', label='Average')
	plt.legend()
	plt.title('Prices for station '+title+ ' for last ' +str(no_of_days)+ ' days')
	plt.show()

def one_stn_range_day_avg(stn_no, date1, date2):
	# one station rates,between given range
	df_range = tmp_df_2_t.loc[:, date1:date2]
	#print(df_range)
	df_range = df_range.iloc[(stn_no-1)]
	df_range = df_range.reset_index()
	df_range.columns = ['Date', 'Average']
	#print(df_range)
	#####add average
	y = df_range.copy()
	y.loc[y['Average'] > 0, 'Average'] = tmp_df_1_t['Average'][(stn_no-1)]
	#print(y)
	title = tmp_df_1_t['Address'][(stn_no-1)]
	plt.plot(df_range['Date'],df_range['Average'])
	plt.plot(y['Date'],y['Average'], 'r--', label='Average')
	plt.legend()
	plt.title('Prices for station '+title+ ' from date ' +date1+ ' to ' +date2)
	plt.show()

######completed
#one_stn_all_day_avg(1)  #### in this try to do average with lists 
#all_stn_one_day_split(1)  ####stn names formatting
#all_stn_one_day_avg(1)   ######stn names formatiing
#one_stn_n_day_split(12,3)
#one_stn_n_day_avg(1,4)
#one_stn_range_day_avg(5, '10/12', '10/15')

#######in progress
