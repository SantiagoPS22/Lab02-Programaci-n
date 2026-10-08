# Se deben codificar las siguientes funciones y replicar la funcionalidad descrita en los comentarios
# Además, para la gestión de usuarios y prácticas de laboratorio se debe hacer uso de archivos de texto no se permite
# el uso de motores de bases de datos


import os
from json import dumps # Convertir diccionario a JSON
from json import loads # Convertir JSON a diccionario
ACTIVE_SESSIONS = {}
usersFile = "server/users.txt"

def writeUserDataToFile(user_data):
    with open(usersFile, "a") as file:
        file.write(dumps(user_data) + "\n")

# Función para registrar un usuario con nombre name, identificador id, rol role y contraseña password.
# Registra el usuario en el sistema si el id del usuario no existe previamente. Si el usuario se pudo registrar debe retornar "User {name} with role {role} registered" de lo contrario
# debe retornar "User already registered"
def registerUser(name,id,role,password):
    
    try:
        file=open(usersFile, "r")        

    except FileNotFoundError:
        #Archivo no existe
        print("File not found, creating a new one.")
         
                      
    else:
        with file:
            lines=file.readlines()
            for line in lines:
                user=loads(line)
                if user["id"]==id:
                    response="User already registered"
                    print(response)
                    return response

    
    #######################################
    user_data = {
        "name": name,
        "id": id,
        "role": role,
        "password": password
    }

    writeUserDataToFile(user_data)
    response=f"User {name} with role {role} registered"
    print(response)
    return response
            




            

# Función que abre una sesión
# Abre una sesión del usuario 
# lo hace si el id del usuario y la contraseña son correctos
# Si la sesión se pudo abrir debe retornar "Session was succesfully opened" de lo contrario
# debe retornar "error"
def openSession(id,password):
    try:
        file=open(usersFile, "r")        
    
    except FileNotFoundError:
        #Archivo no existe
        print("File not found")

    else:
        response = None
        with file:
            lines=file.readlines()
            for line in lines:
                user=loads(line)
                if user["id"]==id and user["password"] == password:
                    ACTIVE_SESSIONS[id] = {
                        "name": user.get("name"),
                        "role": user.get("role")
                    }
                    response=f"openSession called by user {id}"
                    break
        if response is None:
            response = "Unable to log in; user details are incorrect."

    print(response)
    return response

# Función que cierra una sesión
# Cierra una sesión del usuario
# Si la sesión se pudo cerrar debe retornar "Session was succesfully closed" de lo contrario
# debe retornar "error"
def closeSession(id):
    if id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[id]
        response = "Session was succesfully closed"
    else:
        response = "error"
    print(response)
    return response

# Función para recibir una práctica de laboratorio (archivo zip) de un profesor
# Recibe una práctica de laboratorio si el usuario es un profesor y se encuentra con sesión abierta
# Si se recibe el archivo correctamente se debe retornar  "File was succesfully received" de lo contrario
# debe retornar "error"
# Se proporciona un código de ejemplo pero se deben implementar las validaciones de usuario y de sesión abierta
def uploadLab(id,file_name,file_data):
    upload_dir = "server/labs"
    os.makedirs(upload_dir, exist_ok=True)

    target_path = os.path.join(upload_dir, file_name)
    with open(target_path, "wb") as f:
            f.write(file_data)
    response=f"uploadLab called by user {id}"    
    return response

# Función para enviar una práctica de laboratorio (archivo zip) a un estudiante
# Envía una práctica de laboratorio si el usuario es un estudiante, se encuentra con sesión abierta
# y la práctica de laboratorio está asignada a él.
# Si el archivo no existe debe retornar "error"
# Se proporciona un código de ejemplo pero se deben implementar las validaciones de usuario, sesión abierta y asignación de la práctica de laboratorio
def downloadLab(id,file_name):
    response=f"error"        
    upload_dir = "server/labs"
    file_path = os.path.join(upload_dir, file_name)
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            response=f"downloadLab called by user {id}"
            print(response)
            return data
    except FileNotFoundError:
        print(response)
        return response

# Función para listar las prácticas de laboratorio disponibles para un estudiante
# Lista las prácticas de laboratorio disponibles para un estudiante si el usuario es un estudiante y se encuentra con sesión abierta
# Si el usuario no es un estudiante o no tiene sesión abierta debe retornar "error"
def listStudentLabs(id):
    response=f"listStudentLabs called by user {id}"        
    print(response)
    return response


# Función para listar las prácticas de laboratorio cargadas por los profesores
# Lista las prácticas de laboratorio cargadas por los profesores si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"   
def listProfessorsLabs(id):
    response=f"listProfessorsLabs called by user {id}"        
    print(response)
    return response

# Función para listar los estudiantes registrados en el sistema
# Lista los estudiantes registrados en el sistema si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"
def listStudents(id):
    if id not in ACTIVE_SESSIONS or ACTIVE_SESSIONS[id]["role"] != "professor":
        response = "error"
        print(response)
        return response

    students = []
    try:
        with open(usersFile, "r") as file:
            for line in file:
                user = loads(line)
                if user["role"] == "student":
                    students.append({"id": user["id"], "name": user["name"]})
    except FileNotFoundError:
        pass

    response = dumps(students)
    print(response)
    return response
# Función para asignar una práctica de laboratorio a un estudiante
# Asigna una práctica de laboratorio a un estudiante si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta o el estudiante no existe o la práctica no existe debe retornar "error"
def assignLab(id,lab_name,student_id):
    response=f"assignLab called by user {id} to assign lab {lab_name} to student {student_id}"        
    print(response)
    return response
    
   
    

                
                
            
        
    
            
    
