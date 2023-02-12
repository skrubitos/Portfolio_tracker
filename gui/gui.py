import tkinter as tk

def login_window():
    def submit():
        username = username_entry.get()
        password = password_entry.get()
        if login(username, password):
            login_success_label.config(text="Login Successful")
        else:
            login_success_label.config(text="Login Failed")
            
    login_window = tk.Tk()
    login_window.title("Login")
    
    username_label = tk.Label(login_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)
    
    password_label = tk.Label(login_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)
    
    submit_button = tk.Button(login_window, text="Submit", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2)
    
    login_success_label = tk.Label(login_window)
    login_success_label.grid(row=3, column=0, columnspan=2)
    
    login_window.mainloop()
    
login_window()
