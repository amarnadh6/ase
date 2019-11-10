import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import plotly.offline as pyo
#from openpyxl.workbook import Workbook
#import chart_studio.tools as tls

df_d_xlsx = pd.read_excel('Diesel.xlsx')
df_xlsx = pd.read_excel('Premium.xlsx')
#print(df_xlsx)
col, row = df_xlsx.shape
col_d, row_d = df_d_xlsx.shape
#print (row_d, col_d)
#print ('no of stations', col+1)
df_xlsx['non_empty_count'] = df_xlsx.apply(lambda x: x.count(), axis=1)
df_xlsx['Total'] = df_xlsx.iloc[:, 2:(row)].sum(axis=1)
df_xlsx['Average'] = df_xlsx['Total'] / (df_xlsx['non_empty_count'] - 2)
#print(df_xlsx[['Total', 'non_empty_count', 'Average']])

#print(df_xlsx [['Station', 'Address', 'Average']])
#print(df_xlsx.describe())
#plot of one set, station and one date
def complete_day():
	no = input("Enter day number")
	stn = int(no)
	x = df_xlsx['Address']
	y = df_xlsx.iloc[:, (stn + 1) ]
	#some variable which shows he heading of the day
	day = df_xlsx.columns[stn + 1]
	#data comparison for a single day across all stations
	plt.plot(y, x)
	plt.title('Price for the date ' + day)
	plt.ylabel('Address')
	plt.xlabel('price in cents')
	plt.show()
	pyo.plot([{
		'x' : df_xlsx.iloc[:, (stn + 1) ],
		'y' : df_xlsx['Address']
			}])

def class_name_1():
	#print(df_xlsx.iloc[1])
	#which station, starts from 0
	stn_name = 0
	no_of_days = 10
	company_and_address = df_xlsx.iloc[stn_name,0] + ':' + df_xlsx.iloc[stn_name,1]
	j = df_xlsx.iloc[stn_name,2:(no_of_days+2)]
	#dayz = df_xlsx.columns[(stn_name + 2) : (stn_name + 2 + no_of_days)]
	#print(dayz)
	plt.plot(j)
	plt.title(company_and_address)
	plt.ylabel('Price in cents')
	plt.xlabel('Day and Time(in 24 hr format)')
	plt.show()
	pyo.plot([{
		'x' : df_xlsx.columns[(stn_name + 2) : (stn_name + 2 + no_of_days)],
		'y' : df_xlsx.iloc[stn_name,2:(no_of_days+2)]
	}])

def class_name_3():
	#print(df_xlsx.iloc[1])
	#which station, starts from 0
	stn_name_1 = 0
	stn_name_2 = 1
	stn_name_3 = 5
	#my case max vale of no_of_days is 18
	no_of_days = 5
	name_and_address_1 = df_xlsx.iloc[stn_name_1,0] + ':' + df_xlsx.iloc[stn_name_1,1]
	#print(complete_name_1)
	k = df_xlsx.iloc[stn_name_1,2:(no_of_days+2)]
	name_and_address_2 = df_xlsx.iloc[stn_name_2,0] + ':' + df_xlsx.iloc[stn_name_2,1]
	l = df_xlsx.iloc[stn_name_2,2:(no_of_days+2)]
	name_and_address_3 = df_xlsx.iloc[stn_name_3,0] + ':' + df_xlsx.iloc[stn_name_3,1]
	n = df_xlsx.iloc[stn_name_3,2:(no_of_days+2)]
	#need to add legend for this graph
	plt.plot(k, label = name_and_address_1)
	plt.plot(l, label = name_and_address_2)
	plt.plot(n, label = name_and_address_3)
	plt.ylabel('Price in cents')
	plt.xlabel('Day and Time(in 24 hr format)')
	plt.title(name_and_address_1 + ' "VS" ' + name_and_address_2 + ' "VS" ' + name_and_address_3)
	plt.legend()
	plt.show()
	pyo.plot([{
		'x' : df_xlsx.iloc[stn_name_1,2:(no_of_days+2)]
	}])
	pyo.plot([{
		'x' : df_xlsx.iloc[stn_name_2,2:(no_of_days+2)]
	}])
	pyo.plot([{
		'x' : df_xlsx.iloc[stn_name_3,2:(no_of_days+2)]
	}])

def company_average():
	aa = 0
	bb = 0
	my_list = []
	count = 0
	sum_tot = 0
	df = pd.DataFrame(list(dict.fromkeys(df_xlsx['Station'])), columns = ['Station'])
	df['Count'] = np.nan
	df['Average'] = np.nan
	for aa in range(len(df)):
		for bb in range(len(df_xlsx)):
			if (df.loc[aa, "Station"]) == (df_xlsx.loc[bb, "Station"]):
				sum_tot = sum_tot + (df_xlsx.loc[bb, "Average"])
				count = count + 1
		df.loc[aa, "Count"] = count
		df.loc[aa, "Average"] = sum_tot/count
		count = 0
		sum_tot = 0
	print(df)
	#plot graphs
	#(count and station)
	plt.plot(df['Station'], df['Count'])
	plt.show()
	#(average and station)
	plt.plot(df['Station'], df['Average'])
	plt.show()

def one_company_average():
	usr_inp = 'Petro Canada'
	new_df = df_xlsx.loc[(df_xlsx['Station'] == usr_inp)]
	print(new_df)
	#from this data, display address vs average
	plt.plot(new_df['Address'], new_df['Average'])
	plt.show()

#complete_day()
#class_name_1()
#class_name_3()
#company_average()
one_company_average()