import configparser
import hashlib
import os
import csv
import sys
import getpass
import configparser


# Almacenamos las rutas de los archivos dentro de los directorios especificados en un fichero "archivo_path"
def filepaths(archivo_path):
    with open(archivo_path) as csv_file:
        path = csv.reader(csv_file)
        paths = []
        for i in path:
            try:
                for subdir, _, files in os.walk(i[0]):
                    for file in files:
                        paths.append(os.path.join(subdir, file))

            except Exception as ex:
                print(ex)
        return paths


def genfile(name, paths, password, metodo_integridad):
    with open(name, 'w', newline='') as csv_file:
        hasheo = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in paths:
            # Cargar hash_func
            if metodo_integridad == "sha1":
                hash_func = hashlib.sha1
            elif metodo_integridad == "sha256":
                hash_func = hashlib.sha256
            elif metodo_integridad == "sha512":
                hash_func = hashlib.sha512
            elif metodo_integridad == "md5":
                hash_func = hashlib.md5
            file_hash = hash_func(open(i, "rb").read()).hexdigest()
            hasheo.writerow([i, hash_func((file_hash + password).encode()).hexdigest()])


def copy_csv(filename):
    import pandas as pd
    df = pd.read_csv(filename)
    df.to_csv('copy_of_' + filename)
