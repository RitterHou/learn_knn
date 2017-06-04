from os import *

files = listdir('./')
print(files)

for file in files:
    rename(file, file.replace('3', '8'))
