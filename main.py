import json
from collections import defaultdict


class StageNode(object):
	"""
	两个站点之间的线路节点类
	"""
	# 起点
	start = ''
	# 终点
	end = ''
	# 所用时间，不是同一条线的话，time为999,line为0
	time = 999
	# 所在线路
	line = 0


def get_matrix():
	"""
	获取邻接矩阵
	:return:
	"""
	with open('./data/station_new_data.json', encoding='utf-8') as f:
		lines_di = defaultdict(list)
		# 所有站点
		stations = set()
		# key:线路，value:所有站点
		line_station_di = defaultdict(list)
		# key:线路，value:所有站点的时间
		line_time_di = defaultdict(list)
		for i in f:
			lines = i.strip().split('\t')[0]
			start = i.strip().split('\t')[1]
			end = i.strip().split('\t')[2]
			times = int(i.strip().split('\t')[3])

			stations.add(start)
			stations.add(end)

			lines_di[start].append(lines)
			lines_di[end].append(lines)

			if start not in line_station_di[lines]:
				line_station_di[lines].append(start)

			if end not in line_station_di[lines]:
				line_station_di[lines].append(end)
			line_time_di[lines].append(times)

		stations_li = list(stations)
		stations_li.sort(reverse=True)

		# 站点的index字典，通过站名获取其index
		stations_index_li = {i: ind for ind, i in enumerate(stations_li)}

		# 站点和站点之间的邻接矩阵，交点为StageNode实例对象，具有四个属性
		matrix_li = list()
		for m in stations_li:
			line_li = list()
			for n in stations_li:
				stage_node = StageNode()
				stage_node.start = m
				stage_node.end = n

				# 是否有相同的线路
				same_line_li = list(set([i for i in lines_di.get(m, []) if i in lines_di.get(n, [])]))
				if same_line_li:
					# 如果有共同的线路，则获取共同线路的所需时间
					same_time_li = list()
					# print(same_line_li)
					for s in same_line_li:
						index_one = line_station_di[s].index(m)
						index_two = line_station_di[s].index(n)
						if index_one > index_two:
							index_one, index_two = index_two, index_one
						# print(index_one, index_two)
						time_li = line_time_di[s][index_one:index_two]
						time_num = sum(time_li)
						same_time_li.append(time_num)
					# print(m, n)
					# print(same_time_li)
					li = list(zip(same_time_li, same_line_li))
					li = sorted(li, key=lambda x: x[0], reverse=False)
					new_time = li[0][0]
					new_line = li[0][1]
					# print('-'*50)

					stage_node.time = new_time
					stage_node.line = new_line

				else:

					stage_node.time = 999
					stage_node.line = 0

				line_li.append((stage_node.time, [stage_node]))
			# print(line_li)
			matrix_li.append(line_li)
	return matrix_li, stations_index_li, line_station_di, line_time_di


def get_line(source, target):
	"""获取乘车线路"""
	# 起始站点的index
	start_index = stations_index_li[source]
	# 终点站的index
	end_index = stations_index_li[target]

	# 以起始点为起点到各点的路线列表，这个列表非常重要，后面更新的是这个列表
	start_li = matrix_li[start_index]
	path_li = [0 for i in range(len(stations_index_li))]
	path_li[0] = 1

	# 换乘时间
	transfer_time = 3
	# 换乘的线路节点类
	transfer_node = StageNode()
	transfer_node.start = '换乘'
	transfer_node.end = '换乘'
	transfer_node.time = transfer_time
	transfer_node.line = '换乘'

	# 算法核心
	for i in range(len(stations_index_li)):
		short_time = 1000
		short_index = 0
		# 找到最近的点
		for ind, a in enumerate(start_li):
			if path_li[ind] == 0 and a[0] < short_time:
				short_time = a[0]

				short_index = ind

		path_li[short_index] = 1
		# print(short_index)
		# 以该点作为中转站，看其他点到各点距离会不会更近，如果更近，就更新这段列表
		# print(short_time, short_index)
		for j in range(len(stations_index_li)):
			if start_li[short_index][0] + transfer_time + matrix_li[short_index][j][0] < \
					start_li[j][0]:
				a = [i for i in start_li[short_index][1]]

				a.append(transfer_node)

				for new_a in matrix_li[short_index][j][1]:
					a.append(new_a)
				total_time = sum([i.time for i in a])
				start_li[j] = (total_time, a)

	# 打印起点到终点的路线
	ret_li = list()
	ret_di = dict()
	ret_di['time'] = start_li[end_index][0]
	ret_di['line_li'] = ret_li
	for route in start_li[end_index][1]:
		start = route.start
		end = route.end
		lines = route.line
		times = route.time
		# print('-' * 100)
		if start != '换乘':
			line_station_di_reverse = line_station_di[lines][::-1]
			line_time_di_reverse = line_time_di[lines][::-1]

			index_one = line_station_di[lines].index(start)
			index_two = line_station_di[lines].index(end)
			if index_one > index_two:
				index_one = line_station_di_reverse.index(start)
				index_two = line_station_di_reverse.index(end)
				station_li = line_station_di_reverse[index_one:index_two + 1]
				time_li = line_time_di_reverse[index_one:index_two]
			else:
				station_li = line_station_di[lines][index_one:index_two + 1]
				time_li = line_time_di[lines][index_one:index_two]

			one_line_di = dict()
			one_line_di['line'] = lines
			one_line_di['time'] = times
			one_line_di['station'] = list()

			for ind, st in enumerate(station_li):
				if ind != station_li.__len__() - 1:
					start_station = station_li[ind]
					end_station = station_li[ind + 1]
					use_time = time_li[ind]
					one_li = (start_station, end_station, use_time)
					one_line_di['station'].append(one_li)

			ret_li.append(one_line_di)
		else:
			pass
			# print('换乘')
	return ret_di


if __name__ == '__main__':
	matrix_li, stations_index_li, line_station_di, line_time_di = get_matrix()
	transfer_li = get_line('航头东', '虹桥火车站')
	print(transfer_li)