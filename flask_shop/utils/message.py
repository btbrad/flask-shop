status_msg = {
    '200': '成功',
    '10000': '数据不完整',
    '10011': '用户名不合法',
    '10012': '密码不合法',
    '10013': '两次密码不一致',
    '10014': '手机号不合法',
    '10015': '邮箱不合法',
    '20000': '异常错误'
}

def to_dict_msg(status: 200, data=None, msg=None):
    return {
        'status': status,
        'msg': msg if msg else status_msg[str(status)],
        'data': data
    }

if __name__ == '__main__':
    print(to_dict_msg(200))