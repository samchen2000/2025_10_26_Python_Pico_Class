chinese = int(input("國文分數"))
print(type(chinese))
english = int(input("英文分數"))
print(type(english))
math = int(input("數學分數"))
print(type(math))

total = chinese + english + math
print("總分 : ", total, "分", sep = "__")
average = round(total / 3, ndigits=2)
print("平均 : ", average, "分", sep="---")

