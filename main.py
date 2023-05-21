from qgis.core import QgsVectorLayer, QgsGeometry, QgsPoint, QgsFeature
import networkx as nx

# открываем слой с дорогами, вытаскиваем все объекты слоя (Features)
pathLayer = 'C:/Whoosh/src/result.TAB'
layer = QgsVectorLayer(pathLayer, pathLayer, "ogr")
Features = layer.getFeatures()
# достаем геометрию объектов и создаем список для инициализации графов в виде:
# ['37.54666,55.598908', '37.546631,55.598658', 25.16763795052755]), где 1 и 2 - это str координаты, 3 - длина отрезка
dots = []
for Feature in Features:
	nodes = []
	a = Feature.geometry()
	b = a.asPolyline()
	for el in b:
		x = el.x()
		y = el.y()
		node = str(x) + "," + str(y)
		nodes.append(node)
	nodes.append(a.length() * 100000)
	dots.append(nodes)

# создаем граф, инициализируем ребра и определяем самый короткий путь от заданных точек
G = nx.Graph()
for dot in dots:
	G.add_edge(dot[0], dot[1], weight=dot[2])
rez = nx.shortest_path(G, "37.550055,55.595598", "37.553792,55.598109", weight="weight")

# результат в виде списка строк, переводим обратно во float и создаем объект QgsPoint(x, y) - точку
point_list = []
for point in rez:
	lst = point.split(",")
	float_lst = [float(x) for x in lst]
	x = float_lst[0]
	y = float_lst[1]
	point = QgsPoint(x, y)
	point_list.append(point)

# из точек создаем объект polyline
polyline = QgsGeometry.fromPolyline(point_list)

#записыввем линию в слой
pathLayer1 = 'C:/Whoosh/src/done.tab'
lyr = QgsVectorLayer(pathLayer1, pathLayer1, "ogr")
feat = QgsFeature(lyr.fields())
feat.setGeometry(polyline)
lyr.dataProvider().addFeatures([feat])

#обновление карты
lyr.triggerRepaint()