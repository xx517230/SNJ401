import re
import time


def getLineRegexCapture(line, regexPattern):
    match = re.search(regexPattern, line)
    if match:
        matchStrList = []
        captureNums = len(match.groups())
        if captureNums == 0:
            return
        for num in range(1, captureNums + 1):
            matchStr = match.group(num)
            matchStrList.append(matchStr)
        return matchStrList
    return


def prasePin(pinStr, regexPattern, splitChar=","):
    pinList = []
    pinListTmp = pinStr.split(splitChar)
    for pin in pinListTmp:
        match = re.search(regexPattern, pin)
        if match:
            pinName = match.group("pinName")
            pinMaxNum = int(match.group("maxNum"))
            pinMinNum = int(match.group("minNum"))
            if pinMaxNum < pinMinNum:
                pinMaxNum, pinMinNum = pinMinNum, pinMaxNum
            for i in range(pinMaxNum, pinMinNum - 1, -1):
                pinList.append(f"{pinName}{i}")
        else:
            pinList.append(pin)  # 如果没有匹配，直接添加原始 pin
    return pinList


# pattern文件格式校验,用于确认整个pattern内容都是匹配的，防止遗漏内容
def checkFilePattern(filePath, regexPatternList):
    # 1. 读取文件内容
    with open(filePath, "r") as fp:
        lineList = fp.readlines()
    # 2. 使用正则规则遍历每行
    for lineCnt, line in enumerate(lineList, start=1):
        matchFlag = False
        # 2.1 匹配每一行是否符合正则规则
        for regexPattern in regexPatternList:
            if re.search(regexPattern, line):
                matchFlag = True
                break  # 跳出 for regexPattern in regexPatternList
        # 2.2 如果不匹配，返回 False
        if not matchFlag:
            print(
                f"{lineCnt} 行, 不满足正则匹配{regexPatternList}，存在遗漏或错误，请确认！！！"
            )
            return False
    # 3. 如果所有行都匹配，返回 True
    return True


def getDecPinList(decPinStr, spe="+"):
    if not decPinStr:
        return []
    pinList = []
    for pin in decPinStr.split(spe):
        pinList.append(pin.strip())
    return pinList


def getPinLineAtPosList(line, posList):
    if not line:
        return ""
    pinSeqStr = ""
    for i in range(len(line)):
        if i in posList:
            pinSeqStr += line[i]
        else:
            if line[i].upper() != "X" and line[i].upper() != "Z":
                print(
                    f"{line} ==> 在位置{i}处不是X/Z,未下针的PIN存在输入或输出,请确认!"
                )
                return ""
    return pinSeqStr


if __name__ == "__main__":
    startTime = time.time()
    # dec无PD PC
    # dec无PD PC
    decPinStr = """D7 + D6 + D5 + D4 + D3+ D2 + D1 + D0 + RDB + WRB + A0 + IOCS0B + EXTINT0 + RESET + VPP + 
                PA0 + PA1 + PA2 + PA3 + PA4 + PA5 + PA6 + PA7 + PB0 + PB1 + PB2 + PB3 + PB4 + PB5 + PB6 + PB7 """
    decPinList = getDecPinList(decPinStr)

    patternPinStr = (
        "VPP,RESET,EXTINT0,PD[7:0],PC[7:0],PB[7:0],PA[7:0],D[7:0],A0,IOCS0B,WRB,RDB"
    )
    re_pinGroup = re.compile(r"^(?P<pinName>\w+)\[(?P<maxNum>\d+):(?P<minNum>\d+)\]$")
    patternPinList = prasePin(patternPinStr, re_pinGroup, ",")
    setTmp = set(patternPinList)
    if len(setTmp) != len(patternPinList):
        print("pattern文件管脚存在重复,严重错误,请确认!!!")
        exit(-1)
    pinSeqdict = {}
    for pin in patternPinList:
        if pin in decPinList:
            pinSeqdict[pin] = patternPinList.index(pin)
    for pin, index in pinSeqdict.items():
        print(f"{pin}=>{index}")
    # indexList = list(list(pinSeqdict.values()))
    indexList = list(pinSeqdict.values())
    print(indexList)
    print(len(indexList))

    strTmp = getPinLineAtPosList(lineStr, indexList)

    # regexCompiledList = []
    # patternPath = "mach3.pat"
    # pinNum = 47
    # re_checkFileComment = re.compile(r"^//.*$")
    # re_checkPatternBody = re.compile(r"^[01HLZX]{%d}$" % pinNum)
    # re_checkFileCommentCap = re.compile(r"^//(.*)$")
    # re_getPin = re.compile(r"^(//VPP,RESET,EXTINT0.*)$")
    # regexCompiledList.append(re_checkFileComment)
    # regexCompiledList.append(re_checkPatternBody)
    # checkFilePattern("mach3.pat", regexCompiledList)

    # commemtLineList = []
    # with open(patternPath, "r") as fp:
    #     for line in fp:
    #         ll = PatternParse.getLineRegexCapture(line, re_checkFileCommentCap)
    #         if ll:
    #             commemtLineList.append(ll)
    # print("=============")
    # for ll in commemtLineList:
    #     print(ll)
    # print(len(commemtLineList))
    endTime = time.time()
    print(f"时间总共花费: {round(endTime-startTime, 3)} S")
