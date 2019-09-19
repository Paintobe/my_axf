from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from market.models import FoodType, Goods


def index(request,typeid,twoid,sortid):
    #取出分类信息
    foodtype = FoodType.objects.order_by('typesort')

    if typeid == '0':
        #默认取出热销榜的数据
        #取出热销榜的分类ID
        cid = foodtype[0].typeid
        #获取热销榜的子分类名称
        childcate = foodtype[0].childtypenames
    else:
        cid = typeid
        #获取对应的大分类的子分类名称
        childdate = FoodType.objects.get(typeid = cid)
        childcate = childdate.childtypenames
    # print(childcate)
    #找出typeid对应的goods
    goods = Goods.objects.filter(categoryid = cid)

    if twoid != '0':
        goods = goods.filter(childcid = twoid)


    #全部分类: 0  # 进口水果:103534#国产水果:103533
    #将子分类名称转换为字典格式 {'0':'全部分类','103534':'进口水果','103533':'国产水果'}
    childcateDict = {}
    childcateList = childcate.split('#')
    for one in childcateList:
        childcateList2 = one.split(':')
        childcateDict[childcateList2[1]] = childcateList2[0]
    # print(childcateDict)

    twoName = childcateDict[twoid]

    #根据价格和销量排序
    order_data = [
        ['综合排序','0'],
        ['价格升序','1','price'],
        ['价格降序','2','-price'],
        ['销量升序','3','productnum'],
        ['销量降序','4','-productnum'],
    ]

    if sortid!='0':
        goods = goods.order_by(order_data[int(sortid)][2])

    sortName = order_data[int(sortid)][0]


    context = {
        'foodtype' : foodtype,
        'goods' : goods,
        'cid' : int(cid),
        'childcateDict' : childcateDict,
        'twoid' : twoid,
        'twoName' : twoName,
        'order_data' : order_data,
        'sortid' : sortid,
        'sortName' : sortName
    }

    return render(request,'market.html',context)