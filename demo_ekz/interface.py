from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo
import psycopg2
from psycopg2.extensions import register_type, UNICODE

CONN_STR = "host='#.#.#.#' dbname='#' user='#' password='#'"

FONT = ("Arial", 18)

'''
Основной класс приложения
'''


class tkinterApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for page in (startPage, page_teachers, page_teachers_add, page_teachers_view, page_teachers_update_city,
                     page_teachers_delete):
            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(startPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


'''
Класс, отвечающий за окно с начальным меню
'''


class startPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label_start = Label(self, text='База данных университета',
                            fg='black', font=("Arial", 40, 'bold'))

        but_1 = ttk.Button(self, text='База данных учителей', style='normal.TButton',
                           command=lambda: controller.show_frame(page_teachers))

        label_start.place(x=145, y=100,
                          width=1000, height=110)
        but_1.place(x=460, y=340,
                    width=370, height=90)


'''
Класс, отвечающий за окно с выбором действия над клинтами в базе
'''


class page_teachers(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # создание кнопок и надписей
        label_start = Label(self, text='База данных учителей',
                            fg='black', font=("Arial", 40, 'bold'))

        but_1 = ttk.Button(self, text='Открыть базу данных учителей', style='normal.TButton',
                           command=lambda: controller.show_frame(page_teachers_view))
        but_2 = ttk.Button(self, text='Добавить учителя', style='normal.TButton',
                           command=lambda: controller.show_frame(page_teachers_add))
        but_3 = ttk.Button(self, text='Обновить город учителя', style='normal.TButton',
                           command=lambda: controller.show_frame(page_teachers_update_city))
        but_4 = ttk.Button(self, text='Удалить учителя из базы данных', style='normal.TButton',
                           command=lambda: controller.show_frame(page_teachers_delete))
        but_back = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(startPage))

        # размещение кнопок и надписей
        label_start.place(x=145, y=100,
                          width=1000, height=110)
        but_1.place(x=420, y=300,
                    width=450, height=90)
        but_2.place(x=420, y=400,
                    width=450, height=90)
        but_3.place(x=420, y=500,
                    width=450, height=90)
        but_4.place(x=420, y=600,
                    width=450, height=90)
        but_back.place(x=80, y=610,
                       width=200, height=70)


'''
Класс, отвечающий за окно с выводом базы клиентов
'''


class page_teachers_view(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        label = ttk.Label(self, text="База данных учителей", font=('Arial', 23, 'bold'), anchor='center')
        label.grid(row=0, column=0, padx=200, pady=25)

        self.printDB()
        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_teachers))
        but_menu.grid(row=2, column=0, ipadx=20, ipady=10, padx=50, pady=50)

    def print_teachers(self, people):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select * from teachers')
        cols = cur.description
        row = cur.fetchone()
        k = 1
        while row:  # 0 4 7
            st = [k]
            for i in range(len(cols)):
                st.append(row[i])
            people.append(st)
            row = cur.fetchone()
            k += 1
        cur.close()
        conn.close()
        return people

    '''
    Вывод сохраненных клиентов в виде таблице
    '''

    def printDB(self):
        people = self.print_teachers([])
        self.tree = ttk.Treeview(self, columns=['number', 'sname', 'faname', 'caf', 'staj', 'town'],
                                 height=25, show='headings', style='normal.Treeview')
        self.tree.column('number', width=40, anchor=CENTER)
        self.tree.column('sname', width=100, anchor=CENTER)
        self.tree.column('faname', width=260, anchor=CENTER)
        self.tree.column('caf', width=150, anchor=CENTER)
        self.tree.column('staj', width=150, anchor=CENTER)
        self.tree.column('town', width=200, anchor=CENTER)
        self.tree.heading('number', text='№')
        self.tree.heading('sname', text='Имя')
        self.tree.heading('faname', text='Отчество')
        self.tree.heading('caf', text='Кафедра')
        self.tree.heading('staj', text='Стаж')
        self.tree.heading('town', text='Город')
        self.tree.grid(row=1, column=0, padx=250)

        for person in people:
            self.tree.insert('', END, values=person)


'''
Класс, отвечающий за окно с вводом клинтов в базу
'''


class page_teachers_add(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):

        labl = ttk.Label(self, text='Добавление учителя в базу', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=0, pady=100, padx=70)

        labl_4 = ttk.Label(self, text='Введите имя', font=FONT)
        labl_4.grid(row=1, column=0, sticky='w', padx=145, pady=10)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_5 = ttk.Label(self, text='Введите отчетсво', font=FONT)
        labl_5.grid(row=3, column=0, sticky='w', padx=145, pady=10)
        self.ent_5 = ttk.Entry(self, font=FONT)
        self.ent_5.grid(row=4, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_6 = ttk.Label(self, text='Введите кафедру', font=FONT)
        labl_6.grid(row=1, column=1, sticky='w', padx=145, pady=10)
        self.ent_6 = ttk.Entry(self, font=FONT)
        self.ent_6.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_8 = ttk.Label(self, text='Введите стаж', font=FONT)
        labl_8.grid(row=3, column=1, sticky='w', padx=145, pady=10)
        self.ent_8 = ttk.Entry(self, font=FONT)
        self.ent_8.grid(row=4, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_9 = ttk.Label(self, text='Введите город', font=FONT)
        labl_9.grid(row=5, column=1, sticky='w', padx=145, pady=10)
        self.ent_9 = ttk.Entry(self, font=FONT)
        self.ent_9.grid(row=6, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        but_check = ttk.Button(self, text="Добавить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=7, column=1, ipadx=140, ipady=20, padx=145, pady=20)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_teachers))
        but_menu.grid(row=7, column=0, ipadx=20, ipady=10, padx=50)

    def add_teacher(sname, faname, caf, staj, town):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('add_teacher', [sname, faname, caf, staj, town])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if all([self.ent_4.get() != '',
                self.ent_5.get() != '',
                self.ent_6.get() != '',
                self.ent_8.get() != '',
                self.ent_9.get() != '']):
            self.add_teacher(self.ent_4.get(), self.ent_6.get(), self.ent_8.get())
            showinfo(title="Информация", message="Успешно! Учитель записан в базу данных!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
            self.ent_5.delete(0, END)
            self.ent_5.insert(0, '')
            self.ent_6.delete(0, END)
            self.ent_6.insert(0, '')
            self.ent_8.delete(0, END)
            self.ent_8.insert(0, '')
            self.ent_9.delete(0, END)
            self.ent_9.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


'''
Класс, отвечающий за окно с обновлением города клиента в базе
'''


class page_teachers_update_city(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        labl = ttk.Label(self, text='Обновление города учителя в базе', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=1, pady=100, padx=90)

        labl_4 = ttk.Label(self, text='Введите имя', font=FONT)
        labl_4.grid(row=1, column=1, sticky='w', padx=145, pady=20)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_3 = ttk.Label(self, text='Введите отчество', font=FONT)
        labl_3.grid(row=3, column=1, sticky='w', padx=145, pady=20)
        self.ent_3 = ttk.Entry(self, font=FONT)
        self.ent_3.grid(row=4, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_5 = ttk.Label(self, text='Введите новый город', font=FONT)
        labl_5.grid(row=5, column=1, sticky='w', padx=145)
        self.ent_5 = ttk.Entry(self, font=FONT)
        self.ent_5.grid(row=6, column=1, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        but_check = ttk.Button(self, text="Обновить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=7, column=1, ipadx=140, ipady=20, pady=10)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_teachers))
        but_menu.grid(row=7, column=0, ipadx=20, ipady=10, padx=50, pady=70)

    def change_city(sname, faname, new_city):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('update_teacher', [new_city, sname, faname])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if all([self.ent_4.get() != '',
                self.ent_3.get() != '',
                self.ent_5.get() != '']):
            self.change_city(self.ent_4.get(), self.ent_3.get(), self.ent_5.get())
            showinfo(title="Информация", message="Успешно! Информация обновлена!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
            self.ent_3.delete(0, END)
            self.ent_3.insert(0, '')
            self.ent_5.delete(0, END)
            self.ent_5.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


'''
Класс, отвечающий за окно с удалением клиентов из базу
'''


class page_teachers_delete(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        labl = ttk.Label(self, text='Удаление учителя из базы', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=1, pady=150, padx=100)

        labl_4 = ttk.Label(self, text='Введите имя', font=FONT)
        labl_4.grid(row=1, column=1, sticky='w', padx=125)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10, padx=125, pady=20)

        labl_5 = ttk.Label(self, text='Введите отчество', font=FONT)
        labl_5.grid(row=3, column=1, sticky='w', padx=125)
        self.ent_5 = ttk.Entry(self, font=FONT)
        self.ent_5.grid(row=4, column=1, sticky='w', ipadx=100, ipady=10, padx=125, pady=20)

        but_check = ttk.Button(self, text="Удалить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=5, column=1, ipadx=140, ipady=20, pady=10)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_teachers))
        but_menu.grid(row=5, column=0, ipadx=20, ipady=10, padx=50, pady=70)

    def delete_teacher(sname, faname):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('delete_teacher', [sname, faname])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if all([self.ent_4.get() != '',
                self.ent_4.get() != '']):
            self.delete_teacher(self.ent_4.get(), self.ent_5.get())
            showinfo(title="Информация", message="Успешно! Учитель удален из базы данных!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
            self.ent_5.delete(0, END)
            self.ent_5.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


app = tkinterApp()
app.title("База данных университета")
app.geometry('1300x800+300+100')
app.resizable(False, False)
style = ttk.Style()
style.configure('normal.Treeview', font=('Arial', 12))
style.configure('normal.TButton', font=('Arial', 20))
app.mainloop()