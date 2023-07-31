import tkinter as tk
from tkinter import ttk, messagebox
from src.db import DB
from src.crypto import Crypto

__version__ = 2.0
__author__ = 'Rafael Horta'
__github__ = 'https://github.com/RafaelHorta?tab=repositories'
__doc__ = 'Contrasafer'

class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        # Settings
        width = 700
        height = 650
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x_position = (width_screen - width) // 2
        y_position = (height_screen - height) // 2

        self.title("Contrasafer")
        self.geometry(f"{width}x{height}+{x_position}+{y_position}")
        self.minsize(width, height)
        self.maxsize(width + 50, height + 50)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Control variables
        self._id = tk.IntVar()
        self._sitename = tk.StringVar()
        self._email = tk.StringVar()
        self._username = tk.StringVar()
        self._password = tk.StringVar()
        self._search = tk.StringVar()

        # Main Frame
        frame_main = tk.Frame(self, bg="black")
        frame_main.pack(fill="both", expand=True)
        frame_main.rowconfigure(index=0, weight=1)
        frame_main.rowconfigure(index=1, weight=1)
        frame_main.rowconfigure(index=2, weight=1)
        frame_main.columnconfigure(index=0, weight=1)

        # Form Frame
        form_frame = tk.LabelFrame(frame_main, text="USER FORM", bg="black", fg="gray")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(5):
            form_frame.rowconfigure(index=i, weight=1)
            form_frame.columnconfigure(index=i, weight=1)

        tk.Label(form_frame, text="Site name", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Email", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Username", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Password", bg="black", fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(form_frame, textvariable=self._sitename, bg="#121212", fg="white", highlightbackground="#121212", highlightcolor="white", borderwidth=0).grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")
        tk.Entry(form_frame, textvariable=self._email, bg="#121212", fg="white", highlightbackground="#121212", highlightcolor="white", borderwidth=0).grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")
        tk.Entry(form_frame, textvariable=self._username, bg="#121212", fg="white", highlightbackground="#121212", highlightcolor="white", borderwidth=0).grid(row=2, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")
        tk.Entry(form_frame, textvariable=self._password, bg="#121212", fg="white", highlightbackground="#121212", highlightcolor="white", borderwidth=0).grid(row=3, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        # - - - Buttons
        tk.Button(form_frame, text="REGISTER", bg="#0C560C", fg="white", highlightthickness=0, command=self._save_data).grid(row=4, column=1, padx=10, pady=10, sticky="e")
        self._btn_update = tk.Button(form_frame, text="UPDATE", bg="#46681F", fg="white", highlightthickness=0, state="disabled", command=self._update_data)
        self._btn_update.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        # Table Frame
        table_frame = tk.LabelFrame(frame_main, text="TABLE", bg="black", fg="gray")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        table_frame.rowconfigure(index=0, weight=1)
        table_frame.rowconfigure(index=1, weight=1)

        for i in range(7):
            table_frame.columnconfigure(index=i, weight=1)

        # - - - Actions
        tk.Button(table_frame, text="EDIT", bg="#BFB900", fg="white", highlightthickness=0, command=self._get_one_data).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="ew")
        tk.Button(table_frame, text="DELETE", bg="#7F0000", fg="white", highlightthickness=0, command=self._delete_data).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(table_frame, text="VIEW", bg="#1C7C9B", fg="white", highlightthickness=0, command=self._show_password).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # - - - Actions - Search
        tk.Entry(table_frame, textvariable=self._search).grid(row=0, column=4, padx=(5, 0), pady=5, sticky="ew")
        tk.Button(table_frame, text="SEARCH", bg="#1E216B", fg="white", highlightthickness=0, command=self._search_data).grid(row=0, column=5, padx=(0, 10), pady=5, sticky="ew")

        # - - - Treeview
        columns = ('sitename', 'email', 'username')
        self._table = ttk.Treeview(table_frame, selectmode="browse", columns=columns, height=10)
        self._table.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)

        # - - - Treeview - Heading
        self._table.heading("#0", text="ID")
        self._table.heading("sitename", text="Sitename")
        self._table.heading("email", text="Email")
        self._table.heading("username", text="Username")

        # - - - Treeview - Columns
        self._table.column("#0", width=50, minwidth=40, anchor="center")
        self._table.column("sitename", minwidth=200, anchor="center")
        self._table.column("email", minwidth=200, anchor="center")
        self._table.column("username", minwidth=200, anchor="center")

        # Summon database class
        try:
            self._objDB = DB()
        except Exception as ex:
            messagebox.showerror("DB connection error", ex)

            self.destroy()

        # Execute
        self._get_all_data()


    # Get data from database and then insert it into table
    def _insert_into_table(self, data: list) -> None:
        if data:
            self._table.delete(*self._table.get_children())

            for item in data:
                self._table.insert('', 'end', text=item[0], values=(item[1], item[2], item[3]))
        else:
            messagebox.showinfo("", "There isn't data recorded")

    # Copy password to clipboard
    def _copy_to_clipboard(self):
        password = self._password_shown.get()

        if password:
            self.clipboard_clear()
            self.clipboard_append(self._password_shown.get())

    # - - - CRUD - - -
    # Get data from database
    def _get_all_data(self) -> None:
        data = self._objDB.get(['id', 'sitename', 'email', 'username'])

        self._insert_into_table(data)

    # Search data from database
    def _search_data(self) -> None:
        data = self._objDB.get(['id', 'sitename', 'email', 'username'], search=self._search.get())

        self._insert_into_table(data)

    # Get data to edit
    def _get_one_data(self) -> None:
        try:
            focus = self._table.focus()

            if not focus:
                raise ValueError("Select a item from the table")

            pk = int(self._table.item(focus, 'text'))
            data = self._objDB.get(['sitename', 'email', 'username'], pk)[0]

            if not data:
                raise ValueError(f"Data with id '{pk}' not found")

            self._id.set(pk)
            self._sitename.set(data[0])
            self._email.set(data[1])
            self._username.set(data[2])
            self._btn_update.config(state="normal")

        except Exception as ex:
            messagebox.showerror("", ex)

    # Show window to view password
    def _show_password(self) -> None:
        try:
            focus = self._table.focus()

            if not focus:
                raise ValueError("Select a item from the table")

            pk = int(self._table.item(focus, 'text'))
            data = self._objDB.get(['password', 'key'], pk)[0]

            # Summon Crypto class
            objCrypt = Crypto(data[1])
            password = objCrypt.decrypt(data[0])

            # Control variable
            self._password_shown = tk.StringVar(value=password)

            # Create Toplevel
            toplevel = tk.Toplevel(self, bg="black")
            toplevel.title("Your password")

            # Password entry
            tk.Entry(toplevel, textvariable=self._password_shown, bg="black", fg="gray", highlightthickness=0, borderwidth=0).pack(padx=10, pady=10)

            # Button to copy password
            tk.Button(toplevel, text="Copy", bg="black", fg="gray", highlightthickness=0, command=self._copy_to_clipboard).pack(padx=10, pady=10)

        except Exception as ex:
            messagebox.showerror("", ex)

    # Get data from form and save it to the database
    def _save_data(self) -> None:
        sitename = self._sitename.get()
        email = self._email.get()
        username = self._username.get()
        password = self._password.get()

        try:
            if not sitename or not email or not username or not password:
                raise ValueError("You must fill out the form")

            # Cryptography object
            objCrypto = Crypto()
            password = objCrypto.encrypt(password)

            self._objDB.insert({
                'sitename': sitename,
                'email': email,
                'username': username,
                'password': password,
                'key': objCrypto.get_key
            })
            self._clean_form()
            self._get_all_data()

        except Exception as ex:
            messagebox.showerror("", ex)

    # Update data saved
    def _update_data(self) -> None:
        pk = self._id.get()
        sitename = self._sitename.get()
        email = self._email.get()
        username = self._username.get()
        password = self._password.get()

        try:
            if not pk or not sitename or not email or not username:
                raise ValueError("You must fill out the form")

            data = {
                'sitename': sitename,
                'email': email,
                'username': username
            }

            if password:
                objCrypto = Crypto() # Cryptography object
                password = objCrypto.encrypt(password)
                data['password'] = password
                data['key'] = objCrypto.get_key

            self._objDB.update(pk, data)
            self._clean_form()
            self._get_all_data()

        except Exception as ex:
            messagebox.showerror("", ex)

    # Get data to delete
    def _delete_data(self):
        try:
            focus = self._table.focus()

            if not focus:
                raise ValueError("Select a item from the table")

            response = messagebox.askyesno("", "Do you want to delete the element?")

            if response:
                pk = int(self._table.item(focus, 'text'))

                self._objDB.delete(pk)
                self._clean_form()
                self._get_all_data()

        except Exception as ex:
            messagebox.showerror("", ex)

    # - - - - - -
    # Clean form
    def _clean_form(self) -> None:
        self._id.set("")
        self._sitename.set("")
        self._email.set("")
        self._username.set("")
        self._password.set("")
        self._btn_update.config(state="disabled")

    def _on_closing(self):
        try:
            if messagebox.askokcancel("Close", "Do you want to close?"):
                self._objDB.close_connection()
                self.destroy()
        except Exception as ex:
            messagebox.showerror("ERROR", ex)

if __name__ == "__main__":
    app = App()
    app.mainloop()
