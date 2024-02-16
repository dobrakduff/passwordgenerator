from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)


def generate_pass():
    p_en.delete(0,END)
    pass_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    pass_letters = [random.choice(letters) for _ in range(nr_letters)]
    pass_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = pass_symbols + pass_letters + pass_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    pyperclip.copy(password)

    p_en.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = w_en.get()
    email = u_en.get()
    password = p_en.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            w_en.delete(0, END)
            p_en.delete(0, END)

# ------------------------- FIND PASSWORD ----------------------------- #
def find_password():
    website = w_en.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(message=f"NO DATA FILE FOUND")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(message=f"No details oft {website} exist")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("PASSWORD GENERATOR")
window.config(pady=20,padx=20)

canvas = Canvas(height=200,width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0,column=1)
#web label
w_l=Label(text="WEBSITE:")
w_l.grid(row=1,column=0)

w_en = Entry(width=21)
w_en.insert(END, string="")
w_en.focus()
w_en.grid(row=1,column=1)

u_l=Label(text="USERNAME/MAIL:")
u_l.grid(row=2,column=0)

u_en = Entry(width=35)
u_en.insert(END, string="")
u_en.grid(row=2,column=1,columnspan=2)

p_l=Label(text="PASSWORD")
p_l.grid(row=3,column=0)

p_en = Entry(width=21)
p_en.insert(END, string="")
p_en.grid(row=3,column=1)

p_b = Button(text="GENERATE PASSWORD", command=generate_pass)
p_b.grid(row=3,column=2)

a_b = Button(text="ADD", command=save)
a_b.grid(row=4,column=1,columnspan=2)

s_b = Button(text="SEARCH", command=find_password,width=13)
s_b.grid(row=1,column=2)
window.mainloop()