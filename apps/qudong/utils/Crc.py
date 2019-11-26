#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 19:09
# @Author  : userzhang

def calculate_CRC(dataarray):
    data=""
    for i in range(0,len(dataarray),2):
        data+=dataarray[i]+dataarray[i+1]+" "
    datalist = data.strip().split()  # 以空格分割字符串得到对应字符串列表
    index = 0
    try:
        for index, item in enumerate(datalist):
            # if '0x' in item.lower().strip():
            #     datalist[index] = int(item, 16)
            # elif '0o' in item.lower().strip():
            #     datalist[index] = int(item, 8)
            # elif '0b' in item.lower().strip():
            #     datalist[index] = int(item, 2)
            # else:
            #     datalist[index] = int(item)
            datalist[index]=int(item,16)
        # 处理第1个字节数据
        temp = calculateonebyte(datalist.pop(0), 0xFFFF)
        # 循环处理其它字节数据
        for data in datalist:
            temp = calculateonebyte(data, temp)
        CRC = temp
        crc = (temp >> 8) ^ (CRC << 8)
        return dataarray+"%04X"%(crc & 0x00FFFF)
    except ValueError as err:
        print(u'第{0}个数据{1}输入有误'.format(index, datalist[index]).encode('utf-8'))
        print(err)
def calculateonebyte(databyte, tempcrc):
    # databyte必须为字节数据
    # assert 0x00 <= databyte <= 0xFF
    # 同上字节数据检查
    if not 0x00 <= databyte <= 0xFF:
        raise Exception((u'数据：0x{0:<02X}不是字节数据[0x00-0xFF]'.format(databyte)).encode('utf-8'))

        # 把字节数据根CRC当前值的低8位相异或
    low_byte = (databyte ^ tempcrc) & 0x00FF
    # 当前CRC的高8位值不变
    resultCRC = (tempcrc & 0xFF00) | low_byte

    # 循环计算8位数据
    for index in range(8):
        # 若最低为1：CRC当前值跟生成多项式异或;为0继续
        if resultCRC & 0x0001 == 1:
            # print("[%d]: 0x%4X ^^^^ 0x%4X" % (index,resultCRC>>1,resultCRC^GENERATOR_POLYNOMIAL))
            resultCRC >>= 1
            resultCRC ^= 0xA001  # 0xA001是0x8005循环右移16位的值
        else:
            # print ("[{0}]: 0x{1:X} >>>> 0x{2:X}".format(index,resultCRC,resultCRC>>1))
            resultCRC >>= 1
    return resultCRC
# crc=calculate_CRC('0103000100021111')
# print(crc)
