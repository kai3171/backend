from flask import Flask
import rpy2.robjects as robjects

# 创建应用实例
app = Flask(__name__)


# 视图函数（路由）
def func():
    to = robjects.r['pi']
    return (to[0])


f = func()


@app.route('/using')
def test():
    global f
    print(f)
    return '<h1>Hello!<h1>'


@app.route('/')
def index():
    return '<h1>Hello Flask!<h1>'


if __name__ == '__main__':
    app.run()
