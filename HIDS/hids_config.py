import configparser
import hashlib
import os
import csv
import stat
from getpass import getpass


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
        csv_file.close()
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

        csv_file.close()


def get_config_file():
    defaults_paths = ["/etc/hids/config.ini", "./config.ini", "hids.ini", "./hids.ini", "./hids.conf"]

    for path in defaults_paths:
        # comprobamos que existe
        if os.path.isfile(path):
            return path


def configuration():
    config = configparser.ConfigParser()
    config_path = get_config_file()

    # leer la configuracion si la hubiera
    if config_path:
        config.read(config_path)
    else:
        return "No se encontró ningún archivo de configuracion"

    intervalo = 3600
    try:
        intervalo = int(config.get("General", "intervalo"))
    except Exception as e:
        print("No se obtuvo un intervalo de comprobacion valido, usando valor por defecto (" + str(intervalo) + "s)")
        print(e)

    log_path = "hids.log"
    try:
        log_path = config.get("General", "log")
    except Exception as e:
        print("No se obtuvo una ruta valida para el log, usando por defecto (" + log_path + ")")
        print(e)

    db_path = "ficheros_input.txt"
    try:
        db_path = config.get("General", "database")
    except Exception as e:
        print("No se obtuvo una ruta valida para la base de datos, usando por defecto (" + db_path + ")")
        print(e)

    db = filepaths(db_path)

    metodo_integridad = "sha1"
    try:
        metodo_integridad = config.get("General", "metodo_integridad")

    except:
        print("No se ha definido un metodo de comprobacion de integridad, usando sha1")

    # Leemos la contraseña
    try:
        with open(".shadow", "r") as pass_fd:
            contra_hash = pass_fd.read()

        # comprobamos los permisos
        perms = os.stat(".shadow").st_mode

        if perms & stat.S_IRWXO > 0 or perms & stat.S_IRWXG > 0 or perms & stat.S_IWUSR > 0:
            print("El shadow de la contraseña tiene permisos " + \
                  str(oct(perms))[-3:] + "! considere cambiarlos a 400")
            print("El shadow de la contraseña tiene permisos " + \
                  str(oct(perms))[-3:] + "! considere cambiarlos a 400")

        print("Introduzca la contraseña de administrador:")

        # comprobamos que la contraseña introducida es la correcta
        contra_raw = getpass()
        pass_hash = hashlib.sha512(contra_raw.encode()).hexdigest()

        if contra_hash != pass_hash:
            print("Contraseña erronea")

    except FileNotFoundError:

        # esto significa que no hay ninguna contraseña guardada
        print("No existe una contraseña almacena o no se puede acceder a ella")
        contra_raw = getpass("Por favor inserte una contraseña:")
        contra_hash = hashlib.sha512(contra_raw.encode()).hexdigest()

        try:
            with open(".shadow", "x") as pass_fd:
                pass_fd.write(contra_hash)

            os.chmod(".shadow", 0o400)
        except Exception as e:
            print(e)
            return "Fallo al crear la contraseña"

    try:
        genfile("hids.csv", db, contra_raw, metodo_integridad)
    except Exception as ex:
        print(ex)
        print("Error al crear el fichero con los archivos y hashes")

    return [intervalo, log_path, "hids.csv", metodo_integridad, contra_raw]
