from flask import Flask, render_template, request, jsonify
from math import gcd
import copy

app = Flask(__name__)


def mod_invert(a, m):
    """运用扩展欧几里得算法，求模逆"""
    a = a % m
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def calculate_determinant(a, m):
    """计算行列式的值（模m）"""
    leng = len(a)
    if leng == 2:
        return (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % m
    if leng == 1:
        return a[0][0] % m
    if leng == 0:
        return None

    add, sub = 0, 0
    # 对角线加法
    for i in range(0, leng):
        y, x, temp = i, 0, 1
        for j in range(0, leng):
            temp *= a[x][y]
            x += 1
            x = x % leng
            y += 1
            y = y % leng
        add += temp
    # 反对角线减法
    for i in range(leng - 1, -1, -1):
        y, x, temp = i, 0, 1
        for j in range(0, leng):
            temp *= a[x][y]
            x -= 1
            x = x % leng
            y += 1
            y = y % leng
        sub -= temp
    return (sub + add) % m


def matrix_transpose(matrix):
    """矩阵转置"""
    ans = copy.deepcopy(matrix)
    leng = len(ans)
    for i in range(0, leng):
        for j in range(i + 1, leng):
            ans[i][j], ans[j][i] = ans[j][i], ans[i][j]
    return ans


def get_algebraic_cofactor(matrix, x, y, d_invert, m):
    """求代数余子式，返回值的模逆"""
    leng = len(matrix)
    ans = []
    for i in range(0, leng):
        row = []
        if i == x:
            continue
        for j in range(0, leng):
            if j == y:
                continue
            row.append(matrix[i][j])
        ans.append(row)
    d = (-1) ** (x + y) * calculate_determinant(ans, m)
    return (d_invert * d) % m


def matrix_mod_inverse(matrix, mod):
    """计算矩阵的模逆"""
    n = len(matrix)

    # 计算行列式
    det = calculate_determinant(matrix, mod)

    # 计算行列式的模逆
    det_inverse = mod_invert(det, mod)
    if det_inverse is None:
        return None, f"行列式值 {det} 与模数 {mod} 不互质，矩阵不可逆"

    # 构造逆矩阵
    result = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(get_algebraic_cofactor(matrix, i, j, det_inverse, mod))
        result.append(row)

    # 转置
    result = matrix_transpose(result)

    return result, None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        matrix = data['matrix']
        mod = data['mod']

        # 验证输入
        if not matrix or not isinstance(matrix, list):
            return jsonify({'success': False, 'error': '矩阵格式错误'})

        n = len(matrix)
        if n == 0:
            return jsonify({'success': False, 'error': '矩阵不能为空'})

        for row in matrix:
            if len(row) != n:
                return jsonify({'success': False, 'error': f'请输入 {n}x{n} 的方阵'})

        # 计算模逆
        result, error = matrix_mod_inverse(matrix, mod)

        if error:
            return jsonify({'success': False, 'error': error})

        det = calculate_determinant(matrix, mod)
        det_inverse = mod_invert(det, mod)

        return jsonify({
            'success': True,
            'result': result,
            'determinant': det,
            'determinant_inverse': det_inverse
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
