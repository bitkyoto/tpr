from pulp import *
v = [[8, 5,  7,  5,  7],
     [7, 14, 13, 4,  7],
     [7, 11, 7,  12, 9]]
c = [2, 2, 7] # стоимость доставки от станции до складов
s = [60, 60, 1000] # емкость складов
d = [[7,21,23,71,23],
     [35,4,9,38,50]]
xxx1 = [[[0 for _ in range(2)] for _ in range(5)] for _ in range(3)]
yyy1 = [[0 for _ in range(2)] for _ in range(3)]
# целевая функция для анализа чувствительности
def obf(xxx,yyy,vvv,ccc, vvvv):
    for j in range(5):
        vvv[0][j]=vvvv[j]
    return sum(xxx[i][j][t]*vvv[i][j] for i in range(3) for j in range(5) for t in range(2))+sum(yyy[i][t]*ccc[i] for i in range(3) for t in range(2))

# Создаем экземпляр класса LpProblem с определенным типом решаемой задачи (minimize)
prob = LpProblem("TransportationProblem", LpMinimize)
yit = [(x,y) for x in range(1,4) for y in range(1,3)]
xi1 = [[(x,y,1) for x in range(1,4)] for y in range(1,6)]
xi2 = [[(x,y,2) for x in range(1,4)] for y in range(1,6)]
xj1 = [[(y,x,1) for x in range(1,6)] for y in range(1,4)]
xj2 = [[(y,x,2) for x in range(1,6)] for y in range(1,4)]

# переменные
xijt = [(x,y,1) for x in range(1,4) for y in range(1,6)] + [(x,y,2) for x in range(1,4) for y in range(1,6)]
varp1={}
for pp in xijt:
    varp1[pp]=(LpVariable("x(%s,%s,%s)"%pp,lowBound=0,cat="Integer"))
varp2={}
for pp in yit:
    varp2[pp]=(LpVariable("y(%s,%s)"%pp,lowBound=0,cat="Integer"))
# бинарные переменные mtj для учёта того, что на 1 и 2 складах товар расходуется полностью
# varp3={}
# for pp in range(1,3):
#     varp3[pp]=(LpVariable("m(%s)"%pp,lowBound=0,upBound=1,cat="Integer"))
# целевая функция
of = ""
for (u1,v1) in [(x,y) for x in range(1,4) for y in range(1,6)]:
    of += lpSum([varp1[(u1,v1,t)]*v[u1-1][v1-1] for t in range(1,3)])
for u1 in range(1,4):
    of += lpSum([varp2[(u1,t)]*c[u1-1] for t in range(1,3)])
prob += of
for (u1,v1,z1) in xijt:
    prob+=varp1[(u1,v1,z1)]<=min(s[u1-1],d[z1-1][v1-1])
ss1 = sum(d[0][j] for j in range(5))
ss2 = sum(d[1][j] for j in range(5))
for u1 in range(1,4):
    prob+=varp2[(u1,1)]<=min(s[u1-1],ss1)
    prob+=varp2[(u1,2)]<=min(s[u1-1],ss2)
prob+=lpSum([varp2[pp] for pp in [(1,1),(2,1),(3,1)]])==160
prob+=lpSum([varp2[pp] for pp in [(1,2),(2,2),(3,2)]])==160
for i in range(len(xi1)):
    prob+=lpSum([varp1[j] for j in xi1[i]])==d[0][i]
    prob+=lpSum([varp1[j] for j in xi2[i]])==d[1][i]

for i in range(len(xj1)):
    prob += lpSum([varp1[j] for j in xj1[i]]) <= s[i]
    prob += lpSum([varp1[j] for j in xj2[i]]) <= s[i]

# prob+=lpSum([varp1[pp] for pp in [(1,1,1),(1,2,1),(1,3,1),(1,4,1),(1,5,1)]])+lpSum([varp1[pp] for pp in [(2,1,1),(2,2,1),(2,3,1),(2,4,1),(2,5,1)]])<=lpSum([varp1[pp] for pp in [(3,1,1),(3,2,1),(3,3,1),(3,4,1),(3,5,1)]])+min(ss1,s[2])*varp3[(1)]
# prob+=lpSum([varp1[pp] for pp in [(1,1,1),(1,2,1),(1,3,1),(1,4,1),(1,5,1)]])+lpSum([varp1[pp] for pp in [(2,1,1),(2,2,1),(2,3,1),(2,4,1),(2,5,1)]])>=lpSum([varp1[pp] for pp in [(3,1,1),(3,2,1),(3,3,1),(3,4,1),(3,5,1)]])-min(ss1,s[2])*(1-varp3[(1)])
# # Второй период
# prob+=lpSum([varp1[pp] for pp in [(1,1,2),(1,2,2),(1,3,2),(1,4,2),(1,5,2)]])+lpSum([varp1[pp] for pp in [(2,1,2),(2,2,2),(2,3,2),(2,4,2),(2,5,2)]])<=lpSum([varp1[pp] for pp in [(3,1,2),(3,2,2),(3,3,2),(3,4,2),(3,5,2)]])+min(ss2,s[2])*varp3[(2)]
# prob+=lpSum([varp1[pp] for pp in [(1,1,2),(1,2,2),(1,3,2),(1,4,2),(1,5,2)]])+lpSum([varp1[pp] for pp in [(2,1,2),(2,2,2),(2,3,2),(2,4,2),(2,5,2)]])>=lpSum([varp1[pp] for pp in [(3,1,2),(3,2,2),(3,3,2),(3,4,2),(3,5,2)]])-min(ss2,s[2])*(1-varp3[(2)])
#

# prob+=lpSum([varp2[pp] for pp in [(1,1),(2,1),(3,1)]])>=lpSum([varp1[pp] for pp in [(1,x,1) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(2,x,1) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(3,x,1) for x in range(1,6)]])
# prob+=lpSum([varp2[pp] for pp in [(1,2),(2,2),(3,2)]])==lpSum([varp1[pp] for pp in [(1,x,2) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(2,x,2) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(3,x,2) for x in range(1,6)]])
prob+=lpSum([varp2[pp] for pp in [(1,1),(1,2)]])==lpSum([varp1[pp] for pp in [(1,x,1) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(1,x,2) for x in range(1,6)]])
prob+=lpSum([varp2[pp] for pp in [(2,1),(2,2)]])==lpSum([varp1[pp] for pp in [(2,x,1) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(2,x,2) for x in range(1,6)]])
prob+=lpSum([varp2[pp] for pp in [(3,1),(3,2)]])>=lpSum([varp1[pp] for pp in [(3,x,1) for x in range(1,6)]])+lpSum([varp1[pp] for pp in [(3,x,2) for x in range(1,6)]])
# prob+=varp2[(1,1)]==lpSum([varp1[pp] for pp in [(1,x,1) for x in range(1,6)]])
# prob+=varp2[(1,2)]==lpSum([varp1[pp] for pp in [(1,x,2) for x in range(1,6)]])
# prob+=varp2[(2,1)]==lpSum([varp1[pp] for pp in [(2,x,1) for x in range(1,6)]])
# prob+=varp2[(2,2)]==lpSum([varp1[pp] for pp in [(2,x,2) for x in range(1,6)]])
# prob+=varp2[(3,1)]>=lpSum([varp1[pp] for pp in [(3,x,1) for x in range(1,6)]])
# prob+=varp2[(3,2)]>=lpSum([varp1[pp] for pp in [(3,x,2) for x in range(1,6)]])

print(prob)
# решаем задачи линейного программирования
prob.solve(PULP_CBC_CMD(msg=0))
# выводим оптимальное решение
print('Оптимальное решение:')
print(f'Общие транспортные расходы = {pulp.value(prob.objective)}')
for (i,t) in yit:
    print(f'Доставлено {varp2[(i,t)].value()} единиц от станции до склада {i} в период {t}')
for (i,j,t) in xijt:
    print(f'Доставлено {varp1[(i,j,t)].value()} единиц от склада {i} до объекта {j} в период {t}')

for i in range(3):
    for j in range(5):
        for t in range(2):
            xxx1[i][j][t]=varp1[(i+1,j+1,t+1)].value()
for i in range(3):
    for t in range(2):
        yyy1[i][t]=varp2[(i+1,t+1)].value()
#
# vvvv1 = [7,9,14,5,1]
# vvvv2 = [1,9,14,5,1]
# vvvv3 = [17,9,14,5,1]
# print(obf(xxx1,yyy1,v,c,vvvv1))
# print(obf(xxx1,yyy1,v,c,vvvv2))
# print(obf(xxx1,yyy1,v,c,vvvv3))
# print("Изменение цены доставки от 1 склада до первого объекта не меняет общие транспортные расходы")
# vvvv1 =[7,9,14,5,1]
# vvvv2 = [7,1,14,5,1]
# vvvv3 = [7,19,14,5,1]
# print(obf(xxx1,yyy1,v,c,vvvv1))
# print(obf(xxx1,yyy1,v,c,vvvv2))
# print(obf(xxx1,yyy1,v,c,vvvv3))
# print("Изменение цены доставки от 1 склада до 2 объекта не меняет общие транспортные расходы")
# vvvv1 = [7,9,14,5,1]
# vvvv2 = [7,9,1,5,1]
# vvvv3 = [7,9,7,5,1]
# print(obf(xxx1,yyy1,v,c,vvvv1))
# print(obf(xxx1,yyy1,v,c,vvvv2))
# print(obf(xxx1,yyy1,v,c,vvvv3))
# print("Изменение цены доставки от 1 склада до 3 объекта не меняет общие транспортные расходы")
# vvvv1 = [7,9,14,5,1]
# vvvv2 = [7,9,14,1,1]
# vvvv3 = [7,9,14,15,1]
# print(obf(xxx1,yyy1,v,c,vvvv1))
# print(obf(xxx1,yyy1,v,c,vvvv2))
# print(obf(xxx1,yyy1,v,c,vvvv3))
# print("Изменение цены доставки от 1 склада до 4 объекта не меняет общие транспортные расходы")
# vvvv1 = [7,9,14,5,1]
# vvvv2 = [7,9,14,5,7]
# vvvv3 = [7,9,14,5,18]
# print(obf(xxx1,yyy1,v,c,vvvv1))
# print(obf(xxx1,yyy1,v,c,vvvv2))
# print(obf(xxx1,yyy1,v,c,vvvv3))
# print("Увеличение цены доставки от 1 склада до 5 объекта увеличивает общие транспортные расходы")