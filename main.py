from pulp import *
v = [[7,9,14,5,1],
     [3,8,12,7,6],
     [3,6,9,1,13]]
c = [2,6,3] # стоимость доставки от станции до складов
s = [70,70,150] # емкость складов
d = [[26,12,9,66,1],
     [65,16,55,9,10]]
xxx1 = [[[0 for _ in range(2)] for _ in range(5)] for _ in range(3)]
yyy1 = [[0 for _ in range(2)] for _ in range(3)]
# целевая функция для анализа чувствительности
def obf(xxx,yyy,vvv,ccc, vvvv):
    for j in range(5):
        vvv[0][j]=vvvv[j]
    return sum(xxx[i][j][t]*vvv[i][j] for i in range(3) for j in range(5) for t in range(2))+sum(yyy[i][t]*ccc[i] for i in range(3) for t in range(2))

# Создаем экземпляр класса LpProblem с определенным типом решаемой задачи (minimize)
prob = LpProblem("TransportationProblem", LpMinimize)
# индексы количество товара поставленного от складов до магазинов в заданный период

xijt = [(x,y,1) for x in range(1,4) for y in range(1,6)] + [(x,y,2) for x in range(1,4) for y in range(1,6)]
# без периодов
xij = [(x,y) for x in range(1,4) for y in range(1,6)]
#индексы количество товара поставленного от станции до складов в заданный период
# yit = [(1,1),(2,1),(3,1),
# # второй период
# (1,2),(2,2),(3,2)]
yit = [(x,y) for x in range(1,4) for y in range(1,3)]
yi_ = [[(x,y) for x in range(1,4)] for y in range(1,3)]
yi1 = [(1,1),(2,1),(3,1)]
yi2 = [(1,2),(2,2),(3,2)]
# индексы потребности магазинов в заданный период
dtj = [(x,y) for x in range(1,3) for y in range(1,6)]
xji = [(x,y) for x in range(1,4) for y in range(1,6)]
#индексы для 1го магазина в 1 период
xi1 = [[(x,y,1) for x in range(1,4)] for y in range(1,6)]
xi11 = [(x,1,1) for x in range(1,4)]
xi21 = [(x,2,1) for x in range(1,4)]
xi31 = [(x,3,1) for x in range(1,4)]
xi41 = [(x,4,1) for x in range(1,4)]
xi51 = [(x,5,1) for x in range(1,4)]
#второй период
xi2 = [[(x,y,2) for x in range(1,4)] for y in range(1,6)]
xi12 = [(x,1,2) for x in range(1,4)]
xi22 = [(x,2,2) for x in range(1,4)]
xi32 = [(x,3,2) for x in range(1,4)]
xi42 = [(x,4,2) for x in range(1,4)]
xi52 = [(x,5,2) for x in range(1,4)]
# индексы склад 1 период
xj1_ = [[(y,x,1) for x in range(1,6)] for y in range(1,4)] #по сути это равно xj1
x1j1 = [(1,x,1) for x in range(1,6)]
x2j1 = [(2,x,1) for x in range(1,6)]
x3j1 = [(3,x,1) for x in range(1,6)]
# индексы склад 2 период
xj2_ = [[(y,x,2) for x in range(1,6)] for y in range(1,4)] #по сути это равно xj2
x1j2 = [(1,x,2) for x in range(1,6)]
x2j2 = [(2,x,2) for x in range(1,6)]
x3j2 = [(3,x,2) for x in range(1,6)]
xj1 = [[(y,x,1) for x in range(1,6)] for y in range(1,4)]
xj2 = [[(y,x,2) for x in range(1,6)] for y in range(1,4)]
yt = [[(x,y)] for x in range(1,4) for y in range(1,3)]
y1t = [(1,1),(1,2)]
y2t = [(2,1),(2,2)]
y3t = [(3,1),(3,2)]

# переменные
varp1={}
for pp in xijt:
    varp1[pp]=(LpVariable("x(%s,%s,%s)"%pp,lowBound=0,cat="Integer"))
varp2={}
for pp in yit:
    varp2[pp]=(LpVariable("y(%s,%s)"%pp,lowBound=0,cat="Integer"))
# бинарные переменные mtj для учёта того, что на 1 и 2 складах товар расходуется полностью
varp3={}
for pp in range(1,3):
    varp3[pp]=(LpVariable("m(%s)"%pp,lowBound=0,upBound=1,cat="Integer"))
# целевая функция
of = ""
for (u1,v1) in xij:
    of += lpSum([varp1[(u1,v1,t)]*v[u1-1][v1-1] for t in range(1,3)])
for u1 in range(1,4):
    of += lpSum([varp2[(u1,t)]*c[u1-1] for t in range(1,3)])
prob += of
for (u1,v1,z1) in xijt:
 # ограничения по емкости складов
 # и ограничения по потребности магазинов
    prob+=varp1[(u1,v1,z1)]<=min(s[u1-1],d[z1-1][v1-1])
ss1 = sum(d[0][j] for j in range(5))
ss2 = sum(d[1][j] for j in range(5))
ss3 = sum(s[j] for j in range(3))
for u1 in range(1,4):
    prob+=varp2[(u1,1)]<=min(s[u1-1],ss1)
    prob+=varp2[(u1,2)]<=min(s[u1-1],ss2)
prob+=lpSum([varp2[pp] for pp in yi1])==ss1
prob+=lpSum([varp2[pp] for pp in yi2])==ss2
for i in range(len(xi1)):
    for j in range(3):
        prob+=lpSum([varp1[xi1[i][j]]])==d[0][i]
for i in range(len(xi1)):
    for j in range(3):
        prob+=lpSum([varp1[xi2[i][j]]])==d[1][i]

# # prob+=lpSum([varp1[pp] for pp in xi11])==d[0][0]
# prob+=lpSum([varp1[pp] for pp in xi12])==d[1][0]
# # prob+=lpSum([varp1[pp] for pp in xi21])==d[0][1]
# prob+=lpSum([varp1[pp] for pp in xi22])==d[1][1]
# # prob+=lpSum([varp1[pp] for pp in xi31])==d[0][2]
# prob+=lpSum([varp1[pp] for pp in xi32])==d[1][2]
# # prob+=lpSum([varp1[pp] for pp in xi41])==d[0][3]
# prob+=lpSum([varp1[pp] for pp in xi42])==d[1][3]
# # prob+=lpSum([varp1[pp] for pp in xi51])==d[0][4]
# prob+=lpSum([varp1[pp] for pp in xi52])==d[1][4]
prob+=lpSum([varp1[pp] for pp in x1j1])<=s[0]
prob+=lpSum([varp1[pp] for pp in x2j1])<=s[1]
prob+=lpSum([varp1[pp] for pp in x3j1])<=s[2]
prob+=lpSum([varp1[pp] for pp in x1j2])<=s[0]
prob+=lpSum([varp1[pp] for pp in x2j2])<=s[1]
prob+=lpSum([varp1[pp] for pp in x3j2])<=s[2]

prob+=lpSum([varp1[pp] for pp in x1j1])+lpSum([varp1[pp] for pp in x2j1])<=lpSum([varp1[pp] for pp in x3j1])+min(ss1,s[2])*varp3[(1)]
prob+=lpSum([varp1[pp] for pp in x1j1])+lpSum([varp1[pp] for pp in x2j1])>=lpSum([varp1[pp] for pp in x3j1])-min(ss1,s[2])*(1-varp3[(1)])
#второй период
prob+=lpSum([varp1[pp] for pp in x1j2])+lpSum([varp1[pp] for pp in x2j2])<=lpSum([varp1[pp] for pp in x3j2])+min(ss2,s[2])*varp3[(2)]
prob+=lpSum([varp1[pp] for pp in x1j2])+lpSum([varp1[pp] for pp in x2j2])>=lpSum([varp1[pp] for pp in x3j2])-min(ss2,s[2])*(1-varp3[(2)])

prob+=lpSum([varp2[pp] for pp in yi1])==lpSum([varp1[pp] for pp in x1j1])+lpSum([varp1[pp] for pp in x2j1])+lpSum([varp1[pp] for pp in x3j1])
prob+=lpSum([varp2[pp] for pp in yi2])==lpSum([varp1[pp] for pp in x1j2])+lpSum([varp1[pp] for pp in x2j2])+lpSum([varp1[pp] for pp in x3j2])
prob+=lpSum([varp2[pp] for pp in y1t])==lpSum([varp1[pp] for pp in x1j1])+lpSum([varp1[pp] for pp in x1j2])
prob+=lpSum([varp2[pp] for pp in y2t])==lpSum([varp1[pp] for pp in x2j1])+lpSum([varp1[pp] for pp in x2j2])
prob+=lpSum([varp2[pp] for pp in y3t])==lpSum([varp1[pp] for pp in x3j1])+lpSum([varp1[pp] for pp in x3j2])
prob+=varp2[(1,1)]==lpSum([varp1[pp] for pp in x1j1])
prob+=varp2[(1,2)]==lpSum([varp1[pp] for pp in x1j2])
prob+=varp2[(2,1)]==lpSum([varp1[pp] for pp in x2j1])
prob+=varp2[(2,2)]==lpSum([varp1[pp] for pp in x2j2])
prob+=varp2[(3,1)]==lpSum([varp1[pp] for pp in x3j1])
prob+=varp2[(3,2)]==lpSum([varp1[pp] for pp in x3j2])
#print(prob)
# решаем задачи линейного программирования
prob.solve()
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
# for i in range(3):
#     for t in range(2):
#         yyy1[i][t]=varp2[(i+1,t+1)].value()
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