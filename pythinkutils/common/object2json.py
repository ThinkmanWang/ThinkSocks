# -*- coding: utf-8 -*-


'''
object2json.py Convent OBJECT to JSON
将对象结构转化成一个json字符串，使用递归思路，自定义dump解析器，项目地址；https://github.com/hustcc/object2json
python json库，对于对象嵌套的类型的数据转JSON无能为力

--
PS：实际上，采用lambda即可完成，我开眼了
json.dumps(obj, default = lambda o: o.__dict__)
--

@author: hzwangzhiwei
@contact: http://50vip.com/

Created on 2014年11月19日
'''
import json


'''
嵌套对象转json字符串
'''
def obj2json(obj):
    return json.dumps(obj, cls = ObjJsonEncoder)

'''
递归 py对象转dict
'''
def object2dict(obj):
    # 基本数据类型，直接返回
    if not hasattr(obj,'__dict__'):
        return obj
    rst = {}
    for k,v in obj.__dict__.items():
        if k.startswith('-'):
            continue
        if isinstance(v,list):
            ele = [object2dict(item) for item in v]
        else:
            ele = object2dict(v)
        rst[k] = ele
    return rst


'''
重现实现自定义的json encoder
'''
class ObjJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import date, datetime

        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return object2dict(obj)
