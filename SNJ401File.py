import re


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
