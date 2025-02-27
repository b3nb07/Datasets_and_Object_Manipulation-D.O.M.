import os
os.chdir("output")
arr = os.listdir()

os.chdir("..")
arr = os.listdir()

print(arr)