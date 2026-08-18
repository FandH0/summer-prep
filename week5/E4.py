import sys


l, d, n, *gas_stations = map(int, sys.stdin.read().split())
gas_stations.append(l)  # добавление конечной точки
counts = 0
car = 0
prev_station = 0
for station in gas_stations:
    if station - prev_station > d:  # условие заправки
        if station - car > d:  # дотянет ли до следующей заправки
            sys.stdout.write('-1')
            break
        prev_station = car  # заправка
        counts += 1
    car = station  # движение от заправки только если дотянет до следующей
else:
    sys.stdout.write(str(counts))
