import re

# demoStr = "abc123---"

# print(len(re.search("\w", demoStr).groups()))

pinMaxNum = 10
pinMinNum = 30

# 交换最大和最小值
if pinMaxNum < pinMinNum:
    pinMaxNum, pinMinNum = pinMinNum, pinMaxNum
print(pinMaxNum, pinMinNum)
