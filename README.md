# 矩阵模逆计算器

一个用于计算矩阵模逆的 Web 工具，适用于希尔密码等密码学场景。

## 功能特点

- 支持 1x1 到 10x10 的方阵
- 自定义模数（默认 26，适用于希尔密码）
- 实时计算并显示行列式值和模逆矩阵
- 现代化响应式界面

## 在线使用

1. 输入矩阵大小 N
2. 输入模数（默认 26）
3. 填入 N×N 矩阵的值
4. 点击"计算模逆"获得结果

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问 http://localhost:5000
```

## 计算原理

1. 计算行列式的值 D，判断 `gcd(D, N) = 1`，否则矩阵不可逆
2. 计算行列式值对 N 的模逆 `D_invert`
3. 计算每个位置的代数余子式 Aij，乘以 D_invert 并模 N
4. 将矩阵转置，得到模逆矩阵

## 技术栈

- Python Flask
- HTML/CSS/JavaScript

## License

MIT
