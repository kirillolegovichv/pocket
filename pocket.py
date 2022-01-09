import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as mb

class Main(tk.Frame):
	def __init__(self, root):
		super().__init__(root)
		self.init_main()
		self.db = db
		self.view_records()

	def init_main(self):
		toolbar = tk.Frame(bg="#9ee1e1", bd=2)
		toolbar.pack(side=tk.TOP, fill=tk.X)
		
		self.add_img = tk.PhotoImage(file="icon_add.gif")
		btn_open_dialog = tk.Button(toolbar, text="Добавить позицию", 
			command=self.open_dialog, bd=0, compound=tk.TOP, image=self.add_img) 
		btn_open_dialog.pack(side=tk.LEFT)

		self.edit_img = tk.PhotoImage(file="icon_edit.gif")
		btn_edit_dialog = tk.Button(toolbar, text="Редактировать", bd=0, 
			compound=tk.TOP, command=self.open_update_dialog, image=self.edit_img)
		btn_edit_dialog.pack(side=tk.LEFT)

		self.delete_img = tk.PhotoImage(file='icon_delete.gif')
		btn_delete_dialog = tk.Button(toolbar, text="Удалить позицию", bd=0, 
			compound=tk.TOP, command=self.delete_records, image=self.delete_img)
		btn_delete_dialog.pack(side=tk.LEFT)

		self.search_img = tk.PhotoImage(file='icon_search.gif')
		btn_search_dialog = tk.Button(toolbar, text="Поиск", bd=0, compound=tk.TOP, 
			command=self.open_search_dialog, image=self.search_img)
		btn_search_dialog.pack(side=tk.LEFT)

		self.update_img = tk.PhotoImage(file='icon_update.gif')
		btn_refresh = tk.Button(toolbar, text="Обновить", bd=0, compound=tk.TOP, 
			command=self.view_records, image=self.update_img)
		btn_refresh.pack(side=tk.LEFT)

		self.balance_img = tk.PhotoImage(file='icon_balance.gif')
		btn_balance = tk.Button(toolbar, text='Сортировка', bd=0, compound=tk.TOP, 
			command=self.open_balance_dialog, image=self.balance_img)
		btn_balance.pack(side=tk.LEFT)

		footer = tk.Frame(bg="#9ee1e1", bd=2)
		footer.pack(side=tk.BOTTOM, fill=tk.X)

		close_btn = ttk.Button(footer, text="Закрыть", command=root.destroy)
		close_btn.pack(side=tk.RIGHT)

		about_btn = ttk.Button(footer, text="О проекте", command=self.about_project)
		about_btn.pack(side=tk.LEFT)

		self.tree = ttk.Treeview(self, columns=("ID", "description", "costs", "total", "currency"), height=15, show="headings")
		self.tree.column("ID", width=30, anchor=tk.CENTER)
		self.tree.column("description", width=305, anchor=tk.CENTER)
		self.tree.column("costs", width=150, anchor=tk.CENTER)
		self.tree.column("total", width=100, anchor=tk.CENTER)
		self.tree.column("currency", width=60, anchor=tk.CENTER)

		self.tree.heading("ID", text="ID")
		self.tree.heading("description", text="Наименование")
		self.tree.heading("costs", text="Статья дохода/расхода")
		self.tree.heading("total", text="Сумма")
		self.tree.heading("currency", text="Валюта")

		self.tree.pack()

	def sort_article_min(self):
		self.db.c.execute('''SELECT * FROM finance ORDER BY description DESC''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def sort_article_max(self):
		self.db.c.execute('''SELECT * FROM finance ORDER BY description ''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def sort_total_min(self):
		self.db.c.execute('''SELECT * FROM finance ORDER BY total DESC''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def sort_total_max(self):
		self.db.c.execute('''SELECT * FROM finance ORDER BY total ''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def records(self, description, costs, total, currency):
		self.db.insert_data(description, costs, total, currency)
		self.view_records()

	def update_record(self, description, costs, total, currency):
		self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=?, currency=? WHERE ID=?''', 
			(description, costs, total, currency, self.tree.set(self.tree.selection()[0], '#1')))
		self.db.conn.commit()
		self.view_records()

	def view_records(self):
		self.db.c.execute('''SELECT * FROM finance''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values = row) for row in self.db.c.fetchall()]

	def delete_records(self):
		for selection_item in self.tree.selection():
			self.db.c.execute('''DELETE FROM finance WHERE id=?''', (self.tree.set(selection_item, '#1'),))
			self.db.conn.commit()
			self.view_records()

	def search_records(self, description):
		description = ('%' + description + '%',)
		self.db.c.execute('''SELECT * FROM finance WHERE description LIKE ?''', description)
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

	def balance_record(self):
		for i in self.db.c.execute('''SELECT coloumn 4 FROM finance'''):
			balance += i

	def about_project(self):
		mb.showinfo("О проекте","Этот проект создан студентом группы 4941 Кириллом \nВасильевым исключительно в учебных целях.")

	def open_dialog(self):
		Child()

	def open_update_dialog(self):
		Update()

	def open_search_dialog(self):
		Search()

	def open_balance_dialog(self):
		Balance()


class Child(tk.Toplevel):
	def __init__(self):
		super().__init__(root)
		self.init_child()
		self.view = app
		
	def init_child(self):
		self.title("Добавить доходы/расходы")
		self.geometry("400x250+425+230")
		self.resizable(False, False)

		label_description = tk.Label(self, text="Наименование")
		label_description.place(x=50, y=50)
		label_select = tk.Label(self, text="Статья дохода/расхода")
		label_select.place(x=50, y=80)
		label_sum = tk.Label(self, text="Сумма")
		label_sum.place(x=50, y=110)
		label_cur = tk.Label(self, text='Валюта')
		label_cur.place(x=50, y=140)


		self.entry_description = ttk.Entry(self)
		self.entry_description.place(x=200, y=50)

		self.entry_money = tk.Entry(self)
		self.entry_money.place(x=200, y=110)

		self.combobox = ttk.Combobox(self, values=[u"Доход", u"Расход"])
		self.combobox.current(0)
		self.combobox.place(x=200, y=80)

		self.cur = ttk.Combobox(self, values=[u"₽", u"$"])
		self.cur.current(0)
		self.cur.place(x=200, y=140)

		btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
		btn_cancel.place(x=300, y=200)

		self.btn_ok = ttk.Button(self, text="Добавить")
		self.btn_ok.place(x=220, y=200)
		self.btn_ok.bind("<Button-1>", lambda event: self.view.records(self.entry_description.get(), 
			self.combobox.get(), self.entry_money.get(), self.cur.get()))

		self.grab_set()
		self.focus_set()


class Update(Child):
	def __init__(self):
		super().__init__()
		self.init_edit()
		self.view = app
		self.db = db
		self.default_data()

	def init_edit(self):
		self.title("Редактировать")
		btn_edit = ttk.Button(self, text="Редактировать")
		btn_edit.place(x=205, y=170)
		btn_edit.bind("<Button-1>", lambda event: self.view.update_record(self.entry_description.get(), 
			self.combobox.get(), self.entry_money.get(), self.cur.get()))
		self.btn_ok.destroy()

	def default_data(self):
		self.db.c.execute('''SELECT * FROM finance WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
		row = self.db.c.fetchone()
		self.entry_description.insert(0, row[1])
		if row[2] != 'Доход':
			self.combobox.current(1)
		self.entry_money.insert(0, row[3])
		if row[4] != "₽":
			self.cur.current(1)


class Search(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.init_search()
		self.view = app

	def init_search(self):
		self.title('Поиск')
		self.geometry('300x100+400+300')
		self.resizable(False, False)
		
		label_search = tk.Label(self, text='Поиск')
		label_search.place(x=50, y=20)
		
		self.entry_search = ttk.Entry(self)
		self.entry_search.place(x=105, y=20, width=150)

		btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
		btn_cancel.place(x=185, y=50)

		btn_search = ttk.Button(self, text='Поиск')
		btn_search.place(x=105, y=50)
		btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
		btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class Balance(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.init_balance()
		self.view = app

	def init_balance(self):
		self.title('Сортировка')
		self.geometry('400x200+400+300')
		self.resizable(False, False)

		lbl_name = tk.Label(self, text='Название')
		lbl_name.place(x=70, y=20)

		lbl_total = tk.Label(self, text='Сумма')
		lbl_total.place(x=270, y=20)

		name_sort_min = ttk.Button(self, text='Сортировка по убыванию')
		name_sort_min.place(x=20, y=50)
		name_sort_min.bind('<Button-1>', lambda event: self.view.sort_article_min())

		name_sort_max = ttk.Button(self, text='Сортировка по возрастанию')
		name_sort_max.place(x=15, y=80)
		name_sort_max.bind('<Button-1>', lambda event: self.view.sort_article_max())

		total_sort_min = ttk.Button(self, text='Сортировка по убыванию')
		total_sort_min.place(x=220, y=50)
		total_sort_min.bind('<Button-1>', lambda event: self.view.sort_total_min())

		total_sort_max = ttk.Button(self, text='Сортировка по возрастанию')
		total_sort_max.place(x=215, y=80)
		total_sort_max.bind('<Button-1>', lambda event: self.view.sort_total_max())

		btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
		btn_cancel.place(x=160, y=170)


class DB:
	def __init__(self):
		self.conn = sqlite3.connect("finance.db")
		self.c = self.conn.cursor()
		self.c.execute('''CREATE TABLE IF NOT EXISTS finance (id integer primary key, 
			description text, costs text, total real, currency text)''')
		self.conn.commit()

	def insert_data(self, description, costs, total, currency):
		self.c.execute('''INSERT INTO finance(description, costs, total, currency) 
			VALUES (?, ?, ?, ?)''', (description, costs, total, currency))
		self.conn.commit()
		

if __name__ == '__main__':
	root = tk.Tk()
	db = DB()
	app = Main(root)
	app.pack()
	root.title("Финансы")
	root.geometry("650x450+300+100")
	root.resizable(False, False)
	root.mainloop()
