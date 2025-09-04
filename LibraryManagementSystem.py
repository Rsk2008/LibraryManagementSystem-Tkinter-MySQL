# Library Management System with Tkinter + MySQL + Role-Based Access

import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# ----------------- Database Connection -----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rashmi_123",
    database="librarydb"
)
cursor = conn.cursor()


# ----------------- Feature Windows -----------------
def add_book_window(root, role):
    win = tk.Toplevel(root)
    win.title("Add Book")
    win.geometry("400x400")

    tk.Label(win, text="Book Title").pack(pady=5)
    entry_title = tk.Entry(win); entry_title.pack(pady=5)

    tk.Label(win, text="Author").pack(pady=5)
    entry_author = tk.Entry(win); entry_author.pack(pady=5)

    tk.Label(win, text="ISBN").pack(pady=5)
    entry_isbn = tk.Entry(win); entry_isbn.pack(pady=5)

    tk.Label(win, text="Category").pack(pady=5)
    entry_category = tk.Entry(win); entry_category.pack(pady=5)

    tk.Label(win, text="Quantity").pack(pady=5)
    entry_quantity = tk.Entry(win); entry_quantity.pack(pady=5)

    def save_book():
        Book_Title = entry_title.get()
        Author = entry_author.get()
        ISBN = entry_isbn.get()
        category = entry_category.get()
        Quantity = entry_quantity.get()

        if Book_Title and Author and ISBN and category and Quantity:
            try:
                cursor.execute(
                    "INSERT INTO Books (Title, Author, ISBN, Category, Quantity) VALUES (%s, %s, %s, %s, %s)",
                    (Book_Title, Author, ISBN, category, int(Quantity))
                )
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book\n{e}", parent=win)
        else:
            messagebox.showwarning("Input Error", "All fields are required!", parent=win)

    tk.Button(win, text="Add Book", command=save_book).pack(pady=10)
    tk.Button(win, text="Back to Menu", fg="red", command=win.destroy).pack(pady=5)


def view_books_window(root, role):
    win = tk.Toplevel(root)
    win.title("View Books")
    win.geometry("700x450")

    tk.Label(win, text="Enter Book ID (leave empty to view all)").pack(pady=5)
    entry_book_id = tk.Entry(win)
    entry_book_id.pack(pady=5)

    columns = ("BookID", "Title", "Author", "ISBN", "Category", "Quantity")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=10, fill="both", expand=True)

    def search_book():
        BookID = entry_book_id.get()
        try:
            if BookID:
                cursor.execute("SELECT * FROM Books WHERE BookID=%s", (BookID,))
            else:
                cursor.execute("SELECT * FROM Books")
            result = cursor.fetchall()

            for row in tree.get_children():
                tree.delete(row)

            if result:
                for row in result:
                    tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Not Found", "No books found", parent=win)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data\n{e}", parent=win)

    tk.Button(win, text="Search", command=search_book).pack(pady=5)
    tk.Button(win, text="Back to Menu", fg="red", command=win.destroy).pack(pady=5)


def add_member_window(root, role):
    win = tk.Toplevel(root)
    win.title("Add Member")
    win.geometry("400x400")

    tk.Label(win, text="Member ID").pack(pady=5)
    entry_mid = tk.Entry(win); entry_mid.pack(pady=5)

    tk.Label(win, text="Name").pack(pady=5)
    entry_name = tk.Entry(win); entry_name.pack(pady=5)

    tk.Label(win, text="Email").pack(pady=5)
    entry_email = tk.Entry(win); entry_email.pack(pady=5)

    tk.Label(win, text="Phone").pack(pady=5)
    entry_phone = tk.Entry(win); entry_phone.pack(pady=5)

    tk.Label(win, text="Membership Date (YYYY-MM-DD)").pack(pady=5)
    entry_date = tk.Entry(win); entry_date.pack(pady=5)

    def save_member():
        try:
            MID = int(entry_mid.get())
            Name = entry_name.get()
            Email = entry_email.get()
            Phone = int(entry_phone.get())
            Date = entry_date.get()

            cursor.execute(
                "INSERT INTO Members (MemberID, Name, Email, Phone, MembershipDate) VALUES (%s, %s, %s, %s, %s)",
                (MID, Name, Email, Phone, Date)
            )
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully!", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add member\n{e}", parent=win)

    tk.Button(win, text="Add Member", command=save_member).pack(pady=10)
    tk.Button(win, text="Back to Menu", fg="red", command=win.destroy).pack(pady=5)


def borrow_book_window(root, role):
    win = tk.Toplevel(root)
    win.title("Borrow Book")
    win.geometry("400x400")

    tk.Label(win, text="Book ID").pack(pady=5)
    entry_bid = tk.Entry(win); entry_bid.pack(pady=5)

    tk.Label(win, text="Member ID").pack(pady=5)
    entry_mid = tk.Entry(win); entry_mid.pack(pady=5)

    tk.Label(win, text="Issue Date (YYYY-MM-DD)").pack(pady=5)
    entry_issue = tk.Entry(win); entry_issue.pack(pady=5)

    tk.Label(win, text="Due Date (YYYY-MM-DD)").pack(pady=5)
    entry_due = tk.Entry(win); entry_due.pack(pady=5)

    def save_borrow():
        try:
            BID = int(entry_bid.get())
            MID = int(entry_mid.get())
            IssueDate = entry_issue.get()
            DueDate = entry_due.get()

            cursor.execute(
                "INSERT INTO transactions (BookID, MemberID, IssueDate, DueDate) VALUES (%s, %s, %s, %s)",
                (BID, MID, IssueDate, DueDate)
            )
            conn.commit()
            messagebox.showinfo("Success", "Book borrowed successfully!", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to borrow book\n{e}", parent=win)

    tk.Button(win, text="Borrow Book", command=save_borrow).pack(pady=10)
    tk.Button(win, text="Back to Menu", fg="red", command=win.destroy).pack(pady=5)


def return_book_window(root, role):
    win = tk.Toplevel(root)
    win.title("Return Book")
    win.geometry("400x400")

    tk.Label(win, text="Member ID").pack(pady=5)
    entry_mid = tk.Entry(win); entry_mid.pack(pady=5)

    tk.Label(win, text="Book ID").pack(pady=5)
    entry_bid = tk.Entry(win); entry_bid.pack(pady=5)

    tk.Label(win, text="Return Date (YYYY-MM-DD)").pack(pady=5)
    entry_return = tk.Entry(win); entry_return.pack(pady=5)

    def save_return():
        try:
            MID = int(entry_mid.get())
            BID = int(entry_bid.get())
            ReturnDate_str = entry_return.get()
            ReturnDate = datetime.strptime(ReturnDate_str, "%Y-%m-%d").date()

            cursor.execute("SELECT * FROM transactions WHERE BookID=%s AND MemberID=%s", (BID, MID))
            result = cursor.fetchall()

            if not result:
                messagebox.showwarning("Not Found", "No transaction found.", parent=win)
                return

            DueDate = result[0][4]
            if isinstance(DueDate, str):
                DueDate = datetime.strptime(DueDate, "%Y-%m-%d").date()

            fine = (ReturnDate - DueDate).days * 1 if ReturnDate > DueDate else 0

            cursor.execute(
                "UPDATE transactions SET ReturnDate=%s, Fine=%s WHERE BookID=%s AND MemberID=%s",
                (ReturnDate.strftime('%Y-%m-%d'), fine, BID, MID)
            )
            conn.commit()

            if fine > 0:
                messagebox.showinfo("Return Success", f"Book returned with fine: ${fine}", parent=win)
            else:
                messagebox.showinfo("Return Success", "Book returned on time.", parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book\n{e}", parent=win)

    tk.Button(win, text="Return Book", command=save_return).pack(pady=10)
    tk.Button(win, text="Back to Menu", fg="red", command=win.destroy).pack(pady=5)


# ----------------- Main Menu -----------------
def main_menu(role, root):
    win = tk.Toplevel(root)
    win.title("Library Management System")
    win.geometry("400x400")

    tk.Label(win, text=f"Welcome, {role}", font=("Arial", 16, "bold")).pack(pady=20)

    if role == "Admin":
        tk.Button(win, text="Add Book", width=25, command=lambda: add_book_window(root, role)).pack(pady=5)
        tk.Button(win, text="View Books", width=25, command=lambda: view_books_window(root, role)).pack(pady=5)
        tk.Button(win, text="Add Member", width=25, command=lambda: add_member_window(root, role)).pack(pady=5)
        tk.Button(win, text="Borrow Book", width=25, command=lambda: borrow_book_window(root, role)).pack(pady=5)
        tk.Button(win, text="Return Book", width=25, command=lambda: return_book_window(root, role)).pack(pady=5)

    elif role == "User":
        tk.Button(win, text="View Books", width=25, command=lambda: view_books_window(root, role)).pack(pady=5)
        tk.Button(win, text="Borrow Book", width=25, command=lambda: borrow_book_window(root, role)).pack(pady=5)
        tk.Button(win, text="Return Book", width=25, command=lambda: return_book_window(root, role)).pack(pady=5)

    # Logout button -> close menu and show login again
    tk.Button(
        win, text="Logout to Login Page", width=25, fg="red",
        command=lambda: [win.destroy(), root.deiconify()]
    ).pack(pady=20)


# ----------------- Login Window -----------------
def login_window():
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x200")

    tk.Label(root, text="Select Role", font=("Arial", 14)).pack(pady=20)

    tk.Button(
        root, text="Admin", width=15,
        command=lambda: [root.withdraw(), main_menu("Admin", root)]
    ).pack(pady=10)

    tk.Button(
        root, text="User", width=15,
        command=lambda: [root.withdraw(), main_menu("User", root)]
    ).pack(pady=10)

    # Optional: Quit program entirely from login
    tk.Button(root, text="Exit", width=15, fg="red", command=root.destroy).pack(pady=10)

    root.mainloop()


# ----------------- Run -----------------
if __name__ == "__main__":
    login_window()

