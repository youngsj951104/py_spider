import requests
sum=0
for i in range(1, 101):
    params ={
        "group": "rs", #接口名称
        "action": "Match22_getdata", #注册的服务名
        "page": i
    }
    res = requests.get("http://127.0.0.1:5601/asyncInvoke", params=params).json()
    for value in res['data']:
        num = int(value['value'].replace('\r', ''))
        sum = sum + num
    print('前' + str(i) + '页结果为：' + str(sum))
    # print(res.json())
