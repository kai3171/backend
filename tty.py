from flask import Flask,jsonify,request
from flask_cors import *
app = Flask(__name__)
CORS(app,supports_credentials = True)

student_info1 = {"id":1,"name":"张三","gender":"男","className":"一班"}
student_info2 = {"id": 2, "name": "王五", "gender": "男", "className": "二班"}
student_info3 = {"id": 3, "name": "李六", "gender": "男", "className": "三班"}
student_info4 = {"id": 4, "name": "欧拉欧拉", "gender": "男", "className": "四班"}
student_info5 = {"id": 5, "name": "小六", "gender": "男", "className": "五班"}
student_info = [student_info1,student_info2,student_info3,student_info4,student_info5]

#　访问接口：http://127.0.0.1:5000/student
# 请求方式：GET
@app.route('/student/')
def student():
    return jsonify(student_info)

# # 访问接口：http://127.0.0.1:5000/student/find_student_by_id/1 (这个1可以改成2，3，4)
# # 请求方式：GET
# @app.route('/student/find_student_by_id/<int:student_id>')
# def find_student_by_id(student_id):
#     for student in student_info:
#         if student["id"]==student_id:
#             return jsonify(student)

# 访问接口：http://127.0.0.1:5000/student/find_student_by_id?id=1 (这个1可以改成2，3，4)
# 请求方式：GET
@app.route('/student/find_student_by_id')
def find_by_id():
    student_id = request.args.get('id')
    for student in student_info:
        if student["id"]==eval(student_id):
            return jsonify(student)


# 访问接口：http://127.0.0.1:5000/student/find_student_by_name
# 请求方式：POST
@app.route('/student/find_student_by_name',methods=['POST'])
def find_student_by_name():
    # axios返回的数据为application/json，因此我们要用get_json方法
    student_name = request.get_json(silent=True)
    # print(student_name)
    for student in student_info:
        if student["name"]==student_name['name']:
            return jsonify(student)


if __name__ == '__main__':
    app.run(debug=True)

