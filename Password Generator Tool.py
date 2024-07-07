import tkinter as tk
import random 
import string

def generate_password(length):

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

def generate_display_password():
    try:
        length = int(length_entry.get())
        password = generate_password(length)
        password_var.set(password)
    except ValueError:
        password_var.set("Invalid length")
    
root = tk.Tk()
root.title("Password Generator")
root.geometry('500x300')
root.config(bg='#C0C0C0')

font1=('Times New Roman',25,'bold','italic')
font2=('Times New Roman',15,'bold')
font3=('Times New Roman',10,'bold')

length_label=el = tk.Label(root, text="Enter length of Password",font=font1,fg='#000000',bg='#C0C0C0',width=80)
length_label.pack(pady=(20,20))

length_entry = tk.Entry(root,bg='#C9F4F2',font=font2,fg='#000000',width=20)
length_entry.pack(pady=(0, 10), padx=10)

generate_button = tk.Button(root, text="Generate Password",command=generate_display_password, bg='#DB7093',fg='#000000', cursor='hand2',font=font3)
generate_button.pack(pady=(0, 10))

password_var = tk.StringVar()
password_label = tk.Label(root, textvariable=password_var, wraplength=300,bg='#000000',fg='#62F6EF',font=font1)
password_label.pack()

root.mainloop()

