import hashlib
import random
from base import engine_hash, Hash_Base, reset_db
from base_hash import *
from sqlalchemy.sql import insert


def check_password(passwd):
    val = True
    if len(passwd) < 8:
        print('La contraseña debe ser tener como minimo 8 caracteres')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('La contraseña debe tener al menos un caracter numérico')
        val = False

    if not any(char.isupper() for char in passwd):
        print('La contraseña deber tener al menos un caracter en mayúscula')
        val = False

    if not any(char.islower() for char in passwd):
        print('La contraseña deber tener al menos un caracter en minúscula')
        val = False

    return val


data = {}

print('Introduce su nombre de usuario')
username = input()
data["Name"] = username

print('Desea almacenar una contraseña (1) o generarla en base a unas palabras que conozca (2)')
opcion = input()
if opcion == "1":
    print('Escriba la contraseña')
    password = input()
    if check_password(password):
        data["Password"] = password
        h = hashlib.sha512(password.encode('utf-8')).hexdigest()
        data["Hashed_Passw"] = h
        print(password)
if opcion == "2":
    print('¿Cuantas palabras quiere poner?')
    n = input()
    palabras = []
    for i in range(1, int(n) + 1):
        print('Palabra número ' + str(i))
        palabra = input()
        palabras.append(palabra)
    random.shuffle(palabras)
    res = ''.join(palabras)
    res = res + str(random.randint(1, 101))

    if check_password(res):
        data["Password"] = res
        h = hashlib.sha512(res.encode('utf-8')).hexdigest()
        data["Hashed_Passw"] = h
        print(res)

print("¿Está seguro de guardar esta contraseña? (0, 1) ")
decision = input()

if decision == "1":

    # Establishing a connection to the database
    connection = engine_hash.connect()

    try:
        ins = insert(NamePassw)
        connection.execute(ins, data)

    except ValueError as vx:
        print(vx)

    except Exception as ex:
        print(ex)

    else:
        print("Inserted Name: " + data["Name"] + " with Password: " + data["Password"] +
              " and Hashed Password (sha512): " + data["Hashed_Passw"])
    finally:
        # Close connection after insert
        connection.close()

else:
    print("Proceso abortado")
