import tkinter as tk
from tkinter import messagebox

# Dictionary to store items and their quantities along with units
items_inventory = {}

# Dictionary to store students and their cafe permissions
students = {}

class CafeManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cafe Management System")
        self.geometry("550x400")

        self.pages = []
        self.current_page = None

        self.create_pages()
        self.show_page(HomePage)

    def create_pages(self):
        self.home_page = HomePage(self)
        self.add_page(self.home_page)

        self.add_item_page = AddItemPage(self)
        self.add_page(self.add_item_page)

        self.get_item_page = GetItemPage(self)
        self.add_page(self.get_item_page)

        self.withdraw_item_page = WithdrawItemPage(self)
        self.add_page(self.withdraw_item_page)

        self.register_student_page = RegisterStudentPage(self)
        self.add_page(self.register_student_page)

        self.check_access_page = CheckAccessPage(self)
        self.add_page(self.check_access_page)

    def add_page(self, page):
        self.pages.append(page)

    def show_page(self, page_class):
        if self.current_page:
            self.current_page.pack_forget()

        for page in self.pages:
            if isinstance(page, page_class):
                self.current_page = page
                self.current_page.pack(fill=tk.BOTH, expand=True)
                break

class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="#f0f0f0")

    def back_to_home(self):
        self.master.show_page(HomePage)

class HomePage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Welcome to Cafe Management System", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)

        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack()

        buttons = [
            ("Add Item", AddItemPage),
            ("Get Item Quantity", GetItemPage),
            ("Withdraw Item", WithdrawItemPage),
            ("Register Student", RegisterStudentPage),
            ("Check Student Access", CheckAccessPage)
        ]

        for text, page in buttons:
            tk.Button(buttons_frame, text=text, font=("Arial", 14), width=20, height=2, command=lambda p=page: master.show_page(p)).pack(pady=5)

class AddItemPage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Add Item", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

        self.item_name_label = tk.Label(self, text="Item Name:", font=("Arial", 16), bg="#f0f0f0")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self, font=("Arial", 16))
        self.item_name_entry.pack()

        self.item_quantity_label = tk.Label(self, text="Quantity:", font=("Arial", 16), bg="#f0f0f0")
        self.item_quantity_label.pack()
        self.item_quantity_entry = tk.Entry(self, font=("Arial", 16))
        self.item_quantity_entry.pack()

        self.unit_label = tk.Label(self, text="Unit (kg/liter):", font=("Arial", 16), bg="#f0f0f0")
        self.unit_label.pack()
        self.unit_entry = tk.Entry(self, font=("Arial", 16))
        self.unit_entry.pack()

        self.add_item_button = tk.Button(self, text="Add Item", font=("Arial", 14), command=self.add_item)
        self.add_item_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.back_button.pack()

    def add_item(self):
        item_name = self.item_name_entry.get()
        item_quantity = float(self.item_quantity_entry.get())
        unit = self.unit_entry.get().lower()

        if item_name.strip() == "":
            messagebox.showerror("Error", "Please enter item name")
            return

        if unit not in ['kg', 'liter']:
            messagebox.showerror("Error", "Unit must be 'kg' or 'liter'")
            return

        if item_name in items_inventory:
            existing_unit = items_inventory[item_name]['unit']
            if existing_unit == unit:
                items_inventory[item_name]['quantity'] += item_quantity
            else:
                messagebox.showerror("Error", "Unit mismatch. Item already exists with a different unit.")
                return
        else:
            items_inventory[item_name] = {'quantity': item_quantity, 'unit': unit}

        messagebox.showinfo("Success", "Item added successfully.")

class GetItemPage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Get Item Quantity", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

        self.item_name_label = tk.Label(self, text="Item Name", font=("Arial", 16), bg="#f0f0f0")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self, font=("Arial", 16))
        self.item_name_entry.pack()

        self.get_item_button = tk.Button(self, text="Get Item Quantity", font=("Arial", 14), command=self.get_item_amount)
        self.get_item_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.back_button.pack()

    def get_item_amount(self):
        item_name = self.item_name_entry.get()
        if item_name in items_inventory:
            quantity = items_inventory[item_name]['quantity']
            unit = items_inventory[item_name]['unit']
            messagebox.showinfo("Item Quantity", f"Available quantity: {quantity} {unit}")
        else:
            messagebox.showerror("Error", "Item not found.")

class WithdrawItemPage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Withdraw Item", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

        self.item_name_label = tk.Label(self, text="Item Name:", font=("Arial", 16), bg="#f0f0f0")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(self, font=("Arial", 16))
        self.item_name_entry.pack()

        self.withdraw_quantity_label = tk.Label(self, text="Withdraw Quantity:", font=("Arial", 16), bg="#f0f0f0")
        self.withdraw_quantity_label.pack()
        self.withdraw_quantity_entry = tk.Entry(self, font=("Arial", 16))
        self.withdraw_quantity_entry.pack()

        self.withdraw_item_button = tk.Button(self, text="Withdraw Item", font=("Arial", 14), command=self.withdraw_item)
        self.withdraw_item_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.back_button.pack()

    def withdraw_item(self):
        item_name = self.item_name_entry.get()
        if item_name in items_inventory:
            withdraw_quantity = float(self.withdraw_quantity_entry.get())
            if items_inventory[item_name]['quantity'] >= withdraw_quantity:
                items_inventory[item_name]['quantity'] -= withdraw_quantity
                messagebox.showinfo("Success", "Withdrawal successful.")
            else:
                messagebox.showerror("Error", "Insufficient quantity.")
        else:
            messagebox.showerror("Error", "Item not found.")

class RegisterStudentPage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Register Student", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

        self.student_name_label = tk.Label(self, text="Student Name:", font=("Arial", 16), bg="#f0f0f0")
        self.student_name_label.pack()
        self.student_name_entry = tk.Entry(self, font=("Arial", 16))
        self.student_name_entry.pack()

        self.student_id_label = tk.Label(self, text="Student ID:", font=("Arial", 16), bg="#f0f0f0")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self, font=("Arial", 16))
        self.student_id_entry.pack()

        self.cafe_access_label = tk.Label(self, text="Cafe Access (yes/no):", font=("Arial", 16), bg="#f0f0f0")
        self.cafe_access_label.pack()
        self.cafe_access_entry = tk.Entry(self, font=("Arial", 16))
        self.cafe_access_entry.pack()

        self.register_student_button = tk.Button(self, text="Register Student", font=("Arial", 14), command=self.register_student)
        self.register_student_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.back_button.pack()

    def register_student(self):
        student_name = self.student_name_entry.get()
        student_id = self.student_id_entry.get()
        cafe_access = self.cafe_access_entry.get().lower()

        if student_name.strip() == "":
            messagebox.showerror("Error", "Please enter student name")
            return

        if student_id.strip() == "":
            messagebox.showerror("Error", "Please enter student ID")
            return

        if cafe_access not in ['yes', 'no']:
            messagebox.showerror("Error", "Cafe access must be 'yes' or 'no'")
            return

        students[student_id] = {'name': student_name, 'cafe_access': cafe_access, 'last_access': None}
        messagebox.showinfo("Success", "Student registered successfully.")

class CheckAccessPage(Page):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Check Student Access", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

        self.student_id_label = tk.Label(self, text="Student ID:", font=("Arial", 16), bg="#f0f0f0")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self, font=("Arial", 16))
        self.student_id_entry.pack()

        self.check_access_button = tk.Button(self, text="Check Student Access", font=("Arial", 14), command=self.check_access)
        self.check_access_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back to Home", font=("Arial", 14), command=self.back_to_home)
        self.back_button.pack()

    def check_access(self):
        student_id = self.student_id_entry.get()
        if student_id in students:
            if students[student_id]['cafe_access'] == 'yes':
                last_access = students[student_id]['last_access']
                if last_access == None:
                    students[student_id]['last_access'] = 'lunch'
                    messagebox.showinfo("Access Granted", "Access granted.")
                else:
                    messagebox.showerror("Error", "You have already used your access.")
            else:
                messagebox.showinfo("Non-Cafe User", "You are a non-cafe user.")
        else:
            messagebox.showerror("Error", "First you have to register.")

if __name__ == "__main__":
    app = CafeManagementSystem()
    app.mainloop()

