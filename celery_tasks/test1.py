import json
import threading
import time
import binascii

"""
功能： Uart接收数据线程
属性： QueueUartReceiveData：Uart接收到数据后，将数据压入该队列
注解： 接收的数据为二进制，压入到队列中的数据为ASCII码
"""
def is_json(json_str):
    try:
        json.loads(json_str)
        return True
    except :
        return False
json_str='{"m5device_name":"meter", "m5device_type":"USB","m5device_remark":"智能电表","m5device_forward":[{"path_name":"path_mqtt","path_type":"MQTT","path_ip":"10.129.7.199","path_port":"1883","path_user":"iot","path_pwd":"iot123!","path_topic":"edgebox/m5/test","path_remark":"数据转发至MQTT"}]}'
print(is_json(json_str))