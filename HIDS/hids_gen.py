import configparser
import hashlib
import os
import csv
import sys
import getpass
import configparser


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

def get_config_file():
    defaults_paths = ["/etc/hids/config.ini","./config.ini","./hids.ini","./hids.conf"]
    
    for path in defaults_paths:
        #comprobamos que existe
        if os.path.isfile(path):
            return path
        
    return None

def print_usage():
    print("HIDS Generador Database")
    print("Uso: " + sys.argv[0] + " input output")

if len(sys.argv) < 3:
    print_usage()
    exit(-1)

"""metodo_integridad = sys.argv[1]
hash_func = hashlib.sha1

if metodo_integridad == "sha1":
    hash_func = hashlib.sha1
elif metodo_integridad == "sha256":
    hash_func = hashlib.sha256
elif metodo_integridad == "sha512":
    hash_func = hashlib.sha512
elif metodo_integridad == "md5":
    hash_func = hashlib.md5"""

config = configparser.ConfigParser()
config_path = get_config_file()
if config_path == None:
    print("No se encontró ningún archivo de configuracion")
else:
    config.read(config_path)
try:    
    metodo_integridad = config.get("General","metodo_integridad")
    if metodo_integridad == "sha1":
        hash_func = hashlib.sha1
    elif metodo_integridad == "sha256":
        hash_func = hashlib.sha256
    elif metodo_integridad == "sha512":
        hash_func = hashlib.sha512
    elif metodo_integridad == "md5":
        hash_func = hashlib.md5
        
except Exception as e:
    print("No se ha definido un metodo de comprobacion de integridad, usando sha1")

fichero_input = sys.argv[1]
fichero_output = sys.argv[2]

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


# Almacenamos las rutas de los archivos dentro de los directorios especificados en un fichero "archivo_path"

"""
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

def genfile(name, paths, password):
    with open(name, 'w', newline='') as csv_file:
        hasheo = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in paths:
            file_hash = hashlib.sha1(open(i).read().encode()).hexdigest()
            hasheo.writerow([i, " " + hashlib.sha1((file_hash + password).encode()).hexdigest()])

paths = filepaths(r"D:\Fork\SSII\HIDS\Password_Generator.csv")
genfile("hids_test.csv", paths, "test")

"""



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

    return "Hasheo de archivos finalizado"

genfile("hids_test.csv", paths, "test")
