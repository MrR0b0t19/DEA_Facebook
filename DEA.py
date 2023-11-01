import os
import requests
import json
import sys
import time
import getpass
import hashlib

# Variable global para almacenar el token de acceso
access_token = ""
jml = []

# Función para obtener el token de acceso
def obtener_token():
    global access_token

    print('[*] Generando token de acceso ')

    try:
        os.mkdir('cookie')
    except OSError:
        pass

    b = open('cookie/token.log', 'w')
    try:
        id = input('[?] Username (Email): ')
        pwd = getpass.getpass('[?] Password: ')
        API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
        data = {
            "api_key": "882a8490361da98702bf97a021ddc14d",
            "credentials_type": "password",
            "email": id,
            "format": "JSON",
            "generate_machine_id": "1",
            "generate_session_cookies": "1",
            "locale": "en_US",
            "method": "auth.login",
            "password": pwd,
            "return_ssl_resources": "0",
            "v": "1.0"
        }
        sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail=' + id + 'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword=' + pwd + 'return_ssl_resources=0v=1.0' + API_SECRET
        x = hashlib.new('md5')
        x.update(sig.encode('utf-8'))

        data.update({'sig': x.hexdigest()})

        try:
            r = requests.get('https://api.facebook.com/restserver.php', params=data)
            a = json.loads(r.text)
            access_token = a['access_token']
            b.write(access_token)
            b.close()
            print('[*] Token generado correctamente')
            print('[*] Tu token de acceso está almacenado en cookie/token.log')
        except KeyError:
            print('[!] Fallo al generar tu token ')
            print('[!] Checa tu conexión / email o password')
            os.remove('cookie/token.log')
    except requests.exceptions.ConnectionError:
        print('[!] Fallo al generar tu token')
        print('[!] Error de conexión!!!')
        os.remove('cookie/token.log')
    main()

# Función para obtener información de amigos por ID
def obtener_id():
    global access_token

    if not access_token:
        print("[!] Necesitas generar tu token de acceso primero.")
        return

    print('[*] Obteniendo todos los IDs')

    try:
        r = requests.get('https://graph.facebook.com/me/friends?access_token=' + access_token)
        friend_data = json.loads(r.text)

        with open('output/friends_id.txt', 'w') as out_file:
            for friend in friend_data['data']:
                out_file.write(friend['id'] + '\n')
                print(f'[*] {friend["id"]} retrieved')

        print('[*] Todos los IDs de amigos se guardaron correctamente')
        print('[*] Archivo guardado: output/friends_id.txt')
    except requests.exceptions.ConnectionError:
        print('[!] Error de conexión')
        print('[!] Detenido')

# Función para obtener información de amigos por número de teléfono
def obtener_telefono():
    global access_token

    if not access_token:
        print("[!] Tu necesitas generar tu token de acceso primero.")
        return

    print('[*] Obteniendo todos los números de amigos')

    try:
        r = requests.get('https://graph.facebook.com/me/friends?access_token=' + access_token)
        friend_data = json.loads(r.text)

        with open('output/friends_phone.txt', 'w') as out_file:
            for friend in friend_data['data']:
                friend_id = friend['id']
                x = requests.get(f"https://graph.facebook.com/{friend_id}?access_token={access_token}")
                friend_info = json.loads(x.text)

                phone = friend_info.get('Numero de telefono', '')
                if phone:
                    out_file.write(phone + '\n')
                    print(f'[*] ID de amigos: {friend_id}, Teléfono: {phone}')

        print('[*] Todos los números de teléfonos de amigos se guardaron correctamente')
        print('[*] Guardados en: output/friends_phone.txt')
    except requests.exceptions.ConnectionError:
        print('[!] Error de conexión')
        print('[!] Detenido')

# Función para obtener información de amigos por dirección de correo electrónico
def obtener_email():
    global access_token

    if not access_token:
        print("[!] Tu necesitas generar el token de acceso primero.")
        return

    print('[*] Obteniendo todos los emails')

    try:
        r = requests.get('https://graph.facebook.com/me/friends?access_token=' + access_token)
        friend_data = json.loads(r.text)

        with open('output/friends_emails.txt', 'w') as out_file:
            for friend in friend_data['data']:
                friend_id = friend['id']
                x = requests.get(f"https://graph.facebook.com/{friend_id}?access_token={access_token}")
                friend_info = json.loads(x.text)

                email = friend_info.get('email', '')
                if email:
                    out_file.write(email + '\n')
                    print(f'[*] ID de amigos: {friend_id}, Email: {email}')

        print('[*] Todos los emails de amigos se guardaron correctamente')
        print('[*] Guardados en: output/friends_emails.txt')
    except requests.exceptions.ConnectionError:
        print('[!] Error de conexión')
        print('[!] Detenido')

def getdata():
    global a, access_token

    print('[*] Cargando Token de Acceso')

    try:
        access_token = open("cookie/token.log", "r").read()
        print('[*] Token de acceso cargado con éxito')
    except FileNotFoundError:
        print('[!] Error al abrir cookie/token.log')
        print('[!] Escribe "token" para generar un token de acceso')
        main()

    print('[*] Recopilando todos los datos de amigos')

    try:
        r = requests.get(f'https://graph.facebook.com/me/friends?access_token={access_token}')
        a = json.loads(r.text)

    except KeyError:
        print('[!] Tu token de acceso ha expirado')
        print('[!] Escribe "token" para generar un nuevo token de acceso')
        main()

    except requests.exceptions.ConnectionError:
        print('[!] Error de conexión')
        print('[!] Detenido')
        main()

    for friend in a['data']:
        jml.append(friend['id'])
        print(f'\r[*] Recopilando datos de {len(jml)} amigos', end='', flush=True)
        time.sleep(0.0001)

    print(f'\r[*] {len(jml)} datos de amigos recuperados con éxito')
    main()

#buscar
def buscar():
    if len(jml) == 0:
        print("[!] No hay datos de amigos en la base de datos")
        print('[!] Escribe "getdata" para recopilar datos de amigos')
        main()
    else:
        pass

    target = input("[!] Buscar por nombre o ID: ")

    if target == '':
        print("[!] El nombre o ID no puede estar vacío")
        buscar()
    else:
        info(target)
#buscando
def info(target):
    global a, token

    print('[*] Buscando')
    for friend in a['data']:
        if target in friend['name'] or target in friend['id']:
            x = requests.get(f"https://graph.facebook.com/{friend['id']}?access_token={token}")
            friend_info = json.loads(x.text)

            print(' ')
            print('[-------- INFORMACIÓN --------]'.center(44))
            print(' ')

            try:
                print(f'[*] ID: {friend_info["id"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Nombre de usuario: {friend_info["username"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Correo Electrónico: {friend_info["email"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Teléfono Móvil: {friend_info["mobile_phone"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Nombre: {friend_info["name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Primer Nombre: {friend_info["first_name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Segundo Nombre: {friend_info["middle_name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Apellido: {friend_info["last_name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Idioma: {friend_info["locale"].split("_")[0]}')
            except KeyError:
                pass
            try:
                print(f'[*] Ubicación: {friend_info["location"]["name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Ciudad Natal: {friend_info["hometown"]["name"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Género: {friend_info["gender"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Religión: {friend_info["religion"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Estado de Relación: {friend_info["relationship_status"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Orientación Política: {friend_info["political"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Trabajo:')

                for work_info in friend_info.get('work', []):
                    try:
                        print(f'   [-] Posición: {work_info["position"]["name"]}')
                    except KeyError:
                        pass
                    try:
                        print(f'   [-] Empleador: {work_info["employer"]["name"]}')
                    except KeyError:
                        pass
                    try:
                        if work_info['start_date'] == "0000-00":
                            print('   [-] Fecha de Inicio: ---')
                        else:
                            print(f'   [-] Fecha de Inicio: {work_info["start_date"]}')
                    except KeyError:
                        pass
                    try:
                        if work_info['end_date'] == "0000-00":
                            print('   [-] Fecha de Fin: ---')
                        else:
                            print(f'   [-] Fecha de Fin: {work_info["end_date"]}')
                    except KeyError:
                        pass
                    try:
                        print(f'   [-] Ubicación: {work_info["location"]["name"]}')
                    except KeyError:
                        pass
                    print(' ')
            except KeyError:
                pass
            try:
                print(f'[*] Fecha de Actualización: {friend_info["updated_time"][:10]} {friend_info["updated_time"][11:19]}')
            except KeyError:
                pass
            try:
                print('[*] Idiomas:')
                for lang in friend_info.get('languages', []):
                    try:
                        print(f' ~ {lang["name"]}')
                    except KeyError:
                        pass
            except KeyError:
                pass
            try:
                print(f'[*] Biografía: {friend_info["bio"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Citas: {friend_info["quotes"]}')
            except KeyError:
                pass
            try:
                print(f'[*] Cumpleaños: {friend_info["birthday"].replace("/", "-")}')
            except KeyError:
                pass
            try:
                print(f'[*] Enlace: {friend_info["link"]}')
            except KeyError:
                pass
            try:
                print('[*] Equipos Favoritos:')
                for team in friend_info.get('favorite_teams', []):
                    try:
                        print(f' ~ {team["name"]}')
                    except KeyError:
                        pass
            except KeyError:
                pass
            try:
                print('[*] Escuela:')
                for edu_info in friend_info.get('education', []):
                    try:
                        print(f' ~ {edu_info["school"]["name"]}')
                    except KeyError:
                        pass  # Agregar "pass" para mantener el bloque except no vacío
            except KeyError:
                pass

            
# Función principal con el menú
def main():
    print("Datos Extraídos con Accesos FB ")
    print("0. Generar token de acceso")
    print("1. Extraer toda la info para lo demás")
    print("2. Extraer ID de amigos")
    print("3. Extraer números de amigos")
    print("4. Extraer Email")
    print("5. Extraer datos a un amigo")
    print("6. Salir")

    choice = input("Tu opción: ")

    if choice == '0':
        obtener_token()
    elif choice == '1':
        getdata()
    elif choice == '2':
        obtener_id()
    elif choice == '3':
        obtener_telefono()
    elif choice == '4':
        obtener_email()
    elif choice == '5':
        buscar()
        info()
    elif choice == '6':
        sys.exit()
    else:
        print("[!] Selección inválida.")

if __name__ == "__main__":
    main()
