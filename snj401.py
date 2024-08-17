import os, re

re_fileFirstLine = re.compile(r"^//PA[0] input 8M clock")
re_filePinLine = re.compile(r"^//(VPP,RESET,EXTINT0,PD[7:0].*)$")

re_parsePinGroup = re.compile(
    r"(?P<pinName>\w+)[(?P<maxNum>\d+):(?P<minNum>\d+)]"
)  # 管脚组解析


def prasePin(file, pinStr, parseRegex):
    pinList = []
    pinListTmp = pinStr.split(",")
    for pin in pinList:

        if re.search(parseRegex, pin):
            pinName = re.search(parseRegex, pin).group("pinName")
            pinMaxNum = re.search(parseRegex, pin).group("maxNum")
            pinMinNum = re.search(parseRegex, pin).group("minNum")
            if pinMaxNum < pinMinNum:
                tmp = pinMaxNum
                pinMaxNum = pinMinNum
                pinMinNum = tmp
            for i in range(int(pinMinNum), int(pinMaxNum) + 1):

                pinList.append(f"{pinName}{i}")
        else:
            pinList.append(pin)
