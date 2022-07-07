# -*- coding: utf-8 -*-
import requests
import base64
import re
import json
def vmess_un_base64(vmess_str,host=None):
    ba64_code = re.findall('vmess://(.*)',vmess_str)[0]
    #vmess:// 后的base64解密
    vmess_body = str(base64.b64decode(ba64_code), 'utf-8')
    json_proxy = json.loads(vmess_body)


    #判断是否传入host参数，如果有则返回修改host后的vmess
    if host:
        json_proxy['host'] = host
        base64_vmess = 'vmess://' + re.findall("b'(.*)'",str(base64.b64encode(str(json_proxy).encode('utf-8'))))[0]
        return base64_vmess
    #如果host参数为空则返回vmess解密后的内容
    else:
        return vmess_body


def v2ray_dy(url,host=None):
    v = []
    url_text = requests.get(url).text
    #第一次base64解密
    vmess_proxy = str(base64.b64decode(url_text), 'utf-8')
    for a_vmess in re.findall('vmess://(.*)', vmess_proxy):
        # 去除vmess://再次解密
        vmess_body = str(base64.b64decode(a_vmess), 'utf-8')
        json_proxy = json.loads(vmess_body)
        # 设置
        # 修改host内容
        json_proxy['host'] = host
        base_str_list = re.findall("b'(.*)'",str(base64.b64encode(str(json.dumps(json_proxy)).encode('utf-8'))))
        for i in base_str_list:
            vmess_i = 'vmess://' + i
            v.append(vmess_i)
    return v
