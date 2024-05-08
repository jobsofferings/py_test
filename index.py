from app import start_web
import json

def handler(request, response):
    # 调用函数
    result = start_web()

    # 处理结果并返回响应
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.set_data(json.dumps(result))