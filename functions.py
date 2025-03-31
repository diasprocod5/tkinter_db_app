import re
from tkinter import *
from tkinter import ttk, messagebox
from database import Database
from table_data import table_data


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Application")
        self.geometry("1200x900")
        self.resizable(False, False)

        #---------------------- АТРИБУТЫ ____________________________________________________
        self.db = None
        self.table_data = table_data
        self.tariff_names = []
        self.current_table = None  # Текущая загруженная таблица
        self.current_columns = None  # Колонки текущей таблицы
        self.edit_mode = False  # Режим редактирования
#---------------------- frame    ----------------------------------------------------
        self.top_frame = Frame(self, bg='#e9edf5')
        self.top_frame.pack(fill=BOTH)

        self.home_frame = Frame(self,height=800, width=1100, bg='#e9edf5')

        self.log_frame = Frame(self,height=800, width=1100, bg='#e9edf5')

        self.query_frame = Frame(self,height=800, width=1100, bg='#e9edf5')




#---------------------- BUTTONS   ----------------------------------------------------

#---------------------- top_frame buttons -------------------------------------------

        self.btn_home_frame = Button(self.top_frame, text='Главная', font=12, command=lambda:self.frame_changer(self.home_frame))
        self.btn_home_frame.pack(side=LEFT, pady=20, padx=(40, 0), ipady=1, ipadx=40)

        self.btn_query_frame = Button(self.top_frame, text="Запросы", font=12, command=lambda:self.frame_changer(self.query_frame))
        self.btn_query_frame.pack(side=LEFT, pady=20, padx=(0, 0), ipady=1, ipadx=40)

        self.btn_add_window = Button(self.top_frame, text="Добавить", font=12, command=self.show_add_window)
        self.btn_add_window.pack(side=LEFT, pady=20, padx=(0, 0), ipady=1, ipadx=40)

        self.btn_update_window = Button(self.top_frame, text="Обновить", font=12)
        self.btn_update_window.pack(side=LEFT, pady=20, padx=(0, 0), ipady=1, ipadx=40)

        self.btn_delete_frame = Button(self.top_frame, text="Удалить", font=12)
        self.btn_delete_frame.pack(side=LEFT, pady=20, padx=(0, 0), ipady=1, ipadx=40)

        self.btn_log_frame = Button(self.top_frame, text='Авторизация', font=12, command=lambda:self.frame_changer(self.log_frame))
        self.btn_log_frame.pack(side=LEFT, pady=20, padx=(0, 0), ipady=1, ipadx=40)


#---------------------- log_frame button ----------------------------------------------
        self.btn_log_confirm = Button(self.log_frame, text='Вход/Выход', font=8, command=self.connect_db)
        self.btn_log_confirm.place(relx=0.5, rely=0.4, width=150, anchor=CENTER)
#--------------------- home_frame buttons ---------------------------------------------

        self.btn_show_general_data = Button(self.home_frame, text='Общие данные', command=lambda: self.load_data("general") )
        self.btn_show_general_data.place(x=10, y=20, width=200)

        self.btn_show_clients = Button(self.home_frame, text='Все клиенты', command=lambda: self.load_data("clients"))
        self.btn_show_clients.place(x=220, y=20, width=200)

        self.btn_show_debtors = Button(self.home_frame, text='Должники', command=lambda: self.load_data("debtors"))
        self.btn_show_debtors.place(x=430, y=20, width=200)

        self.btn_show_transactions = Button(self.home_frame, text='Транзакции',command=lambda: self.load_data("transactions"))
        self.btn_show_transactions.place(x=640, y=20, width=200)

        self.btn_show_tariffs = Button(self.home_frame, text='Тарифы', command=lambda: self.load_data("tariffs"))
        self.btn_show_tariffs.place(x=850, y=20, width=200)

        self.btn_new_clients = Button(self.home_frame, text="Новые клиенты", command=lambda: self.load_data("new_clients"))
        self.btn_new_clients.place(x=220, y=60, width=200)




#---------------------- ENTRIES -------------------------------------------------------

#---------------------- log_frame entries ---------------------------------------------
        self.login_entry = Entry(self.log_frame, font=16)
        self.login_entry.place(relx=0.5, rely=0.3, width=300, anchor=CENTER)

        self.pass_entry = Entry(self.log_frame, font=16, show='*')
        self.pass_entry.place(relx=0.5, rely=0.35, width=300, anchor=CENTER)


#------------------------ TABLES -------------------------------------------------------

#----------------------- home_frame table + scrollbar
        self.tree_container = Frame(self.home_frame)
        self.tree_container.place(x=50, y=120, height=650, width=1000)

        self.h_scrollbar = ttk.Scrollbar(self.tree_container, orient=HORIZONTAL)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)

        self.v_scrollbar = ttk.Scrollbar(self.tree_container, orient=VERTICAL)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(
            self.tree_container,
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set,
            selectmode=EXTENDED,
            style='Treeview'
        )
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        self.v_scrollbar.config(command=self.tree.yview)
        self.h_scrollbar.config(command=self.tree.xview)

        self.setup_treeview()

#------------------------- ADD_WINDOW ------------------------------


#------------------------ query_frame table + order_by group_by




#---------------------- МЕТОДЫ --------------------------------------------------------
    #----------------- методы окна добавить

    def show_add_window(self):


        # Инициализация окна
        self.add_window = Toplevel(self)
        self.add_window.title("add_data_page v2.04-05")
        self.add_window.geometry("500x400")
        self.add_window.resizable(False, False)

        # Основной контейнер
        main_frame = Frame(self.add_window)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Выбор таблицы
        table_frame = LabelFrame(main_frame, text="Добавить")
        table_frame.pack(fill=X, pady=5)

        self.selected_table = StringVar(value="clients")
        tables = [
            ("Клиент", "clients"),
            ("Тариф", "tariffs"),
            ("Аккаунт", "accounts"),
            ("Транзакция", "transactions")
        ]

        for text, value in tables:
            Radiobutton(table_frame, text=text, variable=self.selected_table,
                        value=value, command=self.update_input_fields).pack(side=LEFT, padx=5)

        # Поля ввода
        self.input_frame = LabelFrame(main_frame, text="Данные для добавления")
        self.input_frame.pack(fill=BOTH, expand=True, pady=5)

        # Кнопка добавления
        Button(main_frame, text="Добавить", command=self.add_data).pack(pady=5)

        # Инициализация полей
        self.update_input_fields()

    def update_input_fields(self):
        """Обновляет поля ввода для выбранной таблицы"""
        # Очистка предыдущих полей
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.input_fields = {}
        table_name = self.selected_table.get()

        # Конфигурация полей
        fields_config = {
            "clients": [
                ("ФИО*", "full_name", "entry", True),
                ("Телефон* (123 456 78 90)", "phone", "entry", True),
                ("Тип клиента*", "client_type", "combobox", True, ["private", "legal"], self.on_client_type_change),
                ("Инфо о компании", "company_info", "entry", False)
            ],
            "tariffs": [
                ("Название тарифа*", "tariff_name", "entry", True),
                ("Цена*", "tariff_price", "entry", True),
                ("Тип тарифа*", "tariff_type", "combobox", True, ["private", "legal"]),
                ("Описание*", "description", "entry", True)
            ],
            "accounts": [
                ("Телефон клиента* (123 456 78 90)", "phone", "entry", True),
                ("Название тарифа*", "tariff_name", "entry", True),
                ("Статус", "account_status", "combobox", False, ["active", "blocked"], "active"),
                ("Начальный баланс", "current_balance", "entry", False, "0.00"),
                ("Начальный долг", "current_debt", "entry", False, "0.00"),
                ("Дата платежа (YYYY-MM-DD)", "next_payment_date", "entry", False)
            ],
            "transactions": [
                ("Номер клиента*", "phone", "entry", True),
                ("Тип*", "transaction_type", "combobox", True, ["deposit", "debit"]),
                ("Сумма*", "amount", "entry", True)
            ]
        }

        # Создание полей
        for row, field in enumerate(fields_config.get(table_name, [])):
            label_text = field[0]
            field_name = field[1]
            field_type = field[2]
            required = field[3]

            Label(self.input_frame, text=label_text).grid(row=row, column=0, sticky=W, pady=2)

            if field_type == "combobox":
                widget = ttk.Combobox(self.input_frame, values=field[4], state="readonly")
                if len(field) > 5:  # Если есть обработчик изменения
                    widget.bind("<<ComboboxSelected>>", field[5])
            else:
                widget = Entry(self.input_frame)
                if len(field) > 4:  # Если есть значение по умолчанию
                    widget.insert(0, field[4])

            widget.grid(row=row, column=1, sticky=EW, pady=2, padx=5)
            self.input_fields[field_name] = (widget, required)

        # Настройка растягивания колонки с полями ввода
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Если это форма клиентов, вызываем обработчик для установки начального состояния
        if table_name == "clients":
            self.on_client_type_change()

    def on_client_type_change(self, event=None):
        """Обработчик изменения типа клиента"""
        if "client_type" not in self.input_fields or "company_info" not in self.input_fields:
            return

        client_type = self.input_fields["client_type"][0].get()
        company_info_widget = self.input_fields["company_info"][0]

        if client_type == "private":
            company_info_widget.config(state="disabled")
            company_info_widget.delete(0, END)
        else:
            company_info_widget.config(state="normal")

    def add_data(self):
        """Добавляет данные в БД с проверкой"""
        try:
            table_name = self.selected_table.get()
            data = {}
            errors = []

            # Проверка обязательных полей
            for field_name, (widget, required) in self.input_fields.items():
                value = widget.get()
                if required and not value:
                    errors.append(f"Поле '{field_name}' обязательно для заполнения")
                data[field_name] = value

            # Дополнительные проверки для клиентов
            if table_name == "clients":
                if not re.match(r'^\d{3}\s\d{3}\s\d{2}\s\d{2}$', data["phone"]):
                    errors.append("Телефон должен быть в формате: 123 456 78 90")

            if errors:
                messagebox.showwarning("Ошибка", "\n".join(errors))
                return

            # Подготовка параметров для каждой таблицы
            if table_name == "clients":
                query = """INSERT INTO clients 
                          (full_name, phone, client_type, company_info) 
                          VALUES (%s, %s, %s, %s)"""
                params = (
                    data["full_name"],
                    data["phone"],
                    data["client_type"],
                    data["company_info"] if data.get("company_info") else None
                )

            elif table_name == "tariffs":
                query = """INSERT INTO tariffs 
                          (tariff_name, tariff_price, tariff_type, description) 
                          VALUES (%s, %s, %s, %s)"""
                params = (
                    data["tariff_name"],
                    float(data["tariff_price"]),
                    data["tariff_type"],
                    data["description"]
                )

            elif table_name == "accounts":
                query = """INSERT INTO accounts 
                          (client_id, tariff_id, account_status, current_balance, current_debt, next_payment_date) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
                params = (
                    int(data["client_id"]),
                    int(data["tariff_id"]) if data.get("tariff_id") else None,
                    data["account_status"],
                    float(data.get("current_balance", "0.00")),
                    float(data.get("current_debt", "0.00")),
                    data.get("next_payment_date") or None
                )

            elif table_name == "transactions":
                query = """CALL add_transaction(%s, %s, %s)"""
                params = (
                    data["phone"],
                    data["transaction_type"],
                    float(data["amount"])
                )

            # Выполнение запроса
            self.db.open_cursor()
            self.db.execute_query(query, params)
            self.db.commit()

            messagebox.showinfo("Успех", "Данные успешно добавлены")
            self.add_window.destroy()

        except ValueError as e:
            self.db.rollback()
            messagebox.showerror("Ошибка", f"Некорректный формат данных: {str(e)}")
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Ошибка", f"Ошибка при добавлении: {str(e)}")
        finally:
            self.db.close_cursor()






   #----------------------------------------------------------------------------------------------------


    def get_tariffs(self):
        try:
            self.db.open_cursor()
            self.db.execute_query('SELECT tariff_name, tariff_type FROM tariffs ORDER BY tariff_name')
            all_tariffs = self.db.fetch_all()
            self.tariff_names = [tariff[0] for tariff in all_tariffs] or  []
            self.legal_tariffs = [tariff[0] for tariff in all_tariffs if tariff[1] == 'legal']
            self.private_tariffs = [tariff[0] for tariff in all_tariffs if tariff[1] == 'private']
            self.db.close_cursor()
        except Exception as e:
            messagebox.showerror(f"error :{e}")
            self.tariff_names =  []
        return self.tariff_names


    def frame_changer(self, frame): # Переключатель фреймов
        for item in {self.home_frame, self.query_frame, self.log_frame}:
            item.pack_forget()
        frame.pack(pady=10, padx=10)


    def connect_db(self): # подключение к БД
        user = self.login_entry.get()
        password = self.pass_entry.get()
        self.db = Database()
        if self.db.is_connected():
            self.db.disconnect()
            self.db = None
        else:
            self.db.connect(user,password)
            self.get_tariffs()

    def setup_treeview(self):
        self.tree.column('#0', width=0, stretch=NO)

        for col in self.tree['columns']:
            self.tree.heading(
                col,
                text=col,
                anchor=W,
                command=lambda c=col: self.treeview_sort_column(self.tree, c, False)
            )
            self.tree.column(col, anchor=W)

        # Добавляем обработчик двойного клика
        self.tree.bind("<Double-1>", self.show_record_details)

    def show_record_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id = selected_item[0]
        values = self.tree.item(item_id, 'values')
        columns = self.tree['columns']

        # Получаем реальные имена колонок из table_data
        table_info = self.table_data.get(self.current_table, {})
        db_columns = table_info.get('columns', [])
        display_columns = table_info.get('display_columns', [])

        # Создаем модальное окно
        self.details_window = Toplevel(self)
        self.details_window.title("Детали записи")
        self.details_window.geometry("600x500")
        self.details_window.resizable(False, False)
        self.details_window.grab_set()  # Делаем окно модальным

        # Основной контейнер
        main_frame = Frame(self.details_window)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Поля для отображения данных
        self.detail_fields = {}
        for i, (col, val) in enumerate(zip(columns, values)):
            Label(main_frame, text=col).grid(row=i, column=0, sticky=W, pady=5)

            # Определяем тип поля (entry/combobox) на основе таблицы
            if self.current_table == "clients" and col == "client_type":
                entry = ttk.Combobox(main_frame, values=["private", "legal"], state="readonly")
                entry.set(val)
            elif self.current_table == "tariffs" and col == "tariff_type":
                entry = ttk.Combobox(main_frame, values=["private", "legal"], state="readonly")
                entry.set(val)
            else:
                entry = Entry(main_frame)
                entry.insert(0, val)

            entry.config(state='readonly')
            entry.grid(row=i, column=1, sticky=EW, pady=5, padx=5)
            self.detail_fields[col] = entry

        # Фрейм для кнопок
        button_frame = Frame(main_frame)
        button_frame.grid(row=len(columns) + 1, columnspan=2, pady=10)

        # Кнопки управления
        self.btn_edit = Button(button_frame, text="Изменить", command=lambda: self.toggle_edit_mode(item_id))
        self.btn_edit.pack(side=LEFT, padx=5)

        self.btn_delete = Button(button_frame, text="Удалить", command=lambda: self.delete_record(item_id))
        self.btn_delete.pack(side=LEFT, padx=5)

        self.btn_cancel = Button(button_frame, text="Отменить", command=self.details_window.destroy)
        self.btn_cancel.pack(side=LEFT, padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def cancel_edit_mode(self, item_id):
        """Отменяет режим редактирования"""
        self.edit_mode = False
        self.btn_edit.config(text="Изменить")

        # Восстанавливаем исходные значения
        values = self.tree.item(item_id, 'values')
        for col, entry in zip(self.tree['columns'], self.detail_fields.values()):
            entry.delete(0, END)
            entry.insert(0, values[self.tree['columns'].index(col)])
            entry.config(state='readonly')

    def save_record_changes(self, item_id):
        try:
            updated_data = {}
            for col, entry in self.detail_fields.items():
                updated_data[col] = entry.get()
                entry.config(state='readonly')

            # Определяем таблицу для обновления
            table_name = self.current_table

            if table_name == "clients":
                query = "UPDATE clients SET full_name = %s, phone = %s WHERE client_id = %s"
                params = (updated_data['Name'], updated_data['Phone'], item_id)
            elif table_name == "tariffs":
                query = "UPDATE tariffs SET tariff_name = %s, tariff_price = %s WHERE tariff_id = %s"
                params = (updated_data['Name'], updated_data['Price'], item_id)
            # Добавьте другие таблицы по аналогии

            self.db.execute_query(query, params)
            self.db.commit()

            messagebox.showinfo("Успех", "Изменения сохранены")
            # ... остальной код
            self.edit_mode = False
            self.btn_edit.config(text="Изменить")

            # Обновляем данные в таблице
            self.load_data(self.current_table)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {str(e)}")
            self.cancel_edit_mode(item_id)

    def delete_record(self, item_id):
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить запись?"):
            return

        try:
            table_name = self.current_table

            if table_name == "clients":
                query = "DELETE FROM clients WHERE client_id = %s"
            elif table_name == "tariffs":
                query = "DELETE FROM tariffs WHERE tariff_id = %s"
            # Добавьте другие таблицы по аналогии

            self.db.execute_query(query, (item_id,))
            self.db.commit()

            messagebox.showinfo("Успех", "Запись удалена")
            # ... остальной код
            self.details_window.destroy()
            self.load_data(self.current_table)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")




    def toggle_edit_mode(self, item_id):
        """Переключает режим редактирования"""
        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            # Включаем редактирование
            self.btn_edit.config(text="Подтвердить")
            for entry in self.detail_fields.values():
                entry.config(state='normal')
        else:
            # Отключаем редактирование и сохраняем изменения
            if messagebox.askyesno("Подтверждение", "Сохранить изменения?"):
                self.save_record_changes(item_id)
            else:
                # Отменяем изменения
                self.cancel_edit_mode(item_id)

    def treeview_sort_column(self, tv, col, reverse):

        l = [(tv.set(k, col), k) for k in tv.get_children('')]

        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def load_data(self, table_name):
        """Загружает данные в таблицу с сохранением информации о текущей таблице"""
        self.current_table = table_name
        table_info = self.table_data[table_name]
        query = table_info['query']
        self.current_columns = table_info['columns']
        display_columns = table_info['display_columns']
        column_widths = table_info['column_widths']

        self.tree.delete(*self.tree.get_children())

        if self.tree['columns'] != display_columns:
            self.tree['columns'] = display_columns
            for col in display_columns:
                self.tree.heading(
                    col,
                    text=col,
                    anchor=W,
                    command=lambda c=col: self.treeview_sort_column(self.tree, c, False)
                )
                self.tree.column(col, anchor=W, width=column_widths.get(col, 100))

        self.db.open_cursor()
        self.db.execute_query(query)
        rows = self.db.fetch_all()

        for row in rows:
            display_values = row[1:] if len(row) == len(self.current_columns) else row
            self.tree.insert('', 'end', values=display_values, iid=row[0])

        self.db.close_cursor()
        self.update_scrollbars()

    def update_scrollbars(self):
        self.tree.update_idletasks()

        bbox = self.tree.bbox("", 0)
        if bbox:
            total_width = sum(self.tree.column(col)['width'] for col in self.tree['columns'])
            if total_width > self.tree.winfo_width():
                self.h_scrollbar.pack(side=BOTTOM,fill=X)

        if len(self.tree.get_children()) > 0:
            item_height =self.tree.bbox(self.tree.get_children()[0])[3]
            visible_height = self.tree.winfo_height()
            if len(self.tree.get_children()) * item_height > visible_height:
                self.v_scrollbar.pack(side=RIGHT, fill=Y)
            else:
                self.v_scrollbar.pack_forget()




#----------------------------------------------------------------------------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        """Показать подсказку"""
        if self.tip_window or not self.text:
            return

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        """Скрыть подсказку"""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None





#-----------------------------------------------------------------------------------


if __name__=='__main__':
    app = App()
    app.mainloop()

