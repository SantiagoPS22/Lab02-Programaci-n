import os
import unittest
import uuid
import json
import client.virtuallab_client as virtuallab_client

class Test(unittest.TestCase):

    url = "http://127.0.0.1:80"

    def setUp(self):
        # Generar IDs únicos para no chocar con la base de datos existente
        self.professor_id = int(uuid.uuid4().hex[:8], 16)
        self.student_id = int(uuid.uuid4().hex[:8], 16)
        self.professor_name = "TestProf"
        self.student_name = "TestStudent"
        self.professor_password = "prof_pass"
        self.student_password = "stud_pass"

        virtuallab_client.registerUser(self.url, self.professor_name, self.professor_id, "professor", self.professor_password)
        virtuallab_client.registerUser(self.url, self.student_name, self.student_id, "student", self.student_password)

    def _create_temp_zip(self, file_path):
        """Función auxiliar para crear archivos temporales simulando un laboratorio"""
        with open(file_path, "wb") as f:
            f.write(b"Contenido simulado de un archivo zip")
        return file_path

    def test_register_user(self):
        new_id = int(uuid.uuid4().hex[:8], 16)
        response = virtuallab_client.registerUser(self.url, "Nuevo", new_id, "student", "pass")
        self.assertEqual(response, "User Nuevo with role student registered")
        
        # Prueba usuario duplicado
        response_dup = virtuallab_client.registerUser(self.url, "Nuevo", new_id, "student", "pass")
        self.assertEqual(response_dup, "User already registered")

    def test_open_session(self):
        response = virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        self.assertEqual(response, "Session was succesfully opened")
        
        response_err = virtuallab_client.openSession(self.url, self.professor_id, "wrong_pass")
        self.assertEqual(response_err, "error")

    def test_close_session(self):
        virtuallab_client.openSession(self.url, self.student_id, self.student_password)
        response = virtuallab_client.closeSession(self.url, self.student_id)
        self.assertEqual(response, "Session was succesfully closed")

    def test_upload_lab(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        
        temp_zip = f"client/test_upload_{self.professor_id}.zip"
        self._create_temp_zip(temp_zip)
        
        # Llamada exacta a tu cliente: url, id, file_path
        response = virtuallab_client.uploadLab(self.url, self.professor_id, temp_zip)
        self.assertEqual(response, "File was succesfully received")

        if os.path.exists(temp_zip): os.remove(temp_zip)

    def test_list_professors_labs(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        
        temp_zip = f"client/test_list_{self.professor_id}.zip"
        self._create_temp_zip(temp_zip)
        virtuallab_client.uploadLab(self.url, self.professor_id, temp_zip)
        
        response = virtuallab_client.listProfessorsLabs(self.url, self.professor_id)
        # Extraemos solo el nombre del archivo para comparar
        file_name = os.path.basename(temp_zip)
        self.assertIn(file_name, response)

        if os.path.exists(temp_zip): os.remove(temp_zip)

    def test_list_students(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        response_str = virtuallab_client.listStudents(self.url, self.professor_id)
        students_list = json.loads(response_str)
        
        student_ids = [str(s["id"]) for s in students_list]
        self.assertIn(str(self.student_id), student_ids)

    def test_assign_lab(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        
        lab_name = f"test_assign_{self.professor_id}"
        temp_zip = f"client/{lab_name}.zip"
        self._create_temp_zip(temp_zip)
        
        virtuallab_client.uploadLab(self.url, self.professor_id, temp_zip)
        
        response = virtuallab_client.assignLab(self.url, self.professor_id, lab_name, self.student_id)
        expected_msg = f"Lab {lab_name} successfully assigned to student {self.student_id} by professor {self.professor_id}"
        self.assertEqual(response, expected_msg)

        if os.path.exists(temp_zip): os.remove(temp_zip)

    def test_list_student_labs(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        virtuallab_client.openSession(self.url, self.student_id, self.student_password)
        
        lab_name = f"test_stud_lab_{self.professor_id}"
        temp_zip = f"client/{lab_name}.zip"
        self._create_temp_zip(temp_zip)
        
        virtuallab_client.uploadLab(self.url, self.professor_id, temp_zip)
        virtuallab_client.assignLab(self.url, self.professor_id, lab_name, self.student_id)
        
        response = virtuallab_client.listStudentLabs(self.url, self.student_id)
        self.assertIn(f"{lab_name}.zip", response)

        if os.path.exists(temp_zip): os.remove(temp_zip)

    def test_download_lab(self):
        virtuallab_client.openSession(self.url, self.professor_id, self.professor_password)
        virtuallab_client.openSession(self.url, self.student_id, self.student_password)
        
        lab_name = f"test_download_{self.professor_id}"
        file_name = f"{lab_name}.zip"
        temp_zip = f"client/{file_name}"
        self._create_temp_zip(temp_zip)
        
        virtuallab_client.uploadLab(self.url, self.professor_id, temp_zip)
        virtuallab_client.assignLab(self.url, self.professor_id, lab_name, self.student_id)
        
        response = virtuallab_client.downloadLab(self.url, self.student_id, file_name)
        self.assertNotEqual(response, "error")

        if os.path.exists(temp_zip): os.remove(temp_zip)

if __name__ == '__main__':
    unittest.main()