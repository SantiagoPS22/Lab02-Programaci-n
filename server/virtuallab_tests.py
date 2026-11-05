
import os
import uuid
import zipfile
import virtuallab_client

from unittest import TestCase


class Test(TestCase):

    url = "http://127.0.0.1:80"

    def setUp(self):
        # Crear identificadores únicos para cada prueba
        unique_id = int(uuid.uuid4().hex[:8], 16)

        self.professor_id = unique_id
        self.student_id = unique_id + 1

        self.professor_name = "Alexander"
        self.student_name = "Santiago"

        self.professor_password = "professor_pass"
        self.student_password = "student_pass"

        # Registrar profesor
        virtuallab_client.registerUser(
            self.url,
            self.professor_name,
            self.professor_id,
            "professor",
            self.professor_password
        )

        # Registrar estudiante
        virtuallab_client.registerUser(
            self.url,
            self.student_name,
            self.student_id,
            "student",
            self.student_password
        )

        # Abrir sesiones
        virtuallab_client.openSession(
            self.url, self.professor_id, self.professor_password
        )

        virtuallab_client.openSession(
            self.url, self.student_id, self.student_password
        )

        # Crear directorio de archivos de prueba
        os.makedirs("client", exist_ok=True)

        # Nombre único para el laboratorio
        self.lab_name = "test_" + uuid.uuid4().hex[:8]
        self.file_name = self.lab_name + ".zip"
        self.file_path = os.path.join("client", self.file_name)

        # Crear un ZIP válido
        with zipfile.ZipFile(self.file_path, "w") as zip_file:
            zip_file.writestr("practice.txt", "Laboratorio de prueba")

    def upload_test_lab(self):
        return virtuallab_client.uploadLab(
            self.url,
            self.professor_id,
            self.file_path
        )

    def assign_test_lab(self):
        self.upload_test_lab()

        return virtuallab_client.assignLab(
            self.url,
            self.professor_id,
            self.lab_name,
            self.student_id
        )

    # ==================================================
    # 1. REGISTER USER
    # ==================================================

    def test_register_user(self):
        print("\nStart register test\n")

        name = "Daniel"
        user_id = int(uuid.uuid4().hex[:8], 16)
        role = "student"
        password = "daniel_pass"

        self.assertEqual(
            virtuallab_client.registerUser(
                self.url, name, user_id, role, password
            ),
            f"User {name} with role {role} registered"
        )

        print("\nFinish register test\n")

    def test_register_user_duplicate(self):
        print("\nStart register duplicate test\n")

        self.assertEqual(
            virtuallab_client.registerUser(
                self.url,
                self.professor_name,
                self.professor_id,
                "professor",
                self.professor_password
            ),
            "User already registered"
        )

        print("\nFinish register duplicate test\n")

    # ==================================================
    # 2. OPEN SESSION
    # ==================================================

    def test_open_session(self):
        print("\nStart open session test\n")

        virtuallab_client.closeSession(self.url, self.student_id)

        self.assertEqual(
            virtuallab_client.openSession(
                self.url,
                self.student_id,
                self.student_password
            ),
            "Session was succesfully opened"
        )

        print("\nFinish open session test\n")

    def test_open_session_wrong_password(self):
        print("\nStart open session wrong password test\n")

        self.assertEqual(
            virtuallab_client.openSession(
                self.url, self.student_id, "wrong_password"
            ),
            "error"
        )

        print("\nFinish open session wrong password test\n")

    def test_open_session_nonexistent_user(self):
        print("\nStart open session nonexistent user test\n")

        self.assertEqual(
            virtuallab_client.openSession(
                self.url, 999999999, "password"
            ),
            "error"
        )

        print("\nFinish open session nonexistent user test\n")

    # ==================================================
    # 3. CLOSE SESSION
    # ==================================================

    def test_close_session(self):
        print("\nStart close session test\n")

        self.assertEqual(
            virtuallab_client.closeSession(
                self.url, self.student_id
            ),
            "Session was succesfully closed"
        )

        print("\nFinish close session test\n")

    def test_close_session_already_closed(self):
        print("\nStart close session already closed test\n")

        virtuallab_client.closeSession(self.url, self.student_id)

        self.assertEqual(
            virtuallab_client.closeSession(
                self.url, self.student_id
            ),
            "error"
        )

        print("\nFinish close session already closed test\n")

    def test_close_session_nonexistent_user(self):
        print("\nStart close session nonexistent user test\n")

        self.assertEqual(
            virtuallab_client.closeSession(self.url, 999999999),
            "error"
        )

        print("\nFinish close session nonexistent user test\n")

    # ==================================================
    # 4. UPLOAD LAB
    # ==================================================

    def test_upload_lab(self):
        print("\nStart upload lab test\n")

        self.assertEqual(
            self.upload_test_lab(),
            "File was succesfully received"
        )

        print("\nFinish upload lab test\n")

    def test_upload_lab_invalid_extension(self):
        print("\nStart upload lab invalid extension test\n")

        invalid_path = os.path.join("client", "invalid.txt")

        with open(invalid_path, "w") as file:
            file.write("This is not a ZIP")

        self.assertEqual(
            virtuallab_client.uploadLab(
                self.url, self.professor_id, invalid_path
            ),
            "error"
        )

        print("\nFinish upload lab invalid extension test\n")

    def test_upload_lab_student(self):
        print("\nStart upload lab student test\n")

        self.assertEqual(
            virtuallab_client.uploadLab(
                self.url, self.student_id, self.file_path
            ),
            "error"
        )

        print("\nFinish upload lab student test\n")

    def test_upload_lab_without_session(self):
        print("\nStart upload lab without session test\n")

        virtuallab_client.closeSession(
            self.url, self.professor_id
        )

        self.assertEqual(
            self.upload_test_lab(),
            "error"
        )

        print("\nFinish upload lab without session test\n")

    # ==================================================
    # 5. DOWNLOAD LAB
    # ==================================================

    def test_download_lab(self):
        print("\nStart download lab test\n")

        self.assign_test_lab()

        result = virtuallab_client.downloadLab(
            self.url,
            self.student_id,
            self.file_name
        )

        # El cliente guarda el archivo descargado en client/labs
        downloaded_path = os.path.join(
            "client", "labs", self.file_name
        )

        self.assertTrue(os.path.exists(downloaded_path))

        print("\nFinish download lab test\n")

    def test_download_lab_not_assigned(self):
        print("\nStart download lab not assigned test\n")

        self.upload_test_lab()

        result = virtuallab_client.downloadLab(
            self.url,
            self.student_id,
            self.file_name
        )

        self.assertEqual(result, "error")

        print("\nFinish download lab not assigned test\n")

    def test_download_lab_nonexistent(self):
        print("\nStart download lab nonexistent test\n")

        self.assertEqual(
            virtuallab_client.downloadLab(
                self.url,
                self.student_id,
                "nonexistent.zip"
            ),
            "error"
        )

        print("\nFinish download lab nonexistent test\n")

    def test_download_lab_without_session(self):
        print("\nStart download lab without session test\n")

        self.assign_test_lab()

        virtuallab_client.closeSession(
            self.url, self.student_id
        )

        self.assertEqual(
            virtuallab_client.downloadLab(
                self.url,
                self.student_id,
                self.file_name
            ),
            "error"
        )

        print("\nFinish download lab without session test\n")

    # ==================================================
    # 6. LIST STUDENT LABS
    # ==================================================

    def test_list_student_labs(self):
        print("\nStart list student labs test\n")

        self.assign_test_lab()

        result = virtuallab_client.listStudentLabs(
            self.url, self.student_id
        )

        self.assertIn(self.file_name, result)

        print("\nFinish list student labs test\n")

    def test_list_student_labs_without_session(self):
        print("\nStart list student labs without session test\n")

        virtuallab_client.closeSession(
            self.url, self.student_id
        )

        self.assertEqual(
            virtuallab_client.listStudentLabs(
                self.url, self.student_id
            ),
            "error"
        )

        print("\nFinish list student labs without session test\n")

    def test_list_student_labs_professor(self):
        print("\nStart list student labs professor test\n")

        self.assertEqual(
            virtuallab_client.listStudentLabs(
                self.url, self.professor_id
            ),
            "error"
        )

        print("\nFinish list student labs professor test\n")

    def test_list_student_labs_empty(self):
        print("\nStart list student labs empty test\n")

        result = virtuallab_client.listStudentLabs(
            self.url, self.student_id
        )

        self.assertEqual(
            result,
            f"No lab practices assigned to student {self.student_id}"
        )

        print("\nFinish list student labs empty test\n")

    # ==================================================
    # 7. LIST PROFESSORS LABS
    # ==================================================

    def test_list_professors_labs(self):
        print("\nStart list professors labs test\n")

        self.upload_test_lab()

        result = virtuallab_client.listProfessorsLabs(
            self.url, self.professor_id
        )

        self.assertIn(self.file_name, result)

        print("\nFinish list professors labs test\n")

    def test_list_professors_labs_without_session(self):
        print("\nStart list professors labs without session test\n")

        virtuallab_client.closeSession(
            self.url, self.professor_id
        )

        self.assertEqual(
            virtuallab_client.listProfessorsLabs(
                self.url, self.professor_id
            ),
            "error"
        )

        print("\nFinish list professors labs without session test\n")

    def test_list_professors_labs_student(self):
        print("\nStart list professors labs student test\n")

        self.assertEqual(
            virtuallab_client.listProfessorsLabs(
                self.url, self.student_id
            ),
            "error"
        )

        print("\nFinish list professors labs student test\n")

    # ==================================================
    # 8. LIST STUDENTS
    # ==================================================

    def test_list_students(self):
        print("\nStart list students test\n")

        result = virtuallab_client.listStudents(
            self.url, self.professor_id
        )

        self.assertIn(str(self.student_id), result)
        self.assertIn(self.student_name, result)

        print("\nFinish list students test\n")

    def test_list_students_without_session(self):
        print("\nStart list students without session test\n")

        virtuallab_client.closeSession(
            self.url, self.professor_id
        )

        self.assertEqual(
            virtuallab_client.listStudents(
                self.url, self.professor_id
            ),
            "error"
        )

        print("\nFinish list students without session test\n")

    def test_list_students_student(self):
        print("\nStart list students student test\n")

        self.assertEqual(
            virtuallab_client.listStudents(
                self.url, self.student_id
            ),
            "error"
        )

        print("\nFinish list students student test\n")

    # ==================================================
    # 9. ASSIGN LAB
    # ==================================================

    def test_assign_lab(self):
        print("\nStart assign lab test\n")

        self.upload_test_lab()

        self.assertEqual(
            virtuallab_client.assignLab(
                self.url,
                self.professor_id,
                self.lab_name,
                self.student_id
            ),
            f"Lab {self.lab_name} successfully assigned to student {self.student_id} by professor {self.professor_id}"
        )

        print("\nFinish assign lab test\n")

    def test_assign_lab_duplicate(self):
        print("\nStart assign lab duplicate test\n")

        self.assign_test_lab()

        self.assertEqual(
            virtuallab_client.assignLab(
                self.url,
                self.professor_id,
                self.lab_name,
                self.student_id
            ),
            f"Student {self.student_id} is already assigned to lab {self.lab_name}"
        )

        print("\nFinish assign lab duplicate test\n")

    def test_assign_lab_nonexistent(self):
        print("\nStart assign lab nonexistent test\n")

        self.assertEqual(
            virtuallab_client.assignLab(
                self.url,
                self.professor_id,
                "nonexistent_lab",
                self.student_id
            ),
            "error"
        )

        print("\nFinish assign lab nonexistent test\n")

    def test_assign_lab_nonexistent_student(self):
        print("\nStart assign lab nonexistent student test\n")

        self.upload_test_lab()

        self.assertEqual(
            virtuallab_client.assignLab(
                self.url,
                self.professor_id,
                self.lab_name,
                999999999
            ),
            "error"
        )

        print("\nFinish assign lab nonexistent student test\n")

    def test_assign_lab_without_session(self):
        print("\nStart assign lab without session test\n")

        self.upload_test_lab()

        virtuallab_client.closeSession(
            self.url, self.professor_id
        )

        self.assertEqual(
            virtuallab_client.assignLab(
                self.url,
                self.professor_id,
                self.lab_name,
                self.student_id
            ),
            "error"
        )

        print("\nFinish assign lab without session test\n")
