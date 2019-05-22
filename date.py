# coding=utf-8
import pandas as pd
from datetime import datetime
import numpy as np

def datetime_format(date, format = "%Y-%m-%dT%H:%M:%S.000Z"):
	date_formated = []
	for i in date:
		temp = datetime.strptime(i, format)
		date_formated.append(temp)
	return date_formated

def date(date_time):
	result = []
	for i in date_time:
		result.append(i.date())
	return np.array(result)

def feature_unique_order(feature):
	uni =[]
	uni.append(feature[0])
	compare = feature[0]
	for i in range(1, len(feature)):
		if feature[i] != compare:
			uni.append(feature[i])
			compare = feature[i]
		else:
			continue
	return np.array(uni)

def merge_array(arr, n):
	"""
	arr = [(1,2,..n),(),(),...]
	:param arr: mảng
	:param n: cột thứ mấy
	:return: mảng là cột thứ n
	"""
	re = []
	for i in arr:
		re.append(i[n])
	return np.array(re)

def hour(date_time):
	result = []
	for i in date_time:
		result.append(i.hour)
	return np.array(result)

def calculate(arr):
	"""

	:param arr:
	:return: array [start, end, max, min, average]
	"""
	max = arr[0]
	min = arr[0]
	temp = arr[0]
	start = arr[0]
	end = arr[len(arr)-1]
	for i in range(1, len(arr)):
		if arr[i] <= min:
			min = arr[i]
		if arr[i] >= max:
			max = arr[i]
		temp += arr[i]
	average = temp/len(arr)
	result = []
	result.append(max)
	result.append(min)
	result.append(start)
	result.append(end)
	result.append(average)
	return np.array(result)

def split_data(date_time, feature, value):
	"""
	Chia dữ liệu thành:
	array = [array_ngày_1, array_ngày_2, ... array_ngày_n]
	array_ngày_1 = [(ngày, feature, value)1, ...(ngày, feature, value)n]
	:param date_time:
	:param feature:
	:param value:
	:return:
	"""
	date_spl = date(date_time)
	date_sql_unique = np.unique(date_spl)
	i = 0
	j = 0
	temp = []
	result = []
	while i < len(date_time):
		if date_time[i].date() == date_sql_unique[j]:
			# process
			temp.append((date_time[i], feature[i], value[i]))
			i += 1
		else:
			j += 1
			result.append(temp)
			temp = []
			continue
	result.append(temp)
	return np.array(result)

def split_data_everyday(data_one_day):
	"""

	:param data_one_day:
	:return: array [' Nhiệt độ không khí' ' Ánh sáng' ' Gió' ' Độ ẩm không khí' ' Mưa'
 	' Hướng gió']
 	Nhiệt độ không khí = [(date, value)i ...]
	"""
	arr_date = merge_array(data_one_day,0)
	arr_feature = merge_array(data_one_day,1)
	arr_value = merge_array(data_one_day,2)
	feature_unique = feature_unique_order(arr_feature)

	result = []
	temp = []
	i = 0
	j = 0
	while i < len(arr_feature):
		if arr_feature[i] == feature_unique[j]:
			temp.append((arr_date[i], arr_value[i]))
			i += 1
		else:
			j += 1
			result.append(temp)
			temp = []
			continue
	result.append(temp)
	return result

def split_data_everyhour(data_every_feature):
	"""
	chia dữ liệu 1 thuộc tính ra từng giờ
	:param data_every_feature:
	:return: array [23,22,...i...0]
	trong đó i là 1 array(value_i,...)
	"""
	arr_date = merge_array(data_every_feature,0)
	arr_value = merge_array(data_every_feature,1)
	hours = feature_unique_order(hour(arr_date))
	i = 0
	j = 0
	temp = []
	result = []
	while i < len(arr_date):
		if arr_date[i].hour == hours[j]:
			temp.append(arr_value[i])
			i += 1
		else:
			j += 1
			result.append(temp)
			temp = []
			continue
	result.append(temp)
	return result

def process_data_every_hour(data_one_feature):
	"""

	:param data_one_feature:
	:return: array (max, min, start, end, average)
	"""
	data_feature_every_hour = split_data_everyhour(data_one_feature)
	result = []
	for i in data_feature_every_hour:
		temp = calculate(i)
		result.append(temp)
	# print(result)
	return np.array(result)
	# return result

def process_data_every_day(data_one_day):
	"""

	:param data_one_day:
	:return:
	"""
	result = []
	data_feature = split_data_everyday(data_one_day)
	for i in data_feature:
		temp = process_data_every_hour(i)
		result.append(temp)
	return np.array(result)
	# return result

def process_data(data):
	"""
	data đã split rồi -> ngày 1, ngày 2, ngày i, ... ngày n
	:param data:
	:return:
	"""
	result = []
	for i in data:
		temp = process_data_every_day(i)
		result.append(temp)
	return np.array(result)

def save_toexcel():
	row1 = [1, 2, 3, 4]
	row2 = [1, 2, 3, 4]
	row = []
	row.append(row1)
	row.append(row2)
	df = pd.DataFrame(np.array(row))
	name = "output.csv"
	df.to_csv(name, index=False)

def save_tocsv(data):
	row = []
	for i in data:
		# ngày
		temp = []
		for j in i:
			# giò
			for k in j:
				temp.append(k[0])
				temp.append(k[1])
				temp.append(k[2])
				temp.append(k[3])
				temp.append(k[4])
		row.append(temp)
	df = pd.DataFrame(np.array(row))
	name = "output.csv"
	df.to_csv(name,header=False, index=False)

def main():
	df = pd.read_csv("VEC_LacDuong.csv", header=None)
	date_time = np.array(datetime_format(df[0]))
	feature = np.array(df[4])
	value = np.array(df[5])
	data_temp = split_data(date_time, feature, value)
	# delete data bị thiếu nhiều -> tạm thời -> bước này quan sát làm tay!!!!!!!!
	data = data_temp[1:]
	result = process_data(data)
	# for i in result:
	# 	print("Ngay: ", np.where(result == i))
	# 	for j in i:
	# 		print("Feature: ", np.where(i == j))
	# 		for k in j:
	# 			print("Hour: ", np.where(j == k))
	# 			print(k[0], k[1], k[2], k[3], k[4])
	# for i in range(0, len(result)):
	# 	print("Ngày: ", i)
	# 	temp1 = result[i]
	# 	for j in range(0, len(temp1)):
	# 		print("Feature: ", j)
	# 		temp2 = temp1[j]
	# 		for k in range(0, len(temp2)):
	# 			print("Hour", k)
	# 			print(temp2[k][0], temp2[k][1], temp2[k][2], temp2[k][3], temp2[k][4])
	save_tocsv(result)
main()