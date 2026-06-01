from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# ================= DATABASE =================

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lalkumbla12",
        database="railway"
    )

# ================= MAIN WINDOW =================

root = Tk()
root.title("Railway Ticket Booking System")
root.geometry("900x600")
root.resizable(False, False)

# ================= BACKGROUND IMAGE =================

try:
    bg = Image.open("bg.jpg")
    bg = bg.resize((900, 600))
    bg_image = ImageTk.PhotoImage(bg)

    bg_label = Label(root, image=bg_image)
    bg_label.place(x=0, y=0)
except:
    root.configure(bg="lightblue")

# ================= TITLE =================

Label(
    root,
    text="Railway Ticket Booking System",
    font=("Arial", 22, "bold"),
    bg="black",
    fg="white"
).pack(pady=15)

# ================= FUNCTIONS =================

def clear_fields():
    name_entry.delete(0, END)
    train_entry.delete(0, END)
    seat_entry.delete(0, END)
    cancel_entry.delete(0, END)


def view_trains():
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM trains")
        trains = cursor.fetchall()

        result = ""

        for row in trains:
            result += f"""
Train No : {row[0]}
Train Name : {row[1]}
From : {row[2]}
To : {row[3]}
Seats : {row[4]}
Price : ₹{row[5]}

"""

        if result == "":
            result = "No Trains Available"

        messagebox.showinfo("Train List", result)

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def book_ticket():

    try:

        name = name_entry.get()

        if name == "":
            messagebox.showerror("Error", "Enter Passenger Name")
            return

        train_no = int(train_entry.get())
        seats = int(seat_entry.get())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT seats, price FROM trains WHERE train_no=%s",
            (train_no,)
        )

        train = cursor.fetchone()

        if train:

            available = train[0]
            price = train[1]

            if seats <= available:

                total = seats * price

                cursor.execute(
                    """
                    INSERT INTO bookings
                    (passenger_name, train_no, seats_booked, total_price)
                    VALUES (%s,%s,%s,%s)
                    """,
                    (name, train_no, seats, total)
                )

                booking_id = cursor.lastrowid

                cursor.execute(
                    """
                    UPDATE trains
                    SET seats = seats - %s
                    WHERE train_no=%s
                    """,
                    (seats, train_no)
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    f"""
Booking Successful

Booking ID : {booking_id}
Passenger : {name}
Train No : {train_no}
Seats : {seats}
Total Price : ₹{total}
"""
                )

                clear_fields()

            else:
                messagebox.showerror(
                    "Error",
                    "Seats Not Available"
                )

        else:
            messagebox.showerror(
                "Error",
                "Train Not Found"
            )

        conn.close()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter Valid Numbers"
        )


def cancel_ticket():

    try:

        booking_id = int(cancel_entry.get())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT train_no,seats_booked
            FROM bookings
            WHERE booking_id=%s
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()

        if booking:

            train_no = booking[0]
            seats = booking[1]

            cursor.execute(
                """
                UPDATE trains
                SET seats = seats + %s
                WHERE train_no=%s
                """,
                (seats, train_no)
            )

            cursor.execute(
                """
                DELETE FROM bookings
                WHERE booking_id=%s
                """,
                (booking_id,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Ticket Cancelled Successfully"
            )

            clear_fields()

        else:
            messagebox.showerror(
                "Error",
                "Invalid Booking ID"
            )

        conn.close()

    except:
        messagebox.showerror(
            "Error",
            "Enter Valid Booking ID"
        )


def seat_check():

    try:

        train_no = int(train_entry.get())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT seats FROM trains WHERE train_no=%s",
            (train_no,)
        )

        result = cursor.fetchone()

        if result:
            messagebox.showinfo(
                "Seat Availability",
                f"Available Seats : {result[0]}"
            )
        else:
            messagebox.showerror(
                "Error",
                "Train Not Found"
            )

        conn.close()

    except:
        messagebox.showerror(
            "Error",
            "Enter Train Number"
        )


def price_calculator():

    try:

        train_no = int(train_entry.get())
        seats = int(seat_entry.get())

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT price FROM trains WHERE train_no=%s",
            (train_no,)
        )

        result = cursor.fetchone()

        if result:

            total = result[0] * seats

            messagebox.showinfo(
                "Price",
                f"Total Price = ₹{total}"
            )

        else:
            messagebox.showerror(
                "Error",
                "Train Not Found"
            )

        conn.close()

    except:
        messagebox.showerror(
            "Error",
            "Enter Valid Details"
        )


def view_bookings():

    try:

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings")

        bookings = cursor.fetchall()

        result = ""

        for row in bookings:

            result += f"""
Booking ID : {row[0]}
Passenger : {row[1]}
Train No : {row[2]}
Seats : {row[3]}
Price : ₹{row[4]}

"""

        if result == "":
            result = "No Bookings Found"

        messagebox.showinfo(
            "Bookings",
            result
        )

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ================= FORM =================

form = Frame(root, bg="white")
form.place(x=250, y=100, width=400, height=420)

Label(form, text="Passenger Name").pack(pady=5)
name_entry = Entry(form, width=30)
name_entry.pack()

Label(form, text="Train Number").pack(pady=5)
train_entry = Entry(form, width=30)
train_entry.pack()

Label(form, text="Seats").pack(pady=5)
seat_entry = Entry(form, width=30)
seat_entry.pack()

Label(form, text="Cancel Booking ID").pack(pady=5)
cancel_entry = Entry(form, width=30)
cancel_entry.pack()

# ================= BUTTONS =================

Button(
    form,
    text="View Trains",
    width=20,
    bg="blue",
    fg="white",
    command=view_trains
).pack(pady=4)

Button(
    form,
    text="Book Ticket",
    width=20,
    bg="green",
    fg="white",
    command=book_ticket
).pack(pady=4)

Button(
    form,
    text="Cancel Ticket",
    width=20,
    bg="red",
    fg="white",
    command=cancel_ticket
).pack(pady=4)

Button(
    form,
    text="Seat Availability",
    width=20,
    bg="orange",
    fg="white",
    command=seat_check
).pack(pady=4)

Button(
    form,
    text="Price Calculator",
    width=20,
    bg="purple",
    fg="white",
    command=price_calculator
).pack(pady=4)

Button(
    form,
    text="View Bookings",
    width=20,
    bg="brown",
    fg="white",
    command=view_bookings
).pack(pady=4)

root.mainloop()