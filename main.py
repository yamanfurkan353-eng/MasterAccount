import sqlite3
from pathlib import Path
from datetime import datetime
import customtkinter as ctk


DB_PATH = Path(__file__).parent / "data.db"


def init_db(path: Path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS incomes(
            id INTEGER PRIMARY KEY,
            date TEXT,
            description TEXT,
            amount REAL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY,
            date TEXT,
            description TEXT,
            amount REAL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY,
            name TEXT,
            contact TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    return conn


class MainApp(ctk.CTk):
    def __init__(self, db_conn):
        super().__init__()
        self.conn = db_conn
        self.title("MasterAccount — Masaüstü Muhasebe")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Layout: sidebar + content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="MasterAccount",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.logo.pack(pady=(20, 30))

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar, text="📊 Dashboard", command=self.show_dashboard, height=40
        )
        self.btn_income_expense = ctk.CTkButton(
            self.sidebar, text="💰 Gelir/Gider", command=self.show_income_expense, height=40
        )
        self.btn_customers = ctk.CTkButton(
            self.sidebar, text="👥 Müşteriler", command=self.show_customers, height=40
        )
        self.btn_settings = ctk.CTkButton(
            self.sidebar, text="⚙️ Ayarlar", command=self.show_settings, height=40
        )

        for w in (self.btn_dashboard, self.btn_income_expense, self.btn_customers, self.btn_settings):
            w.pack(fill="x", padx=12, pady=8)

        # Content frames
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nswe", padx=16, pady=16)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
            self.DashboardFrame,
            self.IncomeExpenseFrame,
            self.CustomersFrame,
            self.SettingsFrame,
        ):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nswe")

        self.show_dashboard()

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()

    def show_dashboard(self):
        self.show_frame("DashboardFrame")
        self.frames["DashboardFrame"].update_cards()

    def show_income_expense(self):
        self.show_frame("IncomeExpenseFrame")
        self.frames["IncomeExpenseFrame"].refresh_table()

    def show_customers(self):
        self.show_frame("CustomersFrame")
        self.frames["CustomersFrame"].refresh_table()

    def show_settings(self):
        self.show_frame("SettingsFrame")

    class DashboardFrame(ctk.CTkFrame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.grid_columnconfigure((0, 1, 2), weight=1)

            self.card_income = ctk.CTkFrame(self, corner_radius=12, fg_color="#2d3748")
            self.card_balance = ctk.CTkFrame(self, corner_radius=12, fg_color="#2d3748")
            self.card_expense = ctk.CTkFrame(self, corner_radius=12, fg_color="#2d3748")

            self.card_income.grid(row=0, column=0, padx=12, pady=12, sticky="nwe")
            self.card_balance.grid(row=0, column=1, padx=12, pady=12, sticky="nwe")
            self.card_expense.grid(row=0, column=2, padx=12, pady=12, sticky="nwe")

            self.lbl_income = ctk.CTkLabel(
                self.card_income, text="Toplam Gelir", font=ctk.CTkFont(size=14, weight="bold")
            )
            self.val_income = ctk.CTkLabel(
                self.card_income, text="0 ₺", font=ctk.CTkFont(size=28, weight="bold"), text_color="#4ade80"
            )
            self.lbl_income.pack(pady=(16, 4))
            self.val_income.pack(pady=(0, 16))

            self.lbl_balance = ctk.CTkLabel(
                self.card_balance, text="Toplam Bakiye", font=ctk.CTkFont(size=14, weight="bold")
            )
            self.val_balance = ctk.CTkLabel(
                self.card_balance, text="0 ₺", font=ctk.CTkFont(size=28, weight="bold"), text_color="#60a5fa"
            )
            self.lbl_balance.pack(pady=(16, 4))
            self.val_balance.pack(pady=(0, 16))

            self.lbl_expense = ctk.CTkLabel(
                self.card_expense, text="Toplam Gider", font=ctk.CTkFont(size=14, weight="bold")
            )
            self.val_expense = ctk.CTkLabel(
                self.card_expense, text="0 ₺", font=ctk.CTkFont(size=28, weight="bold"), text_color="#f87171"
            )
            self.lbl_expense.pack(pady=(16, 4))
            self.val_expense.pack(pady=(0, 16))

        def update_cards(self):
            cur = self.controller.conn.cursor()
            cur.execute("SELECT COALESCE(SUM(amount),0) FROM incomes")
            total_income = cur.fetchone()[0] or 0
            cur.execute("SELECT COALESCE(SUM(amount),0) FROM expenses")
            total_expense = cur.fetchone()[0] or 0
            balance = total_income - total_expense

            self.val_income.configure(text=f"{total_income:,.2f} ₺")
            self.val_expense.configure(text=f"{total_expense:,.2f} ₺")
            color = "#4ade80" if balance >= 0 else "#f87171"
            self.val_balance.configure(text=f"{balance:,.2f} ₺", text_color=color)

    class IncomeExpenseFrame(ctk.CTkFrame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)

            # Form Frame
            form_frame = ctk.CTkFrame(self, fg_color="#2d3748", corner_radius=12)
            form_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 16))
            form_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(form_frame, text="Tür", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=0, column=0, padx=12, pady=(12, 4), sticky="w"
            )
            self.var_type = ctk.StringVar(value="Gelir")
            type_menu = ctk.CTkOptionMenu(
                form_frame, values=["Gelir", "Gider"], variable=self.var_type
            )
            type_menu.grid(row=0, column=1, padx=12, pady=(12, 4), sticky="ew")

            ctk.CTkLabel(form_frame, text="Tarih", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=1, column=0, padx=12, pady=4, sticky="w"
            )
            self.date_entry = ctk.CTkEntry(form_frame)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.date_entry.grid(row=1, column=1, padx=12, pady=4, sticky="ew")

            ctk.CTkLabel(form_frame, text="Açıklama", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=2, column=0, padx=12, pady=4, sticky="w"
            )
            self.desc_entry = ctk.CTkEntry(form_frame, placeholder_text="Örn: Danışmanlık hizmeti")
            self.desc_entry.grid(row=2, column=1, padx=12, pady=4, sticky="ew")

            ctk.CTkLabel(form_frame, text="Tutar (₺)", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=3, column=0, padx=12, pady=4, sticky="w"
            )
            self.amount_entry = ctk.CTkEntry(form_frame, placeholder_text="0.00")
            self.amount_entry.grid(row=3, column=1, padx=12, pady=4, sticky="ew")

            btn_add = ctk.CTkButton(
                form_frame, text="Kaydet", command=self.save_entry, height=36, fg_color="#10b981"
            )
            btn_add.grid(row=4, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

            # Table Frame
            table_frame = ctk.CTkFrame(self, fg_color="#2d3748", corner_radius=12)
            table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
            table_frame.grid_rowconfigure(1, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                table_frame, text="Gelir ve Gider Kayıtları", font=ctk.CTkFont(size=14, weight="bold")
            ).grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

            from tkinter import ttk

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#2d3748")
            style.configure("Treeview.Heading", background="#3f3f3f", foreground="white")
            style.map("Treeview", background=[("selected", "#10b981")])

            self.tree = ttk.Treeview(
                table_frame,
                columns=("id", "date", "desc", "type", "amount"),
                height=12,
                show="headings",
            )
            self.tree.column("id", width=40, anchor="center")
            self.tree.column("date", width=100, anchor="center")
            self.tree.column("desc", width=250, anchor="w")
            self.tree.column("type", width=80, anchor="center")
            self.tree.column("amount", width=120, anchor="e")

            self.tree.heading("id", text="ID")
            self.tree.heading("date", text="Tarih")
            self.tree.heading("desc", text="Açıklama")
            self.tree.heading("type", text="Tür")
            self.tree.heading("amount", text="Tutar (₺)")

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)

            self.tree.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
            scrollbar.grid(row=1, column=1, sticky="nse", padx=(0, 12), pady=(0, 12))

            btn_delete = ctk.CTkButton(
                table_frame,
                text="Sil",
                command=self.delete_selected,
                height=32,
                fg_color="#ef4444",
                width=100,
            )
            btn_delete.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="e")

        def save_entry(self):
            try:
                date = self.date_entry.get()
                desc = self.desc_entry.get()
                amount = float(self.amount_entry.get())
                entry_type = self.var_type.get()

                if not desc:
                    raise ValueError("Açıklama boş olamaz")
                if amount <= 0:
                    raise ValueError("Tutar sıfırdan büyük olmalı")

                table = "incomes" if entry_type == "Gelir" else "expenses"
                cur = self.controller.conn.cursor()
                cur.execute(
                    f"INSERT INTO {table} (date, description, amount) VALUES (?, ?, ?)",
                    (date, desc, amount),
                )
                self.controller.conn.commit()

                self.desc_entry.delete(0, "end")
                self.amount_entry.delete(0, "end")
                self.refresh_table()
                self.controller.show_frame("DashboardFrame")
                self.controller.frames["DashboardFrame"].update_cards()
            except ValueError as e:
                self._show_error(f"Hata: {e}")
            except Exception as e:
                self._show_error(f"Kayıt hatası: {e}")

        def delete_selected(self):
            selection = self.tree.selection()
            if not selection:
                self._show_error("Silmek için kayıt seçiniz")
                return

            item = selection[0]
            record_id = self.tree.item(item)["values"][0]
            entry_type = self.tree.item(item)["values"][3]

            table = "incomes" if entry_type == "Gelir" else "expenses"
            cur = self.controller.conn.cursor()
            cur.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
            self.controller.conn.commit()
            self.refresh_table()
            self.controller.frames["DashboardFrame"].update_cards()

        def refresh_table(self):
            for item in self.tree.get_children():
                self.tree.delete(item)

            cur = self.controller.conn.cursor()
            cur.execute("SELECT * FROM incomes ORDER BY date DESC")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=(row[0], row[1], row[2], "Gelir", f"{row[3]:,.2f}"))

            cur.execute("SELECT * FROM expenses ORDER BY date DESC")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=(row[0], row[1], row[2], "Gider", f"{row[3]:,.2f}"))

        def _show_error(self, msg):
            error_frame = ctk.CTkFrame(self)
            error_frame.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(error_frame, text=msg, text_color="#f87171").pack(padx=20, pady=10)
            error_frame.after(3000, error_frame.destroy)

    class CustomersFrame(ctk.CTkFrame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)

            # Form Frame
            form_frame = ctk.CTkFrame(self, fg_color="#2d3748", corner_radius=12)
            form_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 16))
            form_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(form_frame, text="Müşteri Adı", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=0, column=0, padx=12, pady=(12, 4), sticky="w"
            )
            self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Örn: Şirket Adı")
            self.name_entry.grid(row=0, column=1, padx=12, pady=(12, 4), sticky="ew")

            ctk.CTkLabel(form_frame, text="İletişim", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=1, column=0, padx=12, pady=4, sticky="w"
            )
            self.contact_entry = ctk.CTkEntry(form_frame, placeholder_text="Örn: +90 555 123 4567 / email")
            self.contact_entry.grid(row=1, column=1, padx=12, pady=4, sticky="ew")

            ctk.CTkLabel(form_frame, text="Notlar", font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=2, column=0, padx=12, pady=4, sticky="w"
            )
            self.notes_entry = ctk.CTkEntry(form_frame, placeholder_text="Ek bilgiler")
            self.notes_entry.grid(row=2, column=1, padx=12, pady=4, sticky="ew")

            btn_add = ctk.CTkButton(
                form_frame, text="Ekle", command=self.add_customer, height=36, fg_color="#10b981"
            )
            btn_add.grid(row=3, column=0, columnspan=2, padx=12, pady=12, sticky="ew")

            # Table Frame
            table_frame = ctk.CTkFrame(self, fg_color="#2d3748", corner_radius=12)
            table_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
            table_frame.grid_rowconfigure(1, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                table_frame, text="Müşteri Listesi", font=ctk.CTkFont(size=14, weight="bold")
            ).grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

            from tkinter import ttk

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#2d3748")
            style.configure("Treeview.Heading", background="#3f3f3f", foreground="white")
            style.map("Treeview", background=[("selected", "#10b981")])

            self.tree = ttk.Treeview(
                table_frame, columns=("id", "name", "contact", "notes"), height=12, show="headings"
            )
            self.tree.column("id", width=40, anchor="center")
            self.tree.column("name", width=150, anchor="w")
            self.tree.column("contact", width=200, anchor="w")
            self.tree.column("notes", width=300, anchor="w")

            self.tree.heading("id", text="ID")
            self.tree.heading("name", text="Müşteri Adı")
            self.tree.heading("contact", text="İletişim")
            self.tree.heading("notes", text="Notlar")

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)

            self.tree.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
            scrollbar.grid(row=1, column=1, sticky="nse", padx=(0, 12), pady=(0, 12))

            btn_delete = ctk.CTkButton(
                table_frame,
                text="Sil",
                command=self.delete_customer,
                height=32,
                fg_color="#ef4444",
                width=100,
            )
            btn_delete.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="e")

        def add_customer(self):
            try:
                name = self.name_entry.get()
                contact = self.contact_entry.get()
                notes = self.notes_entry.get()

                if not name:
                    raise ValueError("Müşteri adı boş olamaz")

                cur = self.controller.conn.cursor()
                cur.execute(
                    "INSERT INTO customers (name, contact, notes) VALUES (?, ?, ?)",
                    (name, contact, notes),
                )
                self.controller.conn.commit()

                self.name_entry.delete(0, "end")
                self.contact_entry.delete(0, "end")
                self.notes_entry.delete(0, "end")
                self.refresh_table()
            except ValueError as e:
                self._show_error(f"Hata: {e}")

        def delete_customer(self):
            selection = self.tree.selection()
            if not selection:
                self._show_error("Silmek için kayıt seçiniz")
                return

            item = selection[0]
            customer_id = self.tree.item(item)["values"][0]
            cur = self.controller.conn.cursor()
            cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
            self.controller.conn.commit()
            self.refresh_table()

        def refresh_table(self):
            for item in self.tree.get_children():
                self.tree.delete(item)

            cur = self.controller.conn.cursor()
            cur.execute("SELECT * FROM customers ORDER BY name")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)

        def _show_error(self, msg):
            error_frame = ctk.CTkFrame(self)
            error_frame.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(error_frame, text=msg, text_color="#f87171").pack(padx=20, pady=10)
            error_frame.after(3000, error_frame.destroy)

    class SettingsFrame(ctk.CTkFrame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            settings_frame = ctk.CTkFrame(self, fg_color="#2d3748", corner_radius=12)
            settings_frame.pack(padx=20, pady=20, fill="both", expand=True)

            ctk.CTkLabel(
                settings_frame,
                text="⚙️ Uygulamaya Ait Bilgiler",
                font=ctk.CTkFont(size=18, weight="bold"),
            ).pack(pady=(20, 10))

            info_text = """
            MasterAccount - Masaüstü Muhasebe Uygulaması
            
            Sürüm: 1.0.0
            Python ile geliştirilmiştir.
            
            Özellikler:
            • Dashboard: Anlık gelir, gider ve bakiye gösterme
            • Gelir/Gider: Kayıt ekleme, listeleme ve silme
            • Müşteriler: Müşteri bilgilerini yönetme
            • Yerel Veritabanı: Veriler lokal olarak güvenli şekilde saklanır
            
            Veritabanı Dosyası:
            data.db (uygulama dizininde)
            
            © 2026 - Tüm Hakları Saklıdır
            """

            ctk.CTkLabel(
                settings_frame, text=info_text, justify="left", font=ctk.CTkFont(size=12)
            ).pack(padx=20, pady=20, anchor="nw")

            btn_reset = ctk.CTkButton(
                settings_frame,
                text="🗑️ Tüm Verileri Sil (Dikkat!)",
                command=self.reset_database,
                fg_color="#ef4444",
                height=40,
            )
            btn_reset.pack(padx=20, pady=(20, 20), fill="x")

        def reset_database(self):
            try:
                cur = self.controller.conn.cursor()
                cur.execute("DELETE FROM incomes")
                cur.execute("DELETE FROM expenses")
                cur.execute("DELETE FROM customers")
                self.controller.conn.commit()
                self._show_message("Veritabanı sıfırlandı")
                self.controller.show_dashboard()
            except Exception as e:
                self._show_error(f"Hata: {e}")

        def _show_error(self, msg):
            error_frame = ctk.CTkFrame(self)
            error_frame.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(error_frame, text=msg, text_color="#f87171").pack(padx=20, pady=10)
            error_frame.after(3000, error_frame.destroy)

        def _show_message(self, msg):
            msg_frame = ctk.CTkFrame(self)
            msg_frame.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(msg_frame, text=msg, text_color="#4ade80").pack(padx=20, pady=10)
            msg_frame.after(3000, msg_frame.destroy)


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = init_db(DB_PATH)
    app = MainApp(conn)
    app.mainloop()


if __name__ == "__main__":
    main()
