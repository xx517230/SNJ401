if "":
    print("None")
else:
    print("not None")


# ll = [1, 2, 3, None, None]
# print(ll)
# VPP,RESET,EXTINT0,PD[7:0],PC[7:0],PB[7:0],PA[7:0],D[7:0],A0,IOCS0B,WRB,RDB

# # dec无PD PC
# decPinStr = """D7 + D6 + D5 + D4 + D3+ D2 + D1 + D0 + RDB + WRB + A0 + IOCS0B + EXTINT0 + RESET + VPP +
#                PA0 + PA1 + PA2 + PA3 + PA4 + PA5 + PA6 + PA7 + PB0 + PB1 + PB2 + PB3 + PB4 + PB5 + PB6 + PB7 """

# for pin in decPinStr.split("+"):
#     pin = pin.strip()
#     print(pin)
# print(pin)


# for i in range(10):
#     pass
# print(i)

# with open("mach3.pat", "r") as fp:
#     a = fp.readline()
# print(a)


# fp = open("mach3.pat", "r")
# a = fp.readline()
# print(a)
