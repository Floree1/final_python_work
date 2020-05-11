#A las imagenes la tengo con su ruta de ubicación en la pc
#Las Lineas de las imagenes estan en 308 en adelante, estan la lineas agregadas en lineas de comentarios para cambiarle la ubicacion. 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import sqlite3
import time
import os

TIME_LIMIT = 100

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        self.setWindowTitle("Agregar estudiante")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Ingrese información del estudiante")
        self.setFixedWidth(350)
        self.setFixedHeight(400)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Apellido y Nombre")
        layout.addWidget(self.nameinput)

        self.documentoinput = QLineEdit()
        self.documentoinput.setPlaceholderText("D.N.I")
        layout.addWidget(self.documentoinput)

        
        self.colegioinput = QComboBox()
        self.colegioinput.addItem("Selecione Colegio")
        self.colegioinput.addItem("Colegio Concordia")
        self.colegioinput.addItem("Colegio Cristo Rey")
        self.colegioinput.addItem("Colegio Dante Alighieri")
        self.colegioinput.addItem("Colegio Hispano")
        self.colegioinput.addItem("Colegio Industrial")
        self.colegioinput.addItem("Colegio La Merced")
        self.colegioinput.addItem("Colegio Manuel Belgrano")
        self.colegioinput.addItem("Colegio Mercedes")
        self.colegioinput.addItem("Colegio Nacional")
        self.colegioinput.addItem("Colegio Normal")
        self.colegioinput.addItem("Colegio Nuestra Señora del Carmen")
        self.colegioinput.addItem("Colegio Primario Santa Eufrasia")
        self.colegioinput.addItem("Colegio San Ignacio")
        self.colegioinput.addItem("Colegio San Juan De La Cruz")
        self.colegioinput.addItem("Colegio Santa Eufrasia")
        self.colegioinput.addItem("Escuelas Pias")
        layout.addWidget(self.colegioinput)

        self.familiainput = QComboBox()
        self.familiainput.addItem("Seleccionar intengrantes del grupo familiar")
        self.familiainput.addItem("1")
        self.familiainput.addItem("2")
        self.familiainput.addItem("3")
        self.familiainput.addItem("4")
        self.familiainput.addItem("5")
        self.familiainput.addItem("6")
        self.familiainput.addItem("7")
        self.familiainput.addItem("8")
        layout.addWidget(self.familiainput)

        self.telefonoinput = QLineEdit()
        self.telefonoinput.setPlaceholderText("Telefono de emergencias")
        layout.addWidget(self.telefonoinput)

        self.direccioninput = QLineEdit()
        self.direccioninput.setPlaceholderText("Direccion")
        layout.addWidget(self.direccioninput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = ""
        documento = ""
        colegio = ""
        familia = -1
        telefono = ""
        direccion = ""


        name = self.nameinput.text()
        documento = self.documentoinput.text()
        colegio = self.colegioinput.itemText(self.colegioinput.currentIndex())
        familia = self.familiainput.itemText(self.familiainput.currentIndex())
        telefono = self.telefonoinput.text()
        direccion = self.direccioninput.text()
        
        try:
            self.conn = sqlite3.connect("alumnos.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO alumnos (name,documento,colegio,familia,telefono,direccion) VALUES (?,?,?,?,?,?)",(name,documento,colegio,familia,telefono,direccion))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Registro Exitoso','El estudiante se agrega con éxito a la base de datos.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se pudo agregar al alumno a la base de datos.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Buscar")

        self.setWindowTitle("Buscar Alumno")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("ID")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):

        searchrol = ""
        searchrol = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("alumnos.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from alumnos WHERE id="+str(searchrol))
            row = result.fetchone()
            serachresult = "ID : "+str(row[0])+'\n'+"Nombre Completo: "+str(row[1])+'\n'+"Documento: "+str(row[2])+'\n'+"Direccion: "+str(row[3])+'\n'+"Int. Grupo Familiar: "+ str(row[4])+' Persona/s'
            QMessageBox.information(QMessageBox(), 'Successful', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se pudo encontrar el alumno de la base de datos.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Eliminar")

        self.setWindowTitle("Eliminar Alumno")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("ID")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("alumnos.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from alumnos WHERE id="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Eliminado de la tabla con éxito')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'No se pudo eliminar al alumno de la base de datos.')

class LoginDialog(QDialog):
    
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(220)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.setWindowTitle('Registro de Alumnos')
        self.passinput.setPlaceholderText("Ingresar Key.(Por Defecto: 123456)")
        self.QBtn = QPushButton()
        self.QBtn.setText("Iniciar Sesión")
        self.QBtn.clicked.connect(self.login)


        title = QLabel("Hola, Colegio!")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        soporte = QLabel("*INFO:\nEste programa asigna a cada alumno su número de ID, por el cual cuando se necesite \nla infomación de un alumno solo con saber el ID que se le ortorgará\n\nSolicita la licencia en: ventas@gmail.com")
        font = soporte.font()
        font.setPointSize(9)
        soporte.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)
        layout.addWidget(soporte)

    def login(self):
        if(self.passinput.text() == "123456"):
        #if(self.passinput.text() == "9f3d4f1891c543bfbd9e64a91bfef0ca"):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Key Incorrecta\nSolicita tu key en RegistroAlumnos@gmail.com')



class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(390)
        self.setFixedHeight(350)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        self.setWindowTitle("Información del Desarrollador")
        title = QLabel("Registro de Alumnos en PyQt5")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('C:/Users/usuario/Desktop/RegistroAlumnos/icono/logo.png')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("Version 1.9\n\n"))
        layout.addWidget(QLabel("Partes de codigo sacados de Guias"))
        layout.addWidget(QLabel("Adaptados por Mauro Flores"))
        layout.addWidget(QLabel("Para uso personal - no comercial"))
        layout.addWidget(labelpic)


        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect("alumnos.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS alumnos(id INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,documento TEXT,colegio INTEGER,familia INTEGER,telefono TEXT,direccion TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&Registro")

        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("Registro de Alumnos")

        self.setMinimumSize(1200, 720)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("ID", "Apellido y Nombre", "DNI", "Colegio", "Integrantes familia", "Teléfono de Urgencias","Dirección"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/add.png"), "Agregar Alumno", self)
        #btn_ac_adduser = QAction(QIcon("icono/add.png"), "Agregar Alumno", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Agregar Alumno")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/refresh.png"),"Actualizar",self)
        #btn_ac_refresh = QAction(QIcon("icono/refresh.png"),"Actualizar",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Actualizar DB")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/search.png"), "Buscar", self)
        #btn_ac_search = QAction(QIcon("icono/search.png"), "Buscar", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Buscar Alumno")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/trash.png"), "Eliminar", self)
        #btn_ac_delete = QAction(QIcon("icono/trash.png"), "Eliminar", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Eliminar Alumno")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/add.png"),"Agregar Alumno", self)
        #adduser_action = QAction(QIcon("icono/add.png"),"Agregar Alumno", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/search.png"), "Buscar Alumno", self)
        #searchuser_action = QAction(QIcon("icono/search.png"), "Buscar Alumno", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/trash.png"), "Eliminar", self)
        #deluser_action = QAction(QIcon("icono/trash.png"), "Eliminar", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)


        about_action = QAction(QIcon("C:/Users/usuario/Desktop/RegistroAlumnos/icono/info.png"),"Desarrollador", self)
        #about_action = QAction(QIcon("icono/info.png"),"Desarrollador", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("alumnos.db")
        query = "SELECT * FROM alumnos"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()


app = QApplication(sys.argv)
passdlg = LoginDialog()


if(passdlg.exec_() == QDialog.Accepted):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())