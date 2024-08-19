import re, time, os


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
                    f"{line} ==> 在位置{i+1}处不是X/Z,未下针的PIN存在输入或输出,请确认!"
                )
                return ""
    return pinSeqStr


if __name__ == "__main__":
    startTime = time.time()
    # 1.获取dec中各个管脚
    # dec无PD PC管脚组
    decPinStr = """D7 + D6 + D5 + D4 + D3+ D2 + D1 + D0 + RDB + WRB + A0 + IOCS0B + EXTINT0 + RESET + VPP + 
                PA0 + PA1 + PA2 + PA3 + PA4 + PA5 + PA6 + PA7 + PB0 + PB1 + PB2 + PB3 + PB4 + PB5 + PB6 + PB7 """
    decPinList = getDecPinList(decPinStr)
    # 2.获取pattern文件中各个管脚
    patternPinStr = (
        "VPP,RESET,EXTINT0,PD[7:0],PC[7:0],PB[7:0],PA[7:0],D[7:0],A0,IOCS0B,WRB,RDB"
    )
    re_pinGroup = re.compile(r"^(?P<pinName>\w+)\[(?P<maxNum>\d+):(?P<minNum>\d+)\]$")
    patternPinList = prasePin(patternPinStr, re_pinGroup, ",")
    # 2.1 确认pattern文件管脚是否存在重复
    setTmp = set(patternPinList)
    if len(setTmp) != len(patternPinList):
        print("pattern文件管脚存在重复,严重错误,请确认!!!")
        exit(-1)
    # 3. 判断pattern管脚是否在dec管脚中,若在记录该管脚和位置(用于获取pattern时将不需要的管脚字符跳过,保存需要的管脚字符)
    pinSeqdict = {}
    for pin in patternPinList:
        if pin in decPinList:
            pinSeqdict[pin] = patternPinList.index(pin)
    # for pin, index in pinSeqdict.items():
    #     print(f"{pin}=>{index}")
    # 4. 获取pattern中需要的管脚位置列表
    indexList = list(pinSeqdict.values())
    # 5. 检查pattern文件格式是否满足预设的正则规则,防止出现遗漏情况
    regexCompiledList = []
    patternPath = "mach3.pat"
    pinNum = 47
    re_checkFileComment = re.compile(r"^//.*$")
    re_checkPatternBody = re.compile(r"^[01HLZX]{%d}$" % pinNum)
    regexCompiledList.append(re_checkFileComment)
    regexCompiledList.append(re_checkPatternBody)
    # if not checkFilePattern("mach3.pat", regexCompiledList):
    #     print("pattern文件格式存在问题,请确认!!!")
    # 6. 遍历pattern文件,根据正则获取需要的pattern内容并写入新的pattern文件内
    re_checkFileCommentCap = re.compile(r"^(//.*)$")
    re_checkFilePlainCommentCap = re.compile(r"^//(.*)$")
    re_checkPatternBodyCap = re.compile(r"^([01HLZX]{47})$")
    # 6.1 获取comment行并通过comment行的内容得到需要创建的pattern文件数
    commentLineList = []
    with open(patternPath, "r") as fp:
        for line in fp:
            ll = getLineRegexCapture(line, re_checkFilePlainCommentCap)
            if ll:
                commentLineList.append(ll)

    for i in range(len(commentLineList)):
        # print(commentLineList[i])
        if len(commentLineList[i]) == 1:
            commentLineList[i] = commentLineList[i][0]
    print(len(commentLineList))
    print(commentLineList)

    # commentLineList = list(commentLineList)
    # patternNameList = []
    # for comment in commentLineList:
    #     if comment.endswith("END"):
    #         patternNameList.append(comment[:-3])
    # for ll in patternNameList:
    #     print(ll)
    # with open(patternPath, "r") as fp:
    #     with open("mach3_new.pat", "w") as fp2:
    #         pass
    #     for lineCnt, line in enumerate(fp, start=1):
    #         if not line:
    #             break
    #         if lineCnt < 3:
    #             continue
    #         matchBody = re_checkPatternBodyCap.search(line)
    #         matchComment = re_checkFileCommentCap.search(line)
    #         if matchBody:
    #             pinSeqStr = matchBody.group(1)
    #             pinSeqStr = getPinLineAtPosList(pinSeqStr, indexList)
    #             if pinSeqStr:
    #                 with open("mach3_new.pat", "a") as fp2:
    #                     fp2.write(pinSeqStr)
    #                     fp2.write("\n")
    #             else:
    #                 print("获取管脚字符出错, 请确认!!!")
    #                 break  # 遇到 pattern行, 直接跳出
    #         if matchComment:
    #             with open("mach3_new.pat", "a") as fp2:
    #                 fp2.write(matchComment.group(1))
    #             break  # 遇到注释行, 直接跳出
    endTime = time.time()
    print(f"时间总共花费: {round(endTime-startTime, 3)} S")
