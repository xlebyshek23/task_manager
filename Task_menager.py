
import sys
import time
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QTextEdit,
                             QLabel, QListWidgetItem, QMessageBox,)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.red = QColor()
        self.red.setRed(255)
        self.tasks_list = QListWidget(self)
        self.button_all_tasks = QPushButton("Все задачи", self)
        self.button_active_tasks = QPushButton("Активные задачи", self)
        self.button_done_tasks = QPushButton("Выполненные задачи", self)
        self.task_name = QLineEdit(self)
        self.task_description = QTextEdit(self)
        self.button_add_task = QPushButton("Добавить задачу", self)
        self.button_edit_task = QPushButton("Изменить задачу", self)
        self.button_delete_task = QPushButton("Удалить задачу", self)
        self.categories_list = QListWidget(self)
        self.category_name = QLineEdit(self)
        self.button_add_category = QPushButton("Добавить категорию", self)
        self.button_edit_category = QPushButton("Изменить категорию", self)
        self.button_delete_category = QPushButton("Удалить категорию", self)
        self.time_hour = QLineEdit(self)
        self.time_min = QLineEdit(self)

        self.tasks_list.itemClicked.connect(self.task_detail)
        self.tasks_list.itemDoubleClicked.connect(self.change_statuse)
        self.categories_list.itemClicked.connect(self.category_detail)
        self.button_delete_task.clicked.connect(self.delete_task)
        self.button_delete_category.clicked.connect(self.delete_category)
        self.button_add_category.clicked.connect(self.add_category)
        self.button_add_task.clicked.connect(self.add_task)
        self.button_edit_task.clicked.connect(self.edit_task)
        self.button_edit_category.clicked.connect(self.edit_category)
        self.button_all_tasks.clicked.connect(self.load_tasks)
        self.button_active_tasks.clicked.connect(self.acctive_task)
        self.button_done_tasks.clicked.connect(self.done_task)

        self.init_ui()

        self.create_db()
        self.load_tasks()
        self.load_categories()



    def init_ui(self):
        self.resize(400, 500)
        self.setWindowTitle("Менеджер задач")
        icon = QIcon()
        icon.addPixmap(QPixmap("icon.png"), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        vbox = QVBoxLayout()
        self.name1 = QLabel('Список задач:', self)
        vbox.addWidget(self.name1)
        vbox.addWidget(self.tasks_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_all_tasks)
        hbox.addWidget(self.button_active_tasks)
        hbox.addWidget(self.button_done_tasks)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name2 = QLabel('Название задачи:', self)
        hbox.addWidget(self.name2)
        hbox.addWidget(self.task_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name3 = QLabel('Описание задачи:', self)
        hbox.addWidget(self.name3)
        hbox.addWidget(self.task_description)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name4 = QLabel('Категория:', self)
        hbox.addWidget(self.name4)
        hbox.addWidget(self.category_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name6 = QLabel('Время выполнения:', self)
        self.name7 = QLabel('часов', self)
        self.name8 = QLabel('минут:', self)
        hbox.addWidget(self.name6)
        hbox.addWidget(self.time_hour)
        hbox.addWidget(self.name7)
        hbox.addWidget(self.time_min)
        hbox.addWidget(self.name8)
        vbox.addLayout(hbox)
        self.name5 = QLabel('Список категорий:', self)
        vbox.addWidget(self.name5)
        vbox.addWidget(self.categories_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_task)
        hbox.addWidget(self.button_edit_task)
        hbox.addWidget(self.button_delete_task)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_category)
        hbox.addWidget(self.button_edit_category)
        hbox.addWidget(self.button_delete_category)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def create_db(self):
        query = QSqlQuery()
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
            );
            """
        )
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            active BOOL NOT NULL DEFAULT TRUE,
            category_id INTEGER,
            time_sek INTEGER,
            date_start INTEGER,
            date_end INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
            );
            """
        )

    def load_tasks(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories 
            ON category_id=categories.id;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                if i == 5:
                    if query.value(3) == 1:
                        if query.value(7)-time.time()>0:
                            temp.append(query.value(7)-time.time())
                        else:
                            temp.append(0)
                    else:
                        temp.append(0)
                else:
                    temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))
            if int(task[5])<=0 and task[3] == 1:
                self.tasks_list.item(len(self.tasks_list)-1).setForeground(self.red)

    def load_categories(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM categories;""")
        self.categories = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                temp.append(query.value(i))
            self.categories.append(temp)
        print(self.categories)
        self.categories_list.clear()
        for category in self.categories:
            self.categories_list.addItem(QListWidgetItem(category[1]))

    def add_task(self):
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        row = self.categories_list.currentRow()
        category_id = self.categories[row][0]
        time_h = self.time_hour.text()
        time_m = self.time_min.text()
        try:
            time_h = int(time_h)
            time_m = int(time_m)
        except (ValueError):
            b = False
        else:
            b = True
        if b is True:
            time_s = int(time_m) * 60 + int(time_h) * 3600
            if time_s > 0 and name.strip() != "" and category_id != "":
                date_s = time.time()
                date_e = time.time() + time_s
                time_m = int(time_m)
                time_h = int(time_h)
                time_h += time_m//60
                time_m = time_m % 60
                print(time_m)
                query = QSqlQuery()
                query.exec(
                    f"""INSERT INTO tasks (name, description, category_id, time_sek, date_start, date_end) 
                    VALUES ('{name}', '{description}', '{category_id}', '{time_s}', '{date_s}', {date_e});"""
                )
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("Неправильно создана задача.")
                message_box.setWindowTitle("Не удалось создать задачу")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.show()
                result = message_box.exec()

        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("Неправильно создана задача.")
            message_box.setWindowTitle("Не удалось создать задачу")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.show()
            result = message_box.exec()
        self.load_tasks()

    def add_category(self):
        name = self.category_name.text()
        if name.strip() != "" and name != "":
            query = QSqlQuery()
            query.exec(
                f"""INSERT INTO categories (name) 
                VALUES ('{name}');"""
            )
        else:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("Неправильно создана категория.")
            message_box.setWindowTitle("Не удалось создать категория")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.show()
            result = message_box.exec()
        self.load_categories()

    def task_detail(self):
        row = self.tasks_list.currentRow()
        self.task_name.setText(self.tasks[row][1])
        self.task_description.setText(self.tasks[row][2])
        self.category_name.setText(self.tasks[row][9])
        if self.tasks[row][5] > 0:
            self.time_hour.setText(str(int(self.tasks[row][5]//3600)))
            self.time_min.setText(str(int(self.tasks[row][5] % 3600//60)))
        else:
            self.time_hour.setText("0")
            self.time_min.setText("0")
    def category_detail(self):
        row = self.categories_list.currentRow()
        self.category_name.setText(self.categories[row][1])

    def delete_task(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите удалить задачу: {self.tasks[row][1]}?")
        message_box.setWindowTitle("Удалить задачу?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(
                f"""DELETE FROM tasks 
                   WHERE id={task_id};"""
            )
            self.load_tasks()

    def delete_category(self):
        row = self.categories_list.currentRow()
        cat_id = self.categories[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите удалить категорию: {self.categories[row][1]}?")
        message_box.setWindowTitle("Удалить категорию?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(
                f"""DELETE FROM categories
                           WHERE id={cat_id};"""
            )
            self.load_categories()

    def edit_category(self):
        row = self.categories_list.currentRow()
        cat_id = self.categories[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите удалить категорию: {self.categories[row][1]}?")
        message_box.setWindowTitle("Удалить категорию?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            name = self.category_name.text()
            if name.strip() != "":
                query = QSqlQuery()
                query.exec(
                    f"""DELETE FROM categories
                                       WHERE id={cat_id};"""
                )
                query = QSqlQuery()
                query.exec(
                    f"""INSERT INTO categories (name) 
                            VALUES ('{name}');"""
                )
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("Неправильно изменена категория.")
                message_box.setWindowTitle("Не удалось изменить категорию")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.show()
                result = message_box.exec()
            self.load_categories()

    def edit_task(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите изменить задачу: {self.tasks[row][1]}?")
        message_box.setWindowTitle("Изменить задачу?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            time_sk = self.tasks[row][5]
            date_st = self.tasks[row][6]
            date_en =self.tasks[row][7]
            name = self.task_name.text()
            if name.strip() != "":
                query = QSqlQuery()
                query.exec(
                    f"""DELETE FROM tasks 
                               WHERE id={task_id};"""
                )

                description = self.task_description.toPlainText()
                row = self.categories_list.currentRow()
                category_id = self.categories[row][0]
                query = QSqlQuery()
                query.exec(
                    f"""INSERT INTO tasks (name, description, category_id, time_sek, date_start, date_end) 
                            VALUES ('{name}', '{description}', '{category_id}', '{time_sk}', '{date_st}', {date_en});"""
                )
            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setText("Неправильно изменена задача.")
                message_box.setWindowTitle("Не удалось изменить категория")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.show()
                result = message_box.exec()
            self.load_tasks()
    def acctive_task(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories 
            ON category_id=categories.id WHERE active == 1;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                if i == 5:
                    if query.value(3) == True:
                        if query.value(7) - time.time() > 0:
                            temp.append(query.value(7) - time.time())
                        else:
                            temp.append(0)
                else:
                    temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))
            if int(task[5]) <= 0:
                self.tasks_list.item(len(self.tasks_list) - 1).setForeground(self.red)


    def done_task(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories 
            ON category_id=categories.id WHERE active == 0;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                if i == 5:
                    temp.append(0)
                else:
                    temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))


    def change_statuse(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Хотите сделать задачу выполненной: {self.tasks[row][1]}?")
        message_box.setWindowTitle("Изменить статус задачи?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(
                f"""UPDATE tasks SET active = 0 WHERE id={task_id};""")
            self.load_tasks()

if __name__ == '__main__':
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("tasks.sqlite")

    if not con.open():
        print("Database Error: %s" % con.lastError().databaseText())
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
