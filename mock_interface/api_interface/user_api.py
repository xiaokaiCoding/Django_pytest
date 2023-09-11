from django.http import HttpResponse,JsonResponse
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from api_interface.models import UserApi
from typing import Dict
import json
from loguru import logger


def dispatcher(request):
    if request.method == "GET":
        request.params = request.GET
    else:
        request.params = json.loads(request.body)     
    action = request.params["action"]    
    logger.info(f"request.params: {request.params}")
    if action == "add_user":
        return add_user(request)
    if action == "update_user":
        return update_user(request)        
    elif action == "list_users":
        return list_users(request)            
    elif action == "delete_user":
        return delete_user(request)
    else:
        return responce_dealer(-1, {"data": "请检查参数！"})    


def responce_dealer(code: int, msg="ok", content={"data": {}}): 
    result = {"code": code, "msg": msg}
    result.update(content)
    logger.info(f"res:{result}")
    return JsonResponse(result)

'''
添加用户，如已经存在重名用户，则提示添加失败
'''
def add_user(request):    
    name = request.params["name"]
    pwd = request.params["pwd"]
    qs = list(UserApi.objects.filter(name=name))
    if len(qs) >= 1:
        return responce_dealer(-1, "已存在此用户！无法重复创建")
    else:    
        user_1 = UserApi(name=name, pwd=pwd)
        user_1.save()
        return responce_dealer(0) 

'''
查询用户，支持全量/name/pagesize查询,name为模糊查询
'''
def list_users(request):
    try:
        name = request.params["name"]
    except KeyError:
        name = ""  
    try:
        pagesize = request.params["pagesize"]
    except KeyError:
        pagesize = 10
    try:
        pagenum = request.params["pagenum"]
    except KeyError:
        pagenum = 1              
    if name == "":
        qs = UserApi.objects.values()
    else:
        qs = UserApi.objects.filter(name__contains=name).values()
        # qs = UserApi.objects.filter(name=name).values()
    logger.info(qs)    
    # 使用分页对象，设定每页多少条记录
    try:
        pgnt = Paginator(qs, pagesize)
        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum) 
    except Exception:
        return responce_dealer(-1, "查询用户失败，请检查分页参数",{"data": {}})        
    lists = list(page)
    logger.info("查询全部用户成功！")
    return responce_dealer(0, "查询全部用户成功",{"total": len(qs), "data": lists})    


# def list_user(request):
#     qs = UserApi.objects.filter(name=request.params["name"])
#     logger.info(f"type lists:{type(qs)}")    
#     logger.info("查询单条用户成功！")
#     return responce_dealer(0, "查询成功",{"data": {"name": qs.name, "pwd": qs.pwd}}) 

'''
删除用户，支持按名字 name批量删除
'''
def delete_user(request):    
    names = request.params["names"]
    for name in names:
        try:
            user_1 = UserApi.objects.get(name=name)
            user_1.delete()
            logger.info(f"删除{name}用户成功！")
        except UserApi.DoesNotExist:
            logger.info(f"未找到{name}用户")     
    return responce_dealer(0)    

def update_user(request):  
    name = request.params["name"]
    pwd = request.params["pwd"]     
    try:
        qs = UserApi.objects.get(name=name)
        qs.pwd = pwd
        qs.save()
    except UserApi.DoesNotExist:
        code = -1
        msg = "未找到对应用户！"
        return responce_dealer(code, msg)       
    logger.info("修改单条用户成功！")
    return responce_dealer(0)     