from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from new_window_virtuallab import NewWindow
from virtuallab_client import *

# Program demonstrating a simple login interface for the virtual lab project. 
# Make sure you run the server first (virtuallab_server.py).
# Alexander López Parrado, 2026


# Main window class inheriting from QMainWindow
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Lab - Login")
        
        # Estilos modernos para la interfaz
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                font-weight: bold;
            }
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QComboBox {
                padding: 6px;
                font-size: 14px;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
       
        # Labels are created
        l1 = QLabel('Nombre: ')
        l2 = QLabel('ID: ')
        l3 = QLabel('Rol: ')
        l4 = QLabel('Contraseña: ')

        # Edit fields are created
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()

        # Combo box to select between "Profesor" and "Estudiante" roles
        self.combo = QComboBox()      
        options = ["Profesor", "Estudiante"]
        self.combo.addItems(options)

        # Password field is created 
        self.e4 = QLineEdit()
        self.e4.setEchoMode(QLineEdit.Password)

        # Registration and login buttons are created
        b1 = QPushButton('Registrarse')
        b1.clicked.connect(self.registerUser)
        b2 = QPushButton('Iniciar sesión')
        b2.clicked.connect(self.openSession)
        
        # We're using a grid layout to arrange the widgets in a grid format
        gridLayout = QGridLayout()
        
        # Widgets are added to the grid layout at specified row and column positions
        gridLayout.addWidget(l1, 0, 0)
        gridLayout.addWidget(l2, 1, 0)
        gridLayout.addWidget(l3, 2, 0)
        gridLayout.addWidget(l4, 3, 0)
        
        gridLayout.addWidget(self.e1, 0, 1)
        gridLayout.addWidget(self.e2, 1, 1)
        gridLayout.addWidget(self.combo, 2, 1)
        gridLayout.addWidget(self.e4, 3, 1)

        gridLayout.addWidget(b1, 4, 0)
        gridLayout.addWidget(b2, 4, 1)

        # Central widget is created and the grid layout is set to it. QMainWindow requires a central widget.
        widget = QWidget()
        widget.setLayout(gridLayout)        
        self.setCentralWidget(widget)
        
        # Maximizing is disabled
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

    # Slot function to handle user registration
    def registerUser(self):
        name = self.e1.text()
        id = self.e2.text()
        role = self.combo.currentText()
        password = self.e4.text()
        
        if len(id) and len(password) and len(name):
            url = "http://127.0.0.1:80"
            response = registerUser(url, name, id, role, password)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(str(response))
            msgBox.setWindowTitle("Registro")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Por favor ingresar toda la información")
            msgBox.setWindowTitle("Alerta")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
     
   # Slot function to handle user login
    def openSession(self):
        name = self.e1.text()
        id = self.e2.text()
        role = self.combo.currentText()
        password = self.e4.text()
        
        if len(id) and len(password) and len(name):
            url = "http://127.0.0.1:80"
            response = openSession(url, id, password)
            print(response)        
            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(str(response))
            msgBox.setWindowTitle("Respuesta del Servidor")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            
            # Si el inicio de sesión fue exitoso, abrimos la ventana pasando el ID y el Rol mapeado
            if response == "Session was succesfully opened":
                mapped_role = "professor" if role.lower() in ["profesor", "professor"] else "student"
                self.nw = NewWindow(id, mapped_role)
                self.nw.show()
                self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Por favor ingresar toda la información")
            msgBox.setWindowTitle("Alerta")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

# Creating an instance of the main window and showing it
app = QApplication([])
ex = MainWindow()
ex.show()
app.exec()