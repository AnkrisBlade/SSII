import configparser
import hashlib
import os
import csv


# Returns list with all files inside that path
def filepaths(archivo_path):
    path = csv.reader(archivo_path, delimiter=',')
    paths = []
    for i in path:
        for subdir, _, files in os.walk(i):
            for file in files:
                paths.append(os.path.join(subdir, file))
        return paths

paths = filepaths(r"D:\Fork\SSII\Password_Generator")

dir = os.path.dirname(paths[0]).split("\\")[-1]

with open(dir+".csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in paths:
        wr.writerow(i + ", " + hashlib.sha512(i.encode('utf-8')).hexdigest())


