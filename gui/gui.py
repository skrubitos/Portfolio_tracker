def show_user():
    global user_list_window
    # Create a new window to display the user list
    user_list_window = tk.Toplevel(root)
    user_list_window.geometry("300x400")
    user_list_window.title("List of Users")
    cur.execute("SELECT name, timestamp FROM user")
    result = cur.fetchall()
    if len(result) < 1:
        messagebox.showinfo("User List", "No users yet")
    else:
        user_data = ""
        for j in range(len(result)):
            user_data += f"User {j+1}: {result[j][0]} (Registered: {result[j][1]})\n"
        user_window = tk.Toplevel(root)
        user_window.title("User List")
        user_label = tk.Label(user_window, text=user_data, justify="left")
        user_label.pack(padx=10, pady=10)

        
def toggle_user_list():
    global user_list_displayed
    if user_list_displayed:
        # If the user list is currently displayed, hide it and update the flag
        show_users_button.destroy()
        user_list_displayed = False
    else:
        # If the user list is not displayed, show it and update the flag
        show_user()
        user_list_displayed = True

show_users_button = tk.Button(input_frame, text="Show Users", command=toggle_user_list)
show_users_button.grid(row=2, column=2, padx=10, pady=10)
