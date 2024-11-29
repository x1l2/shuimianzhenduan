from django.http import HttpResponse
from django.shortcuts import render
from gstore_api.gStoreCloud import gStoreCloud

# 初始化gStoreCloud对象
gstore = gStoreCloud(api_key="66988263966e43d791f24e42d5c965f2", api_secret="1A150AF9D1AE9A1ECDAF586335F94741")
db_name = "图谱睡眠"

# 定义初始数据结构
initial_data = {'可能患的睡眠疾病': ["特发性过度睡眠","慢性偏头痛","多发性硬化合并睡眠障碍",'不宁腿综合征（RLS）','阻塞性睡眠呼吸暂停','日间过度思睡（EDS）',
                '睡眠期周期性肢体运动（PLMS）','孤独症谱系障碍（ASD）儿童睡眠障碍','中枢性睡眠呼吸暂停','短期失眠症','慢性失眠症','成年人阻塞性睡眠呼吸暂停低通气综合征','失眠症'],
                '症状与临床表现': [],'易感因素':[]}
initial_data1 = {'可能患的睡眠疾病': [],'症状与临床表现': [],'易感因素':[]}
data = {'名称': '', '症状与临床表现': [], '易感因素': [], '预防措施及诊疗建议': []}

# 定义视图所用SPARQL查询语句
def sparql_1(y):
    sparqls = ''
    i = "睡眠障碍疾病病种/%s/#%s"%(y,y)
    # print("dsas",i)
    yh = "select ?x where{<%s><关联关系>?x.}" % i
    sparqls = yh
    # print("sparqls=",sparqls)
    return sparqls

def sparql1(y):
    yh = "select ?x where{?x <关联关系><%s>.}" % y
    return yh

def sparql2(y):
    sparqls = []
    for i in y:
        yh = "select ?x where{<%s> <关联关系>?x.}" % i
        sparqls.append(yh)
    return sparqls

def sparql3(y):  # 查找预防措施及诊疗建议
    sparql = "select ?x where{?x<建议适用关系><%s> .}" % y
    return sparql

def sparql4(y):  # 查找易感因素及症状与临床表现
    sparql = "select ?x where{<%s> <关联关系>?x.}" % y
    return sparql

# def sparql5(y):  # 查找症状与临床表现
#     sparql = "select ?x where{<%s> <关联关系>?x.}" % y
#     return sparql

# 定义解析JSON格式数据的函数
def Parse_Json_1(result):
    bindings = result.get('data', {}).get('results', {}).get('bindings', [])
    results = []
    for item in bindings:
        result1 = item.get('x', {}).get('value')
        if "睡眠障碍疾病病种" in result1:
            result1 = result1.split('/#')[-1]
            if result1 not in initial_data['可能患的睡眠疾病']:
                initial_data['可能患的睡眠疾病'].append(result1.split('/#')[-1])
            # print(initial_data)
        if "症状与临床表现" in result1:
            result1 = result1.split('/#')[-1]
            if result1 not in initial_data['症状与临床表现']:
                initial_data['症状与临床表现'].append(result1.split('/#')[-1])
            # print(initial_data)
        if "易感因素" in result1:
            result1 = result1.split('/#')[-1]
            if result1 not in initial_data['易感因素']:
                initial_data['易感因素'].append(result1.split('/#')[-1])
    print(initial_data)
    return results

def Parse_Json(result):
    global initial_data1
    bindings = result.get('data', {}).get('results', {}).get('bindings', [])
    results = []
    for item in bindings:
        result1 = item.get('x', {}).get('value')
        if "睡眠障碍疾病病种" in result1 and result1 not in initial_data1['可能患的睡眠疾病']:
            initial_data1['可能患的睡眠疾病'].append(result1.split('/#')[-1])
            # print(initial_data1)
        if "症状与临床表现" in result1 and result1 not in initial_data1['症状与临床表现']:
            initial_data1['症状与临床表现'].append(result1.split('/#')[-1])
            # print(initial_data1)
        if '易感因素' in result1 and result1 not in initial_data1['易感因素']:
            initial_data1['易感因素'].append(result1.split('/#')[-1])
        results.append(result1)
    return results

def Parse_Json1(disease_name,result):
    global data
    # print(result)
    data = { '名称': '','症状与临床表现': [], '易感因素': [], '预防措施及诊疗建议': []}
    data['名称'] = disease_name
    bindings = result.get('data', {}).get('results', {}).get('bindings', [])
    results = []
    for item in bindings:
        result1 = item.get('x', {}).get('value')
        print(result1)
        if "睡眠障碍疾病病种" in result1:
            data['名称'] = result1.split('/#')[-1]
            print(data)
        if "症状与临床表现" in result1:
            data['症状与临床表现'].append(result1.split('/#')[-1])
            print(data)
        if '易感因素' in result1:
            data['易感因素'].append(result1.split('/#')[-1])
            print(data)
        if '预防措施及诊疗建议' in result1:
            data['预防措施及诊疗建议'].append(result1.split('/#')[-1])
            print(data)
        results.append(result1)
    return results


# 定义视图函数
def index(request, **kwargs):
    # classes = kwargs.get('classes')
    return HttpResponse(render(request, 'demo/tsest3.html')
                        # context = {'classes':data.keys(),}
                        )


def test(request, **kwargs):
    # 每次请求时重置数据
    global initial_data
    global initial_data1
    if request.method == 'POST':
        initial_data1 = {'可能患的睡眠疾病': [], '症状与临床表现': [], '易感因素': []}
        symptoms = request.POST.get('symptoms')

        symptom1 = "症状与临床表现/%s/#%s"%(symptoms,symptoms)
        sparql = sparql1(symptom1)
        result = gstore.queryDB(db_name, sparql)
        result1 = Parse_Json(result)
        # print("result1=",result1)
        sparql_second = sparql2(result1)
        for i in sparql_second:
            sub_result = gstore.queryDB(db_name, i)
            Parse_Json(sub_result)

        symptom = "易感因素/%s/#%s" % (symptoms, symptoms)
        sparql = sparql1(symptom)
        result = gstore.queryDB(db_name, sparql)
        result1 = Parse_Json(result)
          # print("result1=",result1)
        sparql_second = sparql2(result1)
        for i in sparql_second:
               sub_result = gstore.queryDB(db_name, i)
               Parse_Json(sub_result)

        data_to_use = initial_data1
    else:
        for i in initial_data['可能患的睡眠疾病']:
            # print("I = ", i)
            sparql = sparql_1(i)
            result = gstore.queryDB(db_name, sparql)
            # print('result=', result)
            result1 = Parse_Json_1(result)
            # print(result1)
            # sparql_second = sparql2(result1)
        data_to_use = initial_data

        # print('initial_data',initial_data)
    return HttpResponse(render(request, 'demo/tsest3.html', {'data1': data_to_use}))


def test1(request, **kwargs):
    # 每次请求时重置数据
    global data
    if 'disease_name' in request.POST:
        disease_name = request.POST.get('disease_name')
        disease_name1 = "睡眠障碍疾病病种/%s/#%s"%(disease_name,disease_name)
        data['名称'] = disease_name.split('/#')[-1]

        sparql = sparql3(disease_name1)
        result = gstore.queryDB(db_name, sparql)
        Parse_Json1(disease_name,result)

        sparql = sparql4(disease_name1)
        result = gstore.queryDB(db_name, sparql)
        Parse_Json1(disease_name,result)

        # sparql = sparql5(disease_name1)
        # result = gstore.queryDB(db_name, sparql)
        # Parse_Json1(disease_name,result)

    return HttpResponse(render(request, 'demo/test1.html', {'data2': data}))
