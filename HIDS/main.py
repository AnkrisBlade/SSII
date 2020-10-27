import csv
import hashlib
import time
import os
import logging
import configparser
import os.path
from tkinter import messagebox

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
        if os.path.isfile(path):
            return path
        
    return None
            

def main():
    intervalo = 3600
    log_path = "hids.log"
    db_path = "hids.csv"
    
    config = configparser.ConfigParser()
    if get_config_file == None:
        print("No se encontró ningún archivo de configuracion")
        
    config.read("hids.ini")
    
    intervalo = int(config.get("General","intervalo"))
    log_path = config.get("General","log")
    db_path = config.get("General","database")
    
    #inicializar log
    log_format = "[%(levelname)s] %(asctime)s : %(message)s"
    logging.basicConfig(level=logging.DEBUG,filename=log_path,format = log_format)
    
    hashes = read_database(db_path)
    
    #Bucle principal, ejecutar cada x tiempo
    while True:
        print("Comprobando Integridad")
        
        for ruta,hash in hashes:
            new_hash = hashlib.sha1(open(ruta).read().encode()).hexdigest()
            if new_hash != hash:
                msg = "===# ARCHIVO CORRUPTO! #===\n" + \
                        "Ruta: " + ruta + "\n" \
                        "SHA1 Original:\t" + hash + "\n" \
                        "SHA1 Actual:\t" + new_hash 
                print(msg)
                #_ = messagebox.showerror("ARCHIVO CORRUPTO!", msg)
                logging.error("Fallo en:(" + ruta + ") Hash original:(" + hash + ") Actual:(" + new_hash + ")")
            
            logging.info("Integridad comprobada")
             
        print(" -- ")
        
        time.sleep(intervalo)
        
main()
