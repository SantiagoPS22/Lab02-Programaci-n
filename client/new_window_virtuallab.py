import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QComboBox, QInputDialog
from PyQt5.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self, user_id, user_role):
        super().__init__()
        self.user_id = user_id
        self.user_role = user_role.lower() # "professor" o "student"
        
        self.setWindowTitle(f"Virtual Lab - Panel Principal (ID: {self.user_id}) - Rol: {self.user_role.capitalize()}")
        self.resize(450, 350)
        
        # Estilos QSS modernos
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f9;
            }
            QLabel {
                font-family: Arial;
                font-size: 14px;
                color: #333333;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Etiqueta de bienvenida con rol
        self.label = QLabel(f"Bienvenido al Laboratorio Virtual\nUsuario ID: {self.user_id} ({self.user_role.capitalize()})")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Funcionalidad según el rol
        if self.user_role == "professor":
            # Opciones exclusivas para el Profesor
            self.btn_subir = QPushButton("Subir Práctica de Laboratorio (.zip)")
            self.btn_subir.clicked.connect(self.subir_practica)
            layout.addWidget(self.btn_subir)

            self.btn_asignar = QPushButton("Asignar Laboratorio a Estudiante")
            self.btn_asignar.clicked.connect(self.asignar_laboratorio)
            layout.addWidget(self.btn_asignar)
        else:
            # Opción por defecto para Estudiante (Cargar archivo .cir)
            self.btn_accion = QPushButton("Cargar Archivo de Circuito (.cir)")
            self.btn_accion.clicked.connect(self.cargar_archivo_circuito)
            layout.addWidget(self.btn_accion)

        # Widget central obligatorio en QMainWindow
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def cargar_archivo_circuito(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo de Circuito",
            "",
            "Archivos de Circuito (*.cir)"
        )
        if file_name:
            QMessageBox.information(
                self,
                "Simulación de Laboratorio",
                f"¡Circuito cargado con éxito!\n\nArchivo:\n{file_name}"
            )

    def subir_practica(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Práctica en ZIP",
            "",
            "Archivos ZIP (*.zip)"
        )
        if file_name:
            # Aquí se conectaría la función uploadLab del servidor
            QMessageBox.information(
                self,
                "Éxito",
                f"Práctica seleccionada para subir:\n{file_name}\n(Función lista para conectar con uploadLab)"
            )

    def asignar_laboratorio(self):
        # Diálogo simple para simular la asignación usando listStudents y assignLab
        student_id, ok1 = QInputDialog.getText(self, "Asignar Laboratorio", "Ingrese el ID del Estudiante:")
        if ok1 and student_id:
            lab_name, ok2 = QInputDialog.getText(self, "Asignar Laboratorio", "Ingrese el nombre del archivo ZIP del laboratorio:")
            if ok2 and lab_name:
                # Aquí se conectaría con assignLab(self.user_id, lab_name, student_id)
                QMessageBox.information(
                    self,
                    "Asignación",
                    f"Laboratorio '{lab_name}' asignado al estudiante ID: {student_id}"
                )