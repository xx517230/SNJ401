import os, re
import SNJ401File


def fileReadByLines(filePath):
    try:
        with open(filePath, "r") as fp:
            lineList = []
            for line in fp:  # 逐行读取文件
                lineList.append(line.strip())  # 去掉换行符
        return lineList
    except FileNotFoundError:
        print(f"错误: 文件 '{filePath}' 未找到。")
        return []  # 返回空列表而不是 None
    except PermissionError:
        print(f"错误: 没有权限读取文件 '{filePath}'。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []


if __name__ == "__main__":
    patternPath = "mach3.pat"

    regexCompiledList = []
    re_checkFileComment = re.compile(r"^//.*$")
    re_checkPatternBody = re.compile(r"^[01HLZX]{%d}$" % pinNum)
    regexCompiledList.append(re_checkFileComment)
    regexCompiledList.append(re_checkPatternBody)

    SNJ401File.checkFilePattern(patternPath)
    lineList = fileReadByLines(patternPath)
    pinNum = 47

    flag = snj401File.checkFilePattern("mach3.pat", regexCompiledList)
    print(flag)
    # checkFilePattern("mach3.pat")
    pass
