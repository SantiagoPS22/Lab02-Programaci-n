# Se deben codificar las siguientes funciones y replicar la funcionalidad descrita en los comentarios
# Además, para la gestión de usuarios y prácticas de laboratorio se debe hacer uso de archivos de texto no se permite
# el uso de motores de bases de datos


import os
from json import dumps # Convertir diccionario a JSON
from json import loads # Convertir JSON a diccionario
usersFile = "server/users.txt"
labsFile = "server/labs.txt"

def writeUserDataToFile(user_data):
    os.makedirs(os.path.dirname(usersFile), exist_ok=True)
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
    user_data = {
        "name": name,
        "id": id,
        "role": role,
        "password": password,
        "session":False
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
def openSession(id, password):
    try:
        with open(usersFile, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        response = "error"
        print(response)
        return response

    user_authenticated = False
    updated_lines = []

    for line in lines:
        if line.strip():
            user = loads(line)
            if user.get("id") == id and user.get("password") == password:
                user["session"] = True
                user_authenticated = True
            updated_lines.append(dumps(user) + "\n")

    if user_authenticated:
        with open(usersFile, "w") as file:
            file.writelines(updated_lines)
        response = "Session was succesfully opened" # Mensaje corregido según especificación
    else:
        response = "error" # Mensaje corregido según especificación

    print(response)
    return response

# Función que cierra una sesión
# Cierra una sesión del usuario
# Si la sesión se pudo cerrar debe retornar "Session was succesfully closed" de lo contrario
# debe retornar "error"


def closeSession(id):
    try:
        with open(usersFile, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found")
        response = "error"
        print(response)
        return response

    session_closed = False
    updated_lines = []

    for line in lines:
        if line.strip():
            user = loads(line)
            # Verifica que el id coincida y que tenga la sesión activa (True)
            if user.get("id") == id and user.get("session") is True:
                user["session"] = False
                session_closed = True
            updated_lines.append(dumps(user) + "\n")

    if session_closed:
        with open(usersFile, "w") as file:
            file.writelines(updated_lines)
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
def uploadLab(id, file_name, file_data):
    # 1. Validar extensión .zip
    if not file_name.lower().endswith(".zip"):
        response = "error"
        print(response)
        return response

    # 2. Validar que el usuario exista, sea profesor y tenga la sesión abierta
    is_authorized = False
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip():
                    user = loads(line)
                    if (user.get("id") == id and 
                        user.get("role") == "professor" and 
                        user.get("session") is True):
                        is_authorized = True
                        break
    except FileNotFoundError:
        print("File not found")
        response = "error"
        print(response)
        return response

    if not is_authorized:
        response = "error"
        print(response)
        return response

    # 3. Guardar el archivo .zip en el servidor
    upload_dir = "server/labs"
    os.makedirs(upload_dir, exist_ok=True)
    target_path = os.path.join(upload_dir, file_name)

    try:
        with open(target_path, "wb") as f:
            f.write(file_data)

        # 4. Registrar el laboratorio en el archivo en formato JSON Lines
        lab_record = {
            "professor_id": id,
            "file_name": file_name,
            "assigned_users": []
        }

        with open(labsFile, "a") as f:
            f.write(dumps(lab_record) + "\n")

        response = "File was succesfully received"
    except Exception:
        response = "error"

    print(response)
    return response

# Función para enviar una práctica de laboratorio (archivo zip) a un estudiante
# Envía una práctica de laboratorio si el usuario es un estudiante, se encuentra con sesión abierta
# y la práctica de laboratorio está asignada a él.
# Si el archivo no existe debe retornar "error"
# Se proporciona un código de ejemplo pero se deben implementar las validaciones de usuario, sesión abierta y asignación de la práctica de laboratorio
def downloadLab(id, file_name):
    response = "error"

    # 1. Validar que el usuario sea estudiante y tenga la sesión abierta
    is_authorized_student = False
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip():
                    user = loads(line)
                    if (user.get("id") == id and 
                        user.get("role") == "student" and 
                        user.get("session") is True):
                        is_authorized_student = True
                        break
    except FileNotFoundError:
        print("File not found")
        print(response)
        return response

    if not is_authorized_student:
        print(response)
        return response

    # 2. Validar que la práctica exista en labsFile y esté asignada al id del estudiante
    is_lab_assigned = False
    try:
        with open(labsFile, "r") as file:
            for line in file:
                if line.strip():
                    lab = loads(line)
                    if lab.get("file_name") == file_name and id in lab.get("assigned_users", []):
                        is_lab_assigned = True
                        break
    except FileNotFoundError:
        print("File not found")
        print(response)
        return response

    if not is_lab_assigned:
        print(response)
        return response

    # 3. Leer y retornar el archivo físico si todo es correcto
    upload_dir = "server/labs"
    file_path = os.path.join(upload_dir, file_name)

    try:
        with open(file_path, "rb") as f:
            data = f.read()
            response = f"downloadLab called by user {id}"
            print(response)
            return data
    except FileNotFoundError:
        print(response)
        return response

# Función para listar las prácticas de laboratorio disponibles para un estudiante
# Lista las prácticas de laboratorio disponibles para un estudiante si el usuario es un estudiante y se encuentra con sesión abierta
# Si el usuario no es un estudiante o no tiene sesión abierta debe retornar "error"
def listStudentLabs(id):
    # 1. Validar que el usuario sea estudiante y tenga la sesión abierta
    is_authorized_student = False
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip():
                    user = loads(line)
                    if (user.get("id") == id and 
                        user.get("role") == "student" and 
                        user.get("session") is True):
                        is_authorized_student = True
                        break
    except FileNotFoundError:
        print("File not found")
        response = "error"
        print(response)
        return response

    if not is_authorized_student:
        response = "error"
        print(response)
        return response

    # 2. Obtener las prácticas asignadas desde labsFile
    assigned_labs = []
    try:
        with open(labsFile, "r") as file:
            for line in file:
                if line.strip():
                    lab = loads(line)
                    if id in lab.get("assigned_users", []):
                        assigned_labs.append(lab.get("file_name"))
    except FileNotFoundError:
        # Si el archivo labsFile aún no existe, no hay prácticas asignadas
        pass

    # 3. Retornar la lista o el mensaje si no tiene asignaciones
    if assigned_labs:
        print(assigned_labs)
        return assigned_labs
    else:
        response = f"No lab practices assigned to student {id}"
        print(response)
        return response

# Función para listar las prácticas de laboratorio cargadas por los profesores
# Lista las prácticas de laboratorio cargadas por los profesores si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"   
def listProfessorsLabs(id):
    # 1. Validar que el usuario sea profesor y tenga la sesión abierta
    is_authorized_professor = False
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip():
                    user = loads(line)
                    if (user.get("id") == id and 
                        user.get("role") == "professor" and 
                        user.get("session") is True):
                        is_authorized_professor = True
                        break
    except FileNotFoundError:
        print("File not found")
        response = "error"
        print(response)
        return response

    if not is_authorized_professor:
        response = "error"
        print(response)
        return response

    # 2. Obtener todas las prácticas registradas en labsFile
    all_labs = []
    try:
        with open(labsFile, "r") as file:
            for line in file:
                if line.strip():
                    lab = loads(line)
                    file_name = lab.get("file_name")
                    if file_name and file_name not in all_labs:
                        all_labs.append(file_name)
    except FileNotFoundError:
        # Si el archivo labsFile aún no existe, no hay prácticas creadas
        pass

    # 3. Retornar la lista de laboratorios o el mensaje en caso de estar vacío
    if all_labs:
        print(all_labs)
        return all_labs
    else:
        response = "No lab practices created"
        print(response)
        return response

# Función para listar los estudiantes registrados en el sistema
# Lista los estudiantes registrados en el sistema si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta debe retornar "error"
def listStudents(id):
    # 1. Validar que quien consulta sea profesor con sesión activa
    is_authorized_professor = False
    try:
        with open(usersFile, "r") as file:
            lines = [loads(line) for line in file if line.strip()]
            for user in lines:
                if user.get("id") == id and user.get("role") == "professor" and user.get("session") is True:
                    is_authorized_professor = True
                    break
    except FileNotFoundError:
        print("error")
        return "error"

    if not is_authorized_professor:
        print("error")
        return "error"

    # 2. Filtrar los usuarios con rol 'student'
    students = [{"id": u["id"], "name": u["name"]} for u in lines if u.get("role") == "student"]

    response = dumps(students)
    print(response)
    return response

# Función para asignar una práctica de laboratorio a un estudiante
# Asigna una práctica de laboratorio a un estudiante si el usuario es un profesor y se encuentra con sesión abierta
# Si el usuario no es un profesor o no tiene sesión abierta o el estudiante no existe o la práctica no existe debe retornar "error"
def assignLab(id, lab_name, student_id):
    # 1. Validar profesor activo y estudiante existente en usersFile
    is_professor_active = False
    is_valid_student = False
    print(id, lab_name, student_id)
    try:
        with open(usersFile, "r") as file:
            for line in file:
                if line.strip():
                    user = loads(line)
                    # Comprueba profesor con sesión activa
                    if user.get("id") == id and user.get("role") == "professor" and user.get("session") is True:
                        is_professor_active = True
                    # Comprueba estudiante registrado
                    if user.get("id") == student_id and user.get("role") == "student":
                        is_valid_student = True
    except FileNotFoundError:
        print("File not found")
        response = "error1"
        print(response)
        return response

    if not is_professor_active or not is_valid_student:
        response = "error2"
        print(response)
        return response

    # 2. Validar existencia del laboratorio y verificar duplicados en labsFile
    lab_found = False
    already_assigned = False
    updated_lines = []

    try:
        with open(labsFile, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found")
        response = "error3"
        print(response)
        return response

    for line in lines:
        if line.strip():
            lab = loads(line)
            if lab.get("file_name") == lab_name + ".zip":
                lab_found = True
                assigned_list = lab.get("assigned_users", [])
                
                if student_id in assigned_list:
                    already_assigned = True
                else:
                    assigned_list.append(student_id)
                    lab["assigned_users"] = assigned_list
            
            updated_lines.append(dumps(lab) + "\n")

    if not lab_found:
        response = "error4"
        print(response)
        return response

    # 3. Si ya estaba asignado, omitir la escritura y retornar aviso
    if already_assigned:
        response = f"Student {student_id} is already assigned to lab {lab_name}"
        print(response)
        return response

    # 4. Guardar los cambios en el archivo labsFile
    with open(labsFile, "w") as file:
        file.writelines(updated_lines)

    response = f"Lab {lab_name} successfully assigned to student {student_id} by professor {id}"
    print(response)
    return response
     

            
    
