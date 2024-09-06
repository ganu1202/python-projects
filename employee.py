import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate
import mysql.connector
from decimal import Decimal


# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ganu@1202",
    database="emp"
)

def check_employee(employee_id):
    sql = 'SELECT * FROM employees WHERE id=%s'
    cursor = con.cursor(buffered=True)
    data = (employee_id,)
    cursor.execute(sql, data)
    employee = cursor.fetchone()
    cursor.close()
    return employee is not None

def add_employee():
    Id = entry_id.get()
    if check_employee(Id):
        messagebox.showerror("Error", "Employee already exists. Please try again.")
        return

    Name = entry_name.get()
    Post = entry_post.get()
    Salary = entry_salary.get()

    sql = 'INSERT INTO employees (id, name, position, salary) VALUES (%s, %s, %s, %s)'
    data = (Id, Name, Post, Salary)
    cursor = con.cursor()

    try:
        cursor.execute(sql, data)
        con.commit()
        messagebox.showinfo("Success", "Employee Added Successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        con.rollback()
    finally:
        cursor.close()

def remove_employee():
    Id = entry_id.get()
    if not check_employee(Id):
        messagebox.showerror("Error", "Employee does not exist. Please try again.")
        return
    
    sql = 'DELETE FROM employees WHERE id=%s'
    data = (Id,)
    cursor = con.cursor()

    try:
        cursor.execute(sql, data)
        con.commit()
        messagebox.showinfo("Success", "Employee Removed Successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        con.rollback()
    finally:
        cursor.close()


def promote_employee():
    Id = entry_id.get()
    if not check_employee(Id):
        messagebox.showerror("Error", "Employee does not exist. Please try again.")
        return
    
    try:
        Amount = Decimal(entry_salary.get())  # Convert to Decimal
        new_position = entry_post.get()  # Get the new position

        sql_select = 'SELECT salary FROM employees WHERE id=%s'
        cursor = con.cursor(buffered=True)
        cursor.execute(sql_select, (Id,))
        current_salary = cursor.fetchone()[0]
        new_salary = current_salary + Amount

        sql_update = 'UPDATE employees SET salary=%s, position=%s WHERE id=%s'
        cursor.execute(sql_update, (new_salary, new_position, Id))
        con.commit()
        messagebox.showinfo("Success", "Employee Promoted Successfully")
    except (ValueError, mysql.connector.Error) as e:
        messagebox.showerror("Error", f"Error: {e}")
        con.rollback()
    finally:
        cursor.close()



def display_employees():
    try:
        sql = 'SELECT * FROM employees'
        cursor = con.cursor(buffered=True)
        cursor.execute(sql)
        employees = cursor.fetchall()

        headers = ["Employee Id", "Employee Name", "Employee Post", "Employee Salary"]
        table = tabulate(employees, headers=headers, tablefmt="grid")

        # Show table in a new window
        new_window = tk.Toplevel(root)
        new_window.title("Employee List")
        new_window.geometry("850x400")


        text_area = tk.Text(new_window, wrap='word', height=20, width=140,font=("Courier", 12), bg="#f8f8f8", fg="#333333")
        text_area.insert(tk.END, table)
        text_area.config(state=tk.DISABLED)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

# Create main window
root = tk.Tk()


input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Set window size
root.geometry("850x400")
root.configure(bg="#f0f0f0")

tk.Label(input_frame, text="Employee Id:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_id = tk.Entry(input_frame, width=50)
entry_id.grid(row=0, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Employee Name:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_name = tk.Entry(input_frame, width=50)
entry_name.grid(row=1, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Employee Post:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_post = tk.Entry(input_frame, width=50)
entry_post.grid(row=2, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Employee Salary:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='e')
entry_salary = tk.Entry(input_frame, width=50)
entry_salary.grid(row=3, column=1, padx=10, pady=10)

font_style = ('Helvetica', 12, 'bold')


# Place buttons in the button frame
tk.Button(button_frame, text="Add Employee", command=add_employee, bg="#4CAF50", fg="white", font=font_style).grid(row=0, column=0, padx=10, pady=15)
tk.Button(button_frame, text="Remove Employee", command=remove_employee, bg="#f44336", fg="white", font=font_style).grid(row=0, column=1, padx=10, pady=15)
tk.Button(button_frame, text="Promote Employee", command=promote_employee, bg="#2196F3", fg="white", font=font_style).grid(row=0, column=2, padx=10, pady=15)
tk.Button(button_frame, text="Display Employees", command=display_employees, bg="#FFC107", fg="white", font=font_style).grid(row=0, column=3, padx=10, pady=15)

# Define buttons with bold text and consistent spacing

# tk.Button(root, text="Add Employee", command=add_employee, bg="#4CAF50", fg="white", font=font_style).grid(row=4, column=0, padx=10, pady=15, sticky='ew')
# tk.Button(root, text="Remove Employee", command=remove_employee, bg="#f44336", fg="white", font=font_style).grid(row=4, column=1, padx=10, pady=15, sticky='ew')
# tk.Button(root, text="Promote Employee", command=promote_employee, bg="#2196F3", fg="white", font=font_style).grid(row=4, column=2, padx=10, pady=15, sticky='ew')
# tk.Button(root, text="Display Employees", command=display_employees, bg="#FFC107", fg="white", font=font_style).grid(row=4, column=3, padx=10, pady=15, sticky='ew')

# Configure column weights to allow resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.title("Employee Management System")
# root.iconbitmap('logo.ico')  # Set a .ico file for the application icon




# Run the application
root.mainloop()
