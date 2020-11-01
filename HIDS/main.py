import csv
import hashlib
import time
import os
import logging
import configparser
import stat
import sys
from getpass import getpass
from tkinter import messagebox
import datetime
from importlib import reload


'''
param: ruta a archivo cvs con las columnas ruta,hash
return: lista de tuplas (ruta,hash)
'''
def read_database(path):
    hashes = []
    with open(path,'r') as csv_file:
        hashes = [(ruta,hash) for ruta,hash in csv.reader(csv_file)]
    return hashes

def get_config_file():
    defaults_paths = ["/etc/hids/config.ini","./config.ini","./hids.ini","./hids.conf"]
    
    for path in defaults_paths:
        #comprobamos que existe
        if os.path.isfile(path):
            return path
        
    return None

def gen_informe(n_analisis, n_ataques,log):
    with open("informe_"+str(datetime.datetime.now())+".txt", "w") as f:
        f.write("INFORME DIARIO "+str(datetime.datetime.now().today())+"\n")
        f.write("NUMERO DE ANÁLISIS: " + str(n_analisis)+"\n")
        f.write("NUMERO DE ATAQUES RECIBIDOS: " + str(n_ataques)+"\n")
        f.write("\n")
        with open(log,'r') as l:
            for linea in l:
                    f.write(linea)
            f.close()
        f.close()

def main():
    intervalo = 3600
    log_path = "hids.log"
    db_path = "hids.csv"
    hash_func = hashlib.sha1

    #leer la configuracion si la hubiera
    config = configparser.ConfigParser()
    config_path = get_config_file()
    if config_path == None:
        print("No se encontró ningún archivo de configuracion")
    else:
        config.read(config_path)
    
    try:
        intervalo = int(config.get("General","intervalo"))
    except Exception as e:
        print("No se obtuvo un intervalo de comprobacion valido, usando valor por defecto ("+intervalo+"s)")
        print(e)
        
    try:
        log_path = config.get("General","log")
    except Exception as e:
        print("No se obtuvo una ruta valida para el log, usando por defecto (" + log_path + ")")
        print(e)
        
    try:    
        db_path = config.get("General","database")
    except Exception as e:
        print("No se obtuvo una ruta valida para la base de datos, usando por defecto (" + db_path + ")")
        print(e)
        
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
    
    #inicializar log
    log_format = "[%(levelname)s] %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.DEBUG,filename=log_path,format = log_format)
    
    
    #cargar base de datos
    hashes = read_database(db_path)
    
    if len(hashes) == 0 :
        print("Base de datos vacia!!")
        exit(0)
        
   
    #leemos la contraseña
    contra_raw = ""
    try:
        with open(".shadow","r") as pass_fd:
            contra_hash = pass_fd.read()
        
        #comprobamos los permisos
        perms = os.stat(".shadow").st_mode
        
        if perms & stat.S_IRWXO > 0 or perms & stat.S_IRWXG > 0 or perms & stat.S_IWUSR > 0:
            print("El shadow de la contraseña tiene permisos " + \
                str(oct(perms))[-3:] + "! considere cambiarlos a 400")
            logging.warning("El shadow de la contraseña tiene permisos " + \
                str(oct(perms))[-3:] + "! considere cambiarlos a 400")
        
        print("Introduzca la contraseña de administrador:")
    
        #comprobamos que la contraseña introducida es la correcta
        contra_raw = getpass()
        pass_hash = hashlib.sha512(contra_raw.encode()).hexdigest()
        
        if contra_hash != pass_hash:
            print("Contraseña erronea")
            exit(-1)
            
    except FileNotFoundError as e:
        #esto significa que no hay ninguna contraseña guardada
        print("No existe una contraseña almacena o no se puede acceder a ella")
        contra_raw = getpass("Por favor inserte una contraseña:")
        contra_hash = hashlib.sha512(contra_raw.encode()).hexdigest()
        
        try:
            with open(".shadow","x") as pass_fd:
                pass_fd.write(contra_hash)
                
            os.chmod(".shadow",0o400)
        except Exception as e:
            print(e)
            print("Fallo al crear la contraseña")
            exit(-1)
        
    logging.info("Arrancando monitor")

    #Variables para el informe
    analisis = 0
    n_ataques = 0

    hora_inicio = time.strftime("%H:%m")

    #Bucle principal, ejecutar cada x tiempo
    while True:
        print("Comprobando Integridad")
        
        ficheros_corruptos = 0
        ficheros_no_encontrados = 0

        ataque = False
        
        ficheros_total = len(hashes)
        
        for ruta,hash in hashes:
            
            try:
                file_hash = hash_func(open(ruta,"rb").read()).hexdigest()
            except FileNotFoundError as e:
                msg = "===# FICHERO NO ENCONTRADO! #===\n" \
                        "Ruta: " + ruta
                print(msg)
                logging.error("Fallo en:(" + ruta + ") El fichero no se encuntra.  Fecha:(" + str(datetime.datetime.now()) + ")")
                ficheros_no_encontrados += 1
                continue
    
            #fichero leido
            new_hash = hash_func((file_hash + contra_raw).encode()).hexdigest()
            if new_hash != hash:
                msg = "===# FICHERO CORRUPTO! #===\n" + \
                        "Ruta: " + ruta + "\n" \
                        "Hash original:\t" + hash + "\n" \
                        "Hash actual:\t" + new_hash 
                print(msg)
                #_ = messagebox.showerror("ARCHIVO CORRUPTO!", msg)
                logging.error("Fallo en:(" + ruta + ") Hash original:(" + hash + ") Actual:(" + new_hash + ") Fecha:(" + str(datetime.datetime.now()) + ")")
                ficheros_corruptos += 1
    
        logging.info("Integridad comprobada")
        
        #Estadisticas
        porcentaje_corruptos = float(ficheros_corruptos/ficheros_total)*100
        porcentaje_no_encontrados = float(ficheros_no_encontrados/ficheros_total)*100
        
        if porcentaje_corruptos > 10 or porcentaje_no_encontrados > 10:
            ataque = True
            n_ataques +=1
        
        logging.info("Estadisticas: corruptos: " + str(porcentaje_corruptos) \
                    + "% no encontrados: " + str(porcentaje_no_encontrados) + "%")     
        
        print("FICHEROS: " + str(ficheros_total))
        print("CORRUPTOS: " + str(ficheros_corruptos) + " " + str(porcentaje_corruptos)+"%")
        print("NO ENCONTRADOS: " + str(ficheros_no_encontrados) + " " + str(porcentaje_no_encontrados)+"%")
        print("VICTIMA DE ATAQUE:" + str(ataque))
        print(" -- ")
        
        analisis += 1

        if(time.strftime("%H:%M")) == hora_inicio:
            gen_informe(analisis,n_ataques,log_path)
            #Reiniciamos las variables utilizadas para las estadisticas del informe
            analisis = 0
            n_ataques = 0
            #Generamos un nuevo log
            logging.basicConfig(level=logging.DEBUG,filename=log_path,format = log_format,filemode='w')
        time.sleep(intervalo)
            
main()
