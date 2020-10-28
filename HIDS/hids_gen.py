import configparser
import hashlib
import os
import csv


# Returns list with all files inside that path
def filepaths(archivo_path):
    with open(archivo_path) as csv_file:
        path = csv.reader(csv_file)
        paths = []
        for i in path:
            for subdir, _, files in os.walk(i[0]):
                for file in files:
                    paths.append(os.path.join(subdir, file))
        return paths

paths = filepaths(r"D:\Fork\SSII\HIDS\Password_Generator.csv")

def genfile(name, paths, password):
    with open(name, 'w', newline='') as csv_file:
        hasheo = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in paths:
            file_hash = hashlib.sha1(open(i).read().encode()).hexdigest()
            hasheo.writerow([i, " " + hashlib.sha1((file_hash + password).encode()).hexdigest()])

    return "Hasheo de archivos finalizado"

genfile("hids_test.csv", paths, "test")
