import hashlib

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

print('Introduce su nombre de usuario')
username = input()
print('Introduce la contraseña que desea almacenar')
password = input()
if check_password(password):
    h = hashlib.sha512(password.encode('utf-8')).hexdigest()
    print(h)
else:
    print('Contraseña no válida')
