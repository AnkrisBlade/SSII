import configparser
import hashlib
import os
import csv
import sys
import getpass


# Returns list with all files inside that path
'''def filepaths(archivo_path):
    path = csv.reader(archivo_path, delimiter=',')
    paths = []
    for i in path:
        for subdir, _, files in os.walk(i):
            for file in files:
                paths.append(os.path.join(subdir, file))
        return paths

#paths = filepaths(r"D:\Fork\SSII\Password_Generator")

#dir = os.path.dirname(paths[0]).split("\\")[-1]'''

def print_usage():
    print("HIDS Generador Database")
    print("Uso: " + sys.argv[0] + " hash_tipo input output")

if len(sys.argv) < 4:
    print_usage()
    exit(-1)

metodo_integridad = sys.argv[1]
hash_func = hashlib.sha1

if metodo_integridad == "sha1":
    hash_func = hashlib.sha1
elif metodo_integridad == "sha256":
    hash_func = hashlib.sha256
elif metodo_integridad == "sha512":
    hash_func = hashlib.sha512
elif metodo_integridad == "md5":
    hash_func = hashlib.md5

fichero_input = sys.argv[2]
fichero_output = sys.argv[3]

ficheros_procesar = []

#leemos los datos del archivo de origen, sin hashes y con carpetas
with open(fichero_input,"r") as input_fd:
    for ruta in input_fd:
        
        def add_ruta(path):
            try:
                if os.path.isfile(path) is True:
                    ficheros_procesar.append(path)
                elif os.path.isdir(path) is True:
                    for item in os.listdir(path):
                        if path[-1] == '/':
                            add_ruta(path + item)
                        else:
                            add_ruta(path + "/" + item)
                            
            except Exception as e:
                print(e)
        
        add_ruta(ruta.replace("\n",""))

print("Introduzca la contraseña de administador para generar los hashes")
pass_raw = getpass.getpass()
print("Introduzca la contraseña de nuevo para verificar")
if pass_raw != getpass.getpass():
    print("Las contraseñas no coinciden")
    exit(-1)


with open(fichero_output,"w") as output_fd:
    for item in ficheros_procesar:
        try:
            fichero_hash = hash_func(open(item,"rb").read()).hexdigest()
            output_fd.write(item + "," + hash_func(fichero_hash.encode() + pass_raw.encode()).hexdigest() + "\n")
        except:
            None
            
'''with open(dir+".csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in paths:
        wr.writerow(i + ", " + hashlib.sha512(i.encode('utf-8')).hexdigest())'''


