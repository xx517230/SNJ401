import re


def getLineRegexCapture(line, regexPattern):
    match = re.search(regexPattern, line)
    if match:
        matchStrList = []
        captureNums = len(match.groups())
        if captureNums == 0:
            return None
        for num in range(1, captureNums + 1):
            matchStr = match.group(num)  # 使用更好的变量名
            matchStrList.append(matchStr)
        return matchStrList
    return None


def prasePin(pinStr, regexPattern, splitChar=","):
    pinList = []
    pinListTmp = pinStr.split(splitChar)

    for pin in pinListTmp:
        match = re.search(regexPattern, pin)
        if match:
            pinName = match.group("pinName")
            pinMaxNum = int(match.group("maxNum"))  # 确保转换为整数
            pinMinNum = int(match.group("minNum"))  # 确保转换为整数
            if pinMaxNum < pinMinNum:
                pinMaxNum, pinMinNum = pinMinNum, pinMaxNum
            for i in range(pinMaxNum, pinMinNum - 1, -1):  # 从最大值到最小值
                pinList.append(f"{pinName}{i}")
        else:
            pinList.append(pin)  # 如果没有匹配，直接添加原始 pin

    return pinList
