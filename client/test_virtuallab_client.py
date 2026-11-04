import os
import zipfile
import virtuallab_client
from PySpice.Spice.Parser import SpiceParser
from PySpice.Unit import *

url = "http://localhost:80"

print("==================================================")
print(" 1. REGISTRO DE USUARIOS (Profesores y Estudiantes)")
print("==================================================")

# Profesores
prof_1 = {"name": "Alexander", "id": 787878, "role": "professor", "pass": "professor_pass"}
prof_2 = {"name": "Maria", "id": 101010, "role": "professor", "pass": "maria_pass"}

# Estudiantes
stud_1 = {"name": "Helena", "id": 99999, "role": "student", "pass": "student_pass"}
stud_2 = {"name": "Carlos", "id": 88888, "role": "student", "pass": "carlos_pass"}
stud_3 = {"name": "Ana", "id": 77777, "role": "student", "pass": "ana_pass"}

print("Registrando Profesor 1:", virtuallab_client.registerUser(url, prof_1["name"], prof_1["id"], prof_1["role"], prof_1["pass"]))
print("Registrando Profesor 2:", virtuallab_client.registerUser(url, prof_2["name"], prof_2["id"], prof_2["role"], prof_2["pass"]))

print("Registrando Estudiante 1:", virtuallab_client.registerUser(url, stud_1["name"], stud_1["id"], stud_1["role"], stud_1["pass"]))
print("Registrando Estudiante 2:", virtuallab_client.registerUser(url, stud_2["name"], stud_2["id"], stud_2["role"], stud_2["pass"]))
print("Registrando Estudiante 3:", virtuallab_client.registerUser(url, stud_3["name"], stud_3["id"], stud_3["role"], stud_3["pass"]))

# Prueba de duplicado
print("Prueba usuario duplicado:", virtuallab_client.registerUser(url, prof_1["name"], prof_1["id"], prof_1["role"], prof_1["pass"]))


print("\n==================================================")
print(" 2. AUTENTICACIÓN Y SESIONES")
print("==================================================")

# Intento fallido de login
print("Login contraseña errónea:", virtuallab_client.openSession(url, prof_1["id"], "wrong_pass"))

# Login exitoso
print("Login Profesor Alexander:", virtuallab_client.openSession(url, prof_1["id"], prof_1["pass"]))


print("\n==================================================")
print(" 3. OPERACIONES DE PROFESOR")
print("==================================================")

# Cargar prácticas de laboratorio (Archivos .zip)
file_rc = "client/rc.zip"
file_voltage = "client/voltage_divider.zip"

print("Cargando RC Lab:", virtuallab_client.uploadLab(url, prof_1["id"], file_rc))
print("Cargando Voltage Divider Lab:", virtuallab_client.uploadLab(url, prof_1["id"], file_voltage))


# Consultar datos como Profesor
print("\nListar laboratorios cargados:", virtuallab_client.listProfessorsLabs(url, prof_1["id"]))
print("Listar estudiantes registrados:", virtuallab_client.listStudents(url, prof_1["id"]))

# Asignar prácticas a estudiantes
print("\nAsignando 'voltage_divider' a Helena:", virtuallab_client.assignLab(url, prof_1["id"], "voltage_divider", stud_1["id"]))
print("Asignando 'rc' a Helena:", virtuallab_client.assignLab(url, prof_1["id"], "rc", stud_1["id"]))
print("Asignando 'voltage_divider' a Carlos:", virtuallab_client.assignLab(url, prof_1["id"], "voltage_divider", stud_2["id"]))

# Re-asignación duplicada (Debe controlar error o aviso)
print("Asignación duplicada a Helena:", virtuallab_client.assignLab(url, prof_1["id"], "voltage_divider", stud_1["id"]))

# Cierre de sesión del Profesor
print("\nCerrar sesión Profesor Alexander:", virtuallab_client.closeSession(url, prof_1["id"]))


print("\n==================================================")
print(" 4. OPERACIONES DE ESTUDIANTE")
print("==================================================")

# Intento de descarga sin sesión activa (Debe fallar)
print("Descargar sin sesión (Helena):", virtuallab_client.downloadLab(url, stud_1["id"], "voltage_divider.zip"))

# Login Estudiante 1 (Helena)
print("Login Estudiante Helena:", virtuallab_client.openSession(url, stud_1["id"], stud_1["pass"]))

# Consultar laboratorios asignados
print("Laboratorios asignados a Helena:", virtuallab_client.listStudentLabs(url, stud_1["id"]))

# Descargar laboratorio asignado
lab_name = "voltage_divider"
file_name = f"{lab_name}.zip"

print(f"Descargando {file_name}:", virtuallab_client.downloadLab(url, stud_1["id"], file_name))


print("\n==================================================")
print(" 5. EJECUCIÓN Y SIMULACIÓN SPICE")
print("==================================================")

zip_path = f"client/labs/{file_name}"

if os.path.exists(zip_path):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open(f"{lab_name}.cir") as file:
                netlist = file.read().decode("utf-8")
                print("Iniciando simulación SPICE para:", lab_name)
                
                parser = SpiceParser(source=netlist)
                circuit = parser.build_circuit()
                simulator = circuit.simulator(temperature=25, nominal_temperature=25)
                analysis = simulator.operating_point()

                for node in analysis.nodes.values():
                    print(f' Nodo {node}: {float(node[0]):.4f} V')
                
                print("Simulación completada con éxito.")
    except Exception as e:
        print(f"Error procesando simulación SPICE: {e}")
else:
    print(f"No se encontró el archivo {zip_path} para la simulación.")

# Cierre de sesión de Helena
print("Cerrar sesión Helena:", virtuallab_client.closeSession(url, stud_1["id"]))


print("\n==================================================")
print(" 6. VERIFICACIÓN DE OTROS ESTUDIANTES")
print("==================================================")

# Carlos (Tiene 1 laboratorio)
print("Login Carlos:", virtuallab_client.openSession(url, stud_2["id"], stud_2["pass"]))
print("Labs de Carlos:", virtuallab_client.listStudentLabs(url, stud_2["id"]))
print("Cerrar sesión Carlos:", virtuallab_client.closeSession(url, stud_2["id"]))

# Ana (No tiene laboratorios)
print("Login Ana:", virtuallab_client.openSession(url, stud_3["id"], stud_3["pass"]))
print("Labs de Ana (sin asignaciones):", virtuallab_client.listStudentLabs(url, stud_3["id"]))
print("Cerrar sesión Ana:", virtuallab_client.closeSession(url, stud_3["id"]))

print("\n==================================================")
print(" PRUEBAS FINALIZADAS")
print("==================================================")