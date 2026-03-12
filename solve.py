from math import gcd
import copy

MOD = 26


# 简单求模逆
def modInvert(a):
    a = a % MOD
    if (gcd(a, MOD) != 1):
        return None
    for i in range(1, 26):
        if (i * a % MOD == 1):
            return i


# 运用欧几里得算法,求模逆
def modInvert2(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


# 定义1*n维矩阵乘法，a是1*n的矩阵，b是n*n的矩阵
def matrixMulty(a, b):
    ans = copy.deepcopy(a)
    for i in range(0, len(b)):
        temp = 0
        for j in range(0, len(b[i])):
            temp += a[j] * b[j][i]
        ans[i] = temp % MOD
    return ans


# 计算逆序数的函数，没什么用
def calculateTao(num):
    # num=[]
    ans = 0
    for i in range(0, len(num) - 1):
        for j in range(i + 1, len(num)):
            if (num[j] < num[i]):
                ans += 1
    ans = (-1) ** ans
    return ans


# print(calculateTao([3,4,5,1,2]))
# 求行列式的值
def calculateD(a):
    leng = len(a)
    if (leng == 2):
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if (leng == 1):
        return a[0][0]
    if (leng == 0):
        return None
    add, sub = 0, 0
    # 加法
    for i in range(0, leng):
        y, x, temp = i, 0, 1
        for j in range(0, leng):
            temp *= a[x][y]
            x += 1
            x = x % leng
            y += 1
            y = y % leng
        add += temp
    # 减法
    for i in range(leng - 1, -1, -1):
        y, x, temp = i, 0, 1
        for j in range(0, leng):
            temp *= a[x][y]
            x -= 1
            x = x % leng
            y += 1
            y = y % leng
        sub -= temp
    return (sub + add) % 26


# 矩阵转置函数,返回矩阵
def matrixReverse(matrix):
    ans = copy.deepcopy(matrix)
    leng = len(ans)
    for i in range(0, leng):
        for j in range(i + 1, leng):
            ans[i][j], ans[j][i] = ans[j][i], ans[i][j]
    return ans


# 求代数余子式,返回行列式的值的模逆
def initAC(matrix, x, y, D):
    leng = len(matrix)
    ans = []
    # x,y是坐标，matrix为矩阵
    for i in range(0, leng):
        row = []
        if (i == x):
            continue
        for j in range(0, leng):
            if (j == y):
                continue
            row.append(matrix[i][j])
        ans.append(row)
    d = (-1) ** (x + 1 + y + 1) * calculateD(ans)
    return D * d % 26


N = 0
encryKey = []
decryKey = []
c, m = [], []
encryDinvert = 0


# 生成密钥矩阵
def initKey():
    global N, encryKey, decryKey, encryDinvert
    ans = []
    for i in range(0, N):
        row = []
        for j in range(0, N):
            row.append(initAC(encryKey, i, j, encryDinvert))
        ans.append(row)
    ans = matrixReverse(ans)
    print('你的密钥：', ans)
    return ans


def encry():
    global N, m, encryKey
    m = []  # 将m清空
    if (N == 0):
        print("请先生成密钥")
        return 0
    print("输入待加密的数据，一共{}个".format(N))
    m = list(map(int, input('>').split(' ')))
    global c
    c = matrixMulty(m, encryKey)


def decry():
    global N, c, decryKey
    mm = []
    if (N == 0):
        print("请先生成")
        return 0
    print('密文：', c)
    print('密钥:', decryKey)
    mm = matrixMulty(c, decryKey)
    print('解密出的明文为：', mm)


def work():
    global N
    N = eval(input('请输入矩阵大小N:'))
    global encryKey, decryKey, encryDinvert
    encryKey, decryKey = [], []  # 将密钥清空
    for i in range(0, N):
        row = list(map(int, input('请输入第' + str(i) + '行:').split(" ")))
        encryKey.append(row)
    encryD = calculateD(encryKey)
    encryDinvert = modInvert(encryD)
    if (encryDinvert == None):
        print('你的加密行列式的值为：', end=str(encryD))
        print(",你的行列式没有模{}的逆".format(MOD))
        return (-1)
    print('行列式的值的逆：', encryDinvert, '行列式的值：', encryD)
    decryKey = initKey()
    print("你的密钥：", decryKey)


def menu():
    print("1.生成密钥\n2.加密\n3.解密")
    select = eval(input('>'))
    if (select == 1):
        work()
    if (select == 2):
        encry()
    if (select == 3):
        decry()


while (True):
    menu()