import urllib, urllib3, sys, uuid
import ssl


host = 'https://sdvin.market.alicloudapi.com'
path = '/vin/query'
method = 'GET'
appcode = '0b7ad96ceb334f36b6b8b157f8204ffe'
querys = 'vin=LFV3B2FY6S3440766'
bodys = {}
url = host + path + '?' + querys

http = urllib3.PoolManager()
headers = {
    'Authorization': 'APPCODE ' + appcode
}
response = http.request('GET', url, headers=headers)
content = response.data.decode('utf-8')
if (content):
    print(content)


# matching_mode	int	匹配模式 1 标准车型
# is_commercial	int	是否商用 1 是 0 否
# cid	string	车ID，车辆车型大全接口 可查看该车所有配置信息
# brand_name	string	品牌名称
# series_name	string	车系
# name	string	车型车款
# year	string	年款
# price	string	厂家指导价
# gearbox	string	变速箱
# geartype	string	变速箱类型
# engine_model	string	发动机型号
# driven_type	string	驱动方式
# displacement_ml	string	排量(mL)
# displacement	string	排量(L)
# nedczhyh	string	油耗
# effluent_standard	string	环保标准
# scale	string	车辆级别
# csjg	string	车身结构
# cms	string	车门数(个)
# zws	string	座位数(个)
# market_date	string	上市时间
# stop_date	string	停产日期
# length	string	长度(mm)
# width	string	宽度(mm)
# high	string	高度(mm)
# wheelbase	string	轴距(mm)
# trackfront	string	前轮距(mm)
# trackrear	string	后轮距(mm)
# full_weight	string	整备质量(kg)
# front_tyre_size	string	前轮胎规格
# rear_tyre_size	string	后轮胎规格
# rlxs	string	燃料形式
# ryxh	string	燃油标号
# gearbox_number	string	变速箱号
# chassis_number	string	底盘号
# model_list	object	可能的销售车型列表
# full_weight_max	string	最大满载质量(kg)
# full_weight_zz	string	核载质量
# img	string	车型图片
# manufacturer	string	厂商
# zdgl	string	最大功率
# front_brake_type	string	前制动器类型
# rear_brake_type	string	后制动器类型
# parking_brake_type	string	驻车制动类型
# qfs	string	气缸数
# gyfs	string	供油方式
# is_import	string	是否进口 0国产 1进口
# is_rules	string	vin是否合规 1是 0否
# market_price	string	市场参考价
# gearnum	string	变速箱档位数
# body_type	string	车体结构
# zdml	string	最大马力
# version	string	销售版本