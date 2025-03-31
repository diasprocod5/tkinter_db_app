from tkinter import *
from tkinter import ttk, messagebox
from table_data import table_data
from database import Database

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Oh shit! Here we again")
        self.geometry('900x600')
        self.minsize(600, 400)
        self.resizable(False, False)

        self.db = None
        self.id_name_phone = dict()
        self.clients_without_accounts = dict() # client_id, fullname, phone, client_type
        self.actual_tariffs = dict() # tariff_id ,tariff_name, tariff_type
        self.table_data = table_data



        self.top_frame =  Frame(self, height=100,bg='#f2dec2')
        self.top_frame.pack(fill=BOTH,ipady=3)

        self.main_frame = Frame(self, bg='blue')
        self.main_frame.pack(fill=BOTH, expand=True)

        self.query_frame = Frame(self, bg='red')

        self.frame_list = (self.main_frame, self.query_frame)

        self.query_text = Text(self.query_frame)
        self.query_frame.pack(padx=10,pady=10)







#---------------------------------------------------- LOGIN -------------------------
        self.btn_log = Button(self.top_frame, width=10, bg='#f2dec2', text='Вход', command=self.connection)
        self.btn_log.pack(side=RIGHT, padx=5)
#-----------------------------------------------------TOP FRAME BUTTONS-------------------------------
        self.btn_home = Button(self.top_frame,width=10,bg='#f2dec2', text='Таблицы', command=lambda :self.frame_packer(self.main_frame))
        self.btn_home.pack(side=LEFT,padx=5)
#---------------------------
        self.btn_add_new = Button(self.top_frame,width=10,bg='#f2dec2', text='Добавить', command=self.show_add_menu)
        self.btn_add_new.pack(side=LEFT, padx=5)

        self.btn_query_tool = Button(self.top_frame,width=10,bg='#f2dec2', text='QueryTool', command=lambda :self.frame_packer(self.query_frame))
        self.btn_query_tool.pack(side=LEFT, padx=5)

        self.add_menu = Menu(self, tearoff=0)
        self.add_menu.add_command(label="Клиенты", command=self.open_add_client_window)
        self.add_menu.add_command(label="Тарифы", command=self.open_add_tariff_window)
        self.add_menu.add_command(label="Счета", command=self.open_add_account_window)
        self.add_menu.add_command(label="Транзакции", command=self.open_add_transaction_window)

#--------------------------------------------------QUERY TOOL------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- TREEVIEW -------------------------------------
#------------------------------------------------- TREEVIEW BUTTONS --------------------------------------
        self.btn_clients = Button(self.main_frame, text='Клиенты', command=lambda:self.load_data('clients'))
        self.btn_clients.place(x=50,y=20, width=100)
        self.btn_tariffs = Button(self.main_frame, text='Тарифы', command=lambda: self.load_data('tariffs'))
        self.btn_tariffs.place(x=160, y=20, width=100)
        self.btn_trans = Button(self.main_frame, text='Транзакции', command=lambda: self.load_data('transactions'))
        self.btn_trans.place(x=270, y=20, width=100)
#-------------------------------------------------------------------------------------------------------

        self.treeview_frame = Frame(self.main_frame)
        self.treeview_frame.pack(fill=BOTH, expand=True, padx=10, pady=(60, 10))

        self.scrollbar_v = ttk.Scrollbar(self.treeview_frame,orient=VERTICAL)
        self.scrollbar_v.pack(side=RIGHT, fill=Y)

        self.scrollbar_h = ttk.Scrollbar(self.treeview_frame, orient=HORIZONTAL)
        self.scrollbar_h.pack(side=BOTTOM,fill=X)

        self.tree = ttk.Treeview(
            self.treeview_frame,
            yscrollcommand=self.scrollbar_v.set,
            xscrollcommand=self.scrollbar_h.set,
            selectmode=EXTENDED
        )
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar_v.config(command=self.tree.yview)
        self.scrollbar_h.config(command=self.tree.xview)


#----------------------------------------------- Functions -------------------------------------

    def frame_packer(self, cur_frame):
        for frame in self.frame_list:
            if frame != cur_frame:
                frame.pack_forget()
            else:
                frame.pack(fill=BOTH, expand=True)



    def load_data(self, table_name):
        self.tree.delete(*self.tree.get_children()) # clear table treeview\

        #take data from table_data dict
        table_info = self.table_data[table_name]
        query = table_info["query"]
        columns = table_info["columns"]
        display_columns = table_info["display_columns"]
        column_widths = table_info["column_widths"]


        self.tree["columns"]= display_columns
        for col in display_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 150), stretch=False)

        self.tree.column("#0", width=0,stretch=NO)

        self.db.open_cursor()
        self.db.execute_query(query)
        rows = self.db.fetch_all()
        self.db.close_cursor()

        for row in rows:
            self.tree.insert("", END, values=row[1:])

        self.update_scrollbars()

    def update_scrollbars(self):
        self.tree.update_idletasks()

        # Проверка вертикального скроллбара
        if len(self.tree.get_children()) > 0:
            # Проверяем, выходит ли содержимое за границы видимой области
            y1, y2 = self.tree.yview()
            if (y1, y2) != (0.0, 1.0):
                self.scrollbar_v.pack(side=RIGHT, fill=Y)
            else:
                self.scrollbar_v.pack_forget()

        # Проверка горизонтального скроллбара
        x1, x2 = self.tree.xview()
        if (x1, x2) != (0.0, 1.0):
            self.scrollbar_h.pack(side=BOTTOM, fill=X)
        else:
            self.scrollbar_h.pack_forget()







    def open_modal(self):
        modal_window = Toplevel(self)
        modal_window.title("Вход в систему")
        modal_window.resizable(False, False)
        modal_window.grab_set()

        x = self.winfo_x() + self.btn_log.winfo_x()
        y = self.winfo_y() + self.btn_log.winfo_y()

        modal_window.geometry(f"+{x + self.btn_log.winfo_width() - 130}+{y+5}")

        label1 = Label(modal_window, text="Логин:")
        label1.pack(pady=1)
        entry1 = Entry(modal_window)
        entry1.pack(pady=5, padx=3)

        label2 = Label(modal_window, text="Пароль")
        label2.pack(pady=1)
        entry2 = Entry(modal_window)
        entry2.pack(pady=5, padx=3)

        def on_cancel():
            modal_window.destroy()

        def on_confirm():
            user = entry1.get()
            password = entry2.get()
            self.db = Database()
            try:
                self.db.connect(user,password)
                if self.db.is_connected():
                    self.btn_log.config(text='Выход')
                    modal_window.destroy()
                else:
                    pass
            except Exception as e:
                print(e)


        btn_cancel = Button(modal_window, text="Отмена", command=on_cancel, width=8)
        btn_cancel.pack(side=LEFT, pady=1, padx=(1,0))
        btn_confirm = Button(modal_window,text="Вход",width=8, command=on_confirm)
        btn_confirm.pack(side=LEFT,pady=1,padx=(0,1))



    def show_add_menu(self):
        x = self.btn_add_new.winfo_rootx()
        y = self.btn_add_new.winfo_rooty() + self.btn_add_new.winfo_height()
        self.add_menu.post(x,y)

    def open_add_client_window(self):
        window = Toplevel(self)
        window.title("Добавить клиента")
        window.geometry("500x200")
        window.resizable(False, False)
        window.grab_set()

        Label(window, text="ФИО:").grid(row=0, column=0, padx=5, pady=(20,5))
        full_name_entry = Entry(window)
        full_name_entry.grid(row=0, column=1, padx=5, pady=(20,5), ipadx=120)

        Label(window, text="Телефон:").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = Entry(window)
        phone_entry.grid(row=1, column=1, padx=5, pady=5,ipadx=40, sticky='w')

        Label(window, text="Тип клиента:").grid(row=2, column=0, padx=5, pady=5)
        client_type_var = StringVar()
        Radiobutton(window, text="Частный", variable=client_type_var, value="private",
                    command=lambda:self.disabler(company_info_entry)).grid(row=2, column=1, padx=5, pady=5,sticky='w')
        Radiobutton(window, text="Юридический", variable=client_type_var, value="legal",
                    command=lambda:self.disabler(company_info_entry,'normal')).grid(row=2, column=1, padx=5, pady=5)

        Label(window, text="О компании:").grid(row=4, column=0, padx=5, pady=5)
        company_info_entry = Entry(window,state=DISABLED)
        company_info_entry.grid(row=4, column=1, padx=5, pady=5, ipadx=120)

        def save_client():
            full_name = full_name_entry.get()
            phone = phone_entry.get()
            client_type = client_type_var.get()
            company_info = company_info_entry.get()
            if company_info.strip() == '':
                company_info = None

            if not full_name or not phone:
                messagebox.showerror("Ошибка", "Поля 'ФИО' и 'Телефон' обязательны!")
                return

            query = """
                        INSERT INTO clients (full_name, phone, client_type, company_info)
                        VALUES (%s, %s, %s, %s)
                        """
            try:
                self.db.open_cursor()
                self.db.execute_query(query, (full_name, phone, client_type, company_info))
                self.db.commit()
                messagebox.showinfo("Успех", "Клиент успешно добавлен!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении клиента: {e}")
            finally:
                self.db.close_cursor()

        Button(window, text="Сохранить", command=save_client).grid(row=5, column=1, padx=5, pady=5)
        Button(window, text='Отмена', command=lambda: window.destroy()).grid(row=5, column=1, padx=5, pady=5,
                                                                             sticky='e')

    def open_add_tariff_window(self):
        window = Toplevel(self)
        window.title("Добавить тариф")
        window.geometry("500x200")
        window.resizable(False,False)
        window.grab_set()

        Label(window, text="Название:").grid(row=0, column=0, padx=5, pady=(20,5))
        tariff_name_entry = Entry(window)
        tariff_name_entry.grid(row=0, column=1, padx=5, pady=(20,5), ipadx=120)

        Label(window, text="Cтоимость:").grid(row=1, column=0, padx=5, pady=5)
        tariff_price_entry = Entry(window)
        tariff_price_entry.grid(row=1, column=1, padx=5, pady=5,sticky='w')

        Label(window, text="Тип тарифа:").grid(row=2, column=0, padx=5, pady=5)
        tariff_type_var = StringVar()
        Radiobutton(window, text="Частный", variable=tariff_type_var, value="private").grid(row=2, column=1, padx=5, pady=(5,0),sticky='w')
        Radiobutton(window, text="Коммерческий", variable=tariff_type_var, value="legal").grid(row=2, column=1, padx=5, pady=(0,5))

        Label(window, text="Описание:").grid(row=4, column=0, padx=5, pady=5)
        description_entry = Entry(window)
        description_entry.grid(row=4, column=1, padx=5, pady=5, ipadx=120,sticky='w')

        def save_tariff():
            tariff_name = tariff_name_entry.get()
            tariff_price = tariff_price_entry.get()
            tariff_type = tariff_type_var.get()
            description = description_entry.get()

            if not tariff_name or not tariff_price or not tariff_type or not description:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return

            query = """
                        INSERT INTO tariffs (tariff_name, tariff_price, tariff_type, description)
                        VALUES (%s, %s, %s, %s)
                        """
            try:
                self.db.open_cursor()
                self.db.execute_query(query, (tariff_name, tariff_price, tariff_type, description))
                self.db.commit()
                messagebox.showinfo("Успех", "Тариф успешно добавлен!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении тарифа: {e}")
            finally:
                self.db.close_cursor()

        Button(window, text="Сохранить", command=save_tariff).grid(row=5, column=1, padx=5, pady=5)
        Button(window, text='Отмена', command=lambda: window.destroy()).grid(row=5, column=1, padx=5, pady=5,
                                                                             sticky='e')

    def open_add_transaction_window(self):
        self.get_id_name_phone()
        window = Toplevel(self)
        window.title("Добавить транзакцию")
        window.geometry("500x200")

        selected_account_id = StringVar()

        accounts_list = [f'{name} ({phone})' for name, phone in self.id_name_phone.values()]

        def on_client_select(event):
            selected_value = client_combobox.get()

            phone = selected_value.split("(")[-1].rstrip(")")

            for account_id, (name, client_phone) in self.id_name_phone.items():
                if phone == client_phone:
                    selected_account_id.set(account_id)
                    break


        Label(window, text="Клиент:").grid(row=0, column=0, padx=5, pady=(20,5))
        client_combobox = ttk.Combobox(window, values=accounts_list, state='readonly')
        client_combobox.grid(row=0, column=1, padx=5, pady=(20,5), ipadx=105,sticky='w')
        client_combobox.bind("<<ComboboxSelected>>", on_client_select)

        Label(window, text="Сумма:").grid(row=1, column=0, padx=5, pady=5)
        amount_entry = Entry(window)
        amount_entry.grid(row=1, column=1, padx=5, pady=5,sticky='w')

        Label(window, text="Тип транзакции:").grid(row=2, column=0, padx=5, pady=5)
        transaction_type_var = StringVar()
        Radiobutton(window, text="Списание", variable=transaction_type_var, value="debit").grid(row=2, column=1, padx=5, pady=5,sticky='w')
        Radiobutton(window, text="Пополнение", variable=transaction_type_var, value="deposit").grid(row=2, column=1, padx=5, pady=5)

        Label(window, text="Описание:").grid(row=4, column=0, padx=5, pady=5)
        description_entry = Entry(window)
        description_entry.grid(row=4, column=1, padx=5, pady=5, ipadx=120,sticky='w')



        def save_transaction():
            client = selected_account_id.get()
            amount = amount_entry.get()
            transaction_type = transaction_type_var.get()
            description = description_entry.get()
            if  description.strip()=='':
                description = None

            if not client or not amount or not transaction_type:
                print(client, amount,transaction_type)
                messagebox.showerror("Ошибка", "Не хватает данных")
                return

            query = """
                        INSERT INTO transactions (account_id, transaction_type, amount, description)
                        VALUES (%s, %s, %s, %s)
                        """
            try:
                self.db.open_cursor()
                self.db.execute_query(query, (client, transaction_type, amount, description))
                self.db.commit()
                messagebox.showinfo("Успех", "Транзакция  успешно добавлена!")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении транзакции: {e}")
            finally:
                self.db.close_cursor()

        Button(window, text="Сохранить", command=save_transaction).grid(row=5, column=1, padx=5, pady=5)
        Button(window, text='Отмена', command=lambda: window.destroy()).grid(row=5, column=1, padx=5, pady=5,
                                                                             sticky='e')





    def open_add_account_window(self):
        self.get_clients_and_tariffs()
        window = Toplevel(self)
        window.title("Добавить лицевой счёт")
        window.geometry("500x300")

        # Переменные для хранения выбранных значений
        selected_client_id = StringVar()
        selected_tariff_id = StringVar()

        # Список клиентов
        clients_list = [f'{name} ({phone}) {client_type}' for name, phone, client_type in self.clients_without_accounts.values()]
        tariff_list = []
        # Функция для обработки выбора клиента
        def on_client_select(event):
            tariff_list.clear()
            selected_value = client_combobox.get()
            # Извлекаем телефон клиента
            phone = selected_value.split("(")[-1].split(")")[0]
            current_client_type = selected_value.split()[-1]


            # Находим id клиента и его тип
            for client_id, (name, client_phone, client_type) in self.clients_without_accounts.items():
                if phone == client_phone:
                    selected_client_id.set(client_id)

            for tariff_id, (tariff_name, tariff_type) in self.actual_tariffs.items():
                if current_client_type == tariff_type:
                    tariff_list.append(tariff_name)

            tariff_combobox.configure(values=tariff_list)



        # Функция для обработки выбора тарифа
        def on_tariff_select(event):
            selected_value = tariff_combobox.get()

            # Извлекаем название тарифа
            tariff_name = selected_value.split("(")[0].strip()

            # Находим id тарифа
            for tariff_id,(t_name, t_type) in self.actual_tariffs.items():
                if t_name == tariff_name:
                    selected_tariff_id.set(tariff_id)
                    break

        # Combobox для выбора клиента
        Label(window, text="Клиент:").grid(row=0, column=0, padx=5, pady=(20, 5))
        client_combobox = ttk.Combobox(window, values=clients_list, state='readonly')
        client_combobox.grid(row=0, column=1, padx=5, pady=(20, 5), ipadx=80, sticky='w')
        client_combobox.bind("<<ComboboxSelected>>", on_client_select)

        # Combobox для выбора тарифа
        Label(window, text="Тариф:").grid(row=1, column=0, padx=5, pady=5)
        tariff_combobox = ttk.Combobox(window, state='readonly')
        tariff_combobox.grid(row=1, column=1, padx=5, pady=5, ipadx=80, sticky='w')
        tariff_combobox.bind("<<ComboboxSelected>>", on_tariff_select)

        Label(window, text="Статус счёта:").grid(row=2, column=0, padx=5, pady=5)
        account_status_var = StringVar()
        Radiobutton(window, text="Активен", variable=account_status_var, value="active").grid(row=2, column=1, padx=5, pady=5, sticky='w')
        Radiobutton(window, text="Заблокирован", variable=account_status_var, value="blocked").grid(row=2, column=1, padx=5, pady=5)


        Label(window, text="Текущий баланс:").grid(row=3, column=0, padx=5, pady=5)
        current_balance_entry = Entry(window)
        current_balance_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        Label(window, text="Текущая задолженность:").grid(row=4, column=0, padx=5, pady=5)
        current_debt_entry = Entry(window)
        current_debt_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        Label(window, text="Оплачено до:").grid(row=5, column=0, padx=5, pady=5)
        next_payment_entry = Entry(window)
        next_payment_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        def save_account():
            client = selected_client_id.get()
            tariff = selected_tariff_id.get()
            status = account_status_var.get()
            current_balance = current_balance_entry.get()
            current_debt = current_debt_entry.get()
            next_payment = next_payment_entry.get()

            if current_balance.strip()=='':
                current_balance = '0.00'
            if current_debt.strip() == '':
                current_debt = '0.00'
            if  next_payment.strip()=='':
                next_payment = None

            if not client or not tariff or not status:
                messagebox.showerror("Ошибка", "Не хватает данных")
                return

            query = """
                        INSERT INTO accounts (client_id, tariff_id, account_status, current_balance, current_debt, next_payment_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
            try:
                self.db.open_cursor()
                self.db.execute_query(query, (client, tariff, status, current_balance, current_debt, next_payment))
                self.db.commit()
                self.clients_without_accounts = {}
                messagebox.showinfo("Успех", "аккаунт  успешно добавлен!")
                window.destroy()



            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении аккаунта: {e}")
            finally:
                self.db.close_cursor()




        # Кнопки
        Button(window, text="Сохранить", command=save_account).grid(row=6, column=1, padx=5, pady=5)
        Button(window, text='Отмена', command=lambda: window.destroy()).grid(row=6, column=1, padx=5, pady=5, sticky='e')




    def connection(self):
        self.db = Database()
        if self.db.is_connected():
            self.db.disconnect()
            self.db = None
            self.btn_log.config(text='Вход')
        else:
            self.open_modal()

    def disabler(self, item, status = 'disabled'):
        item.delete(0, END)
        item.config(state=status)


    def get_id_name_phone(self):
        try:
            self.db.open_cursor()
            self.db.execute_query("SELECT * FROM get_id_name_phone()")
            rows = self.db.fetch_all()
            for row in rows:
                self.id_name_phone[row[0]] = row[1:]
        except Exception as e:
            print(e)
        finally:
            self.db.close_cursor()


    def get_clients_and_tariffs(self):  # get_clients_without_accounts(): client_id, phone, client_type
                                        # get_tariff_info(): tariff_id, tariff_name, tariff_type
        try:
            self.db.open_cursor()
            self.db.execute_query("SELECT * FROM get_clients_without_accounts()")
            client_rows = self.db.fetch_all()
            self.db.execute_query("SELECT * FROM get_tariff_info()")
            tariff_rows = self.db.fetch_all()
            for client_row in client_rows:
                self.clients_without_accounts[client_row[0]] = client_row[1:]
            for  tariff_row in tariff_rows:
                self.actual_tariffs[tariff_row[0]] = tariff_row[1:]
        except Exception as e:
            print(e)
        finally:
            self.db.close_cursor()







app = App()
app.mainloop()