import csv
import hashlib
import time
import logging
import datetime
from hids_config import configuration

'''
param: ruta a archivo cvs con las columnas ruta,hash
return: lista de tuplas (ruta,hash)
'''


def read_database(path):
    with open(path, 'r') as csv_file:
        hashes = [(ruta, hash) for ruta, hash in csv.reader(csv_file)]
    return hashes


def gen_informe(n_analisis, ataque, log):
    with open("informe_"
              + str(datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")) + ".txt", "w", encoding="UTF-8") as f:
        f.write("INFORME DIARIO " + str(datetime.datetime.now().today()) + "\n")
        f.write("NUMERO DE ANÁLISIS: " + str(n_analisis) + "\n")
        f.write("VICTIMA DE ATAQUE: " + str(ataque) + "\n")
        f.write("\n")
        with open(log, 'r') as l:
            for linea in l:
                f.write(linea)
            l.close()
        f.close()


def main():
    # Get Configuration [intervalo, log_path, db_path, hash_func, contra_raw]
    try:
        config = configuration()
    except Exception as ex:
        print(ex)
        exit(-1)

    # cargar base de datos
    hashes = read_database(config[2])

    # Cargar hash_func
    if config[3] == "sha1":
        hash_func = hashlib.sha1
    elif config[3] == "sha256":
        hash_func = hashlib.sha256
    elif config[3] == "sha512":
        hash_func = hashlib.sha512
    elif config[3] == "md5":
        hash_func = hashlib.md5

    # Cargar contraseña
    contra_raw = config[4]

    if len(hashes) == 0:
        return "Base de datos vacia"

    # inicializar log [levelname = Debug, info...], [asctime = time], [message = mensaje]
    log_format = "[%(levelname)s] %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.DEBUG, filename=config[1], format=log_format)

    # Variables para el informe
    analisis = 0
    hora_inicio = time.strftime("%H:%m")

    # Bucle principal, ejecutar cada "intervalo" tiempo
    while True:
        print("Comprobando Integridad")

        ataque = False
        ficheros_corruptos = 0
        ficheros_no_encontrados = 0
        ficheros_total = len(hashes)

        for ruta, hash in hashes:

            try:
                file_hash = hash_func(open(ruta, "rb").read()).hexdigest()
            except FileNotFoundError as e:
                msg = "===# FICHERO NO ENCONTRADO! #===\n" \
                      "Ruta: " + ruta
                print(msg)
                logging.error(
                    "Fallo en:(" + ruta + ") El fichero no se encuntra.  Fecha:(" + str(datetime.datetime.now()) + ")")
                ficheros_no_encontrados = ficheros_no_encontrados + 1
                continue

            # fichero leido
            new_hash = hash_func((file_hash + contra_raw).encode()).hexdigest()
            if new_hash != hash:
                msg = "===# FICHERO CORRUPTO! #===\n" + \
                      "Ruta: " + ruta + "\n" \
                                        "Hash original:\t" + hash + "\n" \
                                                                    "Hash actual:\t" + new_hash
                print(msg)
                # _ = messagebox.showerror("ARCHIVO CORRUPTO!", msg)
                logging.error(
                    "Fallo en:(" + ruta + ") Hash original:(" + hash + ") Actual:(" + new_hash + ") Fecha:(" + str(
                        datetime.datetime.now()) + ")")
                ficheros_corruptos = ficheros_corruptos + 1

        logging.info("Integridad comprobada")

        # Estadisticas
        porcentaje_corruptos = float(ficheros_corruptos / ficheros_total) * 100
        porcentaje_no_encontrados = float(ficheros_no_encontrados / ficheros_total) * 100

        if porcentaje_corruptos > 10 or porcentaje_no_encontrados > 10:
            ataque = True

        logging.info("Estadisticas: corruptos: " + str(porcentaje_corruptos) \
                     + "% no encontrados: " + str(porcentaje_no_encontrados) + "%")

        print("FICHEROS: " + str(ficheros_total))
        print("CORRUPTOS: " + str(ficheros_corruptos) + " " + str(porcentaje_corruptos) + "%")
        print("NO ENCONTRADOS: " + str(ficheros_no_encontrados) + " " + str(porcentaje_no_encontrados) + "%")
        print("VICTIMA DE ATAQUE:" + str(ataque))
        print(" -- ")

        analisis += 1

        # Si la hora es igual a la de inicio, genera informe (24h)
        if (time.strftime("%H:%M")) == hora_inicio:
            gen_informe(analisis, ataque, config[1])
            # Reiniciamos las variables utilizadas para las estadisticas del informe
            analisis = 0
            # Generamos un nuevo log
            open(config[1], "w").close()

        time.sleep(config[0])


main()
