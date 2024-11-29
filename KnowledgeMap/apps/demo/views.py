# from django.http import HttpResponse
# from django.shortcuts import render
# from gstore_api.gStoreCloud import gStoreCloud
# # 存在两次以上反复发作的思睡
# def index(request, **kwargs):
#     # classes = kwargs.get('classes')
#     return HttpResponse(render(request, 'demo/tsest3.html')
#                         # context = {'classes':data.keys(),}
#                         )
#
# # 初始化gStoreCloud对象
# gstore = gStoreCloud(api_key="66988263966e43d791f24e42d5c965f2", api_secret="1A150AF9D1AE9A1ECDAF586335F94741")
# db_name = "睡眠test"
#
# # 定义初始数据结构
# initial_data = {'睡眠障碍疾病病种': [], '症状与临床表现': ['存在两次以上反复发作的思睡','打鼾','呼吸暂停','test']}
# data = {'名称': '', '症状与临床表现': [], '易感因素': [], '预防措施及诊疗建议': []}
#
# # 定义视图所用SPARQL查询语句
# def sparql1(y):
#     yh = "select ?x where{?x <关联关系><%s>.}" % y
#     return yh
#
# def sparql2(y):
#     sparqls = []
#     for i in y:
#         yh = "select ?x where{<%s> <关联关系>?x.}" % i
#         sparqls.append(yh)
#     return sparqls
#
# # 解析JSON格式数据
# def Parse_Json(result):
#     global initial_data
#
#     bindings = result.get('data', {}).get('results', {}).get('bindings', [])
#     results = []
#     for item in bindings:
#         result1 = item.get('x', {}).get('value')
#         if "睡眠障碍疾病病种" in result1 and result1 not in initial_data['睡眠障碍疾病病种']:
#             initial_data['睡眠障碍疾病病种'].append(result1.split('/')[-1])
#             # print(initial_data)
#         if "症状与临床表现" in result1 and result1 not in initial_data['症状与临床表现']:
#             initial_data['症状与临床表现'].append(result1.split('/')[-1])
#             # print(initial_data)
#         results.append(result1)
#     return results
#
# # 定义展示数据所用SPARQL查询语句
# def sparql3(y):  # 查找预防措施及诊疗建议
#     sparql = "select ?x where{<%s><建议适用>?x .}" % y
#     return sparql
#
# def sparql4(y):  # 查找易感因素
#     sparql = "select ?x where{<%s> <风险评估>?x.}" % y
#     return sparql
#
# def sparql5(y):  # 查找症状与临床表现
#     sparql = "select ?x where{<%s> <关联关系>?x.}" % y
#     return sparql
#
#
# # 解析JSON格式数据
# def Parse_Json1(disease_name,result):
#     global data
#     # print(result)
#     data = { '名称': '','症状与临床表现': [], '易感因素': [], '预防措施及诊疗建议': []}
#     data['名称'] = disease_name
#     bindings = result.get('data', {}).get('results', {}).get('bindings', [])
#     results = []
#     for item in bindings:
#         result1 = item.get('x', {}).get('value')
#         print(result1)
#         if "睡眠障碍疾病病种" in result1:
#             data['名称'] = result1.split('/')[-1]
#             print(data)
#         if "症状与临床表现" in result1:
#             data['症状与临床表现'].append(result1.split('/')[-1])
#             print(data)
#         if '易感因素' in result1:
#             data['易感因素'].append(result1.split('/')[-1])
#             print(data)
#         if '预防措施及诊疗建议' in result1:
#             data['预防措施及诊疗建议'].append(result1.split('/')[-1])
#             print(data)
#     return results
#
#
# def test(request, **kwargs):
#     # 每次请求时重置数据
#     global initial_data
#     # initial_data = {'初始供选择症状':['存在两次以上反复发作的思睡','打鼾','呼吸暂停','test'],'睡眠障碍疾病病种': [], '症状与临床表现': []}
#     if request.method == 'POST':
#         symptoms = request.POST.get('symptoms')
#         symptoms = "症状与临床表现/" + symptoms
#         sparql = sparql1(symptoms)
#         result = gstore.queryDB(db_name, sparql)
#         result1 = Parse_Json(result)
#         sparql_second = sparql2(result1)
#         for i in sparql_second:
#             sub_result = gstore.queryDB(db_name, i)
#             Parse_Json(sub_result)
#         # print('initial_data',initial_data)
#     return HttpResponse(render(request, 'demo/tsest3.html', {'data1': initial_data}))
#
# def test1(request, **kwargs):
#     # 每次请求时重置数据
#     global data
#     # data = {'名称': '', '症状与临床表现': [], '易感因素': [], '预防措施及诊疗建议': []}
#     if 'disease_name' in request.POST:
#         disease_name = request.POST.get('disease_name')
#         disease_name1 = "睡眠障碍疾病病种/" + disease_name
#         data['名称'] = disease_name.split('/')[-1]
#         sparql = sparql3(disease_name1)
#         result = gstore.queryDB(db_name, sparql)
#         Parse_Json1(disease_name,result)
#
#         sparql = sparql4(disease_name1)
#         result = gstore.queryDB(db_name, sparql)
#         Parse_Json1(disease_name,result)
#
#         sparql = sparql5(disease_name1)
#         result = gstore.queryDB(db_name, sparql)
#         Parse_Json1(disease_name,result)
#
#     return HttpResponse(render(request, 'demo/test1.html', {'data2': data}))
