import ds_messenger
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


class MainAppError(Exception):
    pass

class Body(tk.Frame):
    """
    Manages widgets in the body of the main frame.
    """
    def __init__(self, root, display):
        """
        :param root: the main window of the Tkinter program
        :param display: display_messages method in MainApp class
        """
        self.root = root
        self.display = display
        self.selected_user = None
        
        self.draw()
        self.list_users = []


    def reset_ui(self) -> None:
        """
        Resets users_tree treeview whenever new user logged in.
        :return: None
        """
        self.set_text_frame_entry("")
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)


    def display_text(self, msg:str) -> None:
        """
        Adds messages to msgs_box widget.
        :param msg: message from selected user to be displayed
        """
        self.msgs_box.config(state='normal')
        self.msgs_box.insert('0.0', msg)
        self.msgs_box.config(state='disabled')


    def clear_display(self) -> None:
        """
        Clears all messages in msgs_box widget when other user selected.
        """
        self.msgs_box.config(state='normal')
        self.msgs_box.delete('0.0', 'end')
        self.msgs_box.config(state='disabled')    
        

    def node_select(self, event):
        """
        Selects user from users_tree treeview widget.
        """
        index = int(self.users_tree.selection()[0])-1 # -1 because selections not 0-based
        self.selected_user = self.list_users[index]
        self.clear_display()
        self.display()


    def add_new_user(self, user) -> None:
        """
        Adds new users to users_tree treeview widget.
        """
        if user not in self.list_users:
            self.list_users.append(user)
            id = len(self.list_users)
            self.users_tree.insert('', id, id, text=user)


    def set_users(self, users) -> None:
        """
        Displays all senders to users_tree treeview widget.
        :return: None
        """
        self.list_users = []
        self.reset_ui()
        self.clear_display()
        for user in users:
            self.add_new_user(user['from'])


    def set_text_frame_entry(self, text:str) -> None:
        """
        Sets the text to be displayed in the text_editor widget.
        :return: None
        """
        self.text_editor.delete('0.0', 'end')
        self.text_editor.insert('0.0', text)


    def get_text_frame_entry(self) -> str:
        """
        Returns the text that is currently displayed in the text_editor widget.
        :return: message user wants to send
        """
        return self.text_editor.get('1.0', 'end').rstrip()


    def draw(self) -> None:
        """
        Creates body frame and adds widgets.
        :return: None
        """
        body_frame = tk.Frame(master=self.root, bg='light grey')
        body_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        users_frame = tk.Frame(master=body_frame, width=250, bg='light grey')
        users_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.users_tree = ttk.Treeview(users_frame)
        self.users_tree.bind('<<TreeviewSelect>>', self.node_select)
        self.users_tree.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=10, expand=True)

        text_frame = tk.Frame(master=body_frame, width=490, height=350)
        text_frame.pack(fill=tk.Y, side=tk.TOP, padx=10, pady=10, expand=True)
        self.msgs_box = tk.Text(master=text_frame, state='disabled', cursor='arrow')
        self.msgs_box.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        send_frame = tk.Frame(master=body_frame, width=490, height=100)
        send_frame.pack(fill=tk.Y, side=tk.BOTTOM, padx=10, pady=10, expand=True)
        self.text_editor = tk.Text(master=send_frame)
        self.text_editor.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)


class Footer(tk.Frame):
    """
    Manages widgets in the footer of the main frame.
    """
    def __init__(self, root, add_user, send_msg, update):
        """
        :param root: the main window of the Tkinter program
        :param add_user: add_user method in MainApp class
        :param send_msg: send_msg method in MainApp class
        :param update: update method in MainApp class
        """
        self.root = root
        self.add_user = add_user
        self.send_msg = send_msg
        self.update = update
        self.draw()

    
    def add_user_entry(self) -> None:
        """
        Opens a popup window when add_user_button clicked.
        User can enter a new username to send to.
        :return: None
        """
        self.new_user = simpledialog.askstring('Add a User', 'Enter a Username:')
        if self.new_user is not None:
            self.add_user()


    def send_post(self) -> None:
        """
        Calls send_msg method in MainApp class when user clicks the Send button.
        :return: None
        """
        self.send_msg()


    def reload(self) -> None:
        """
        Updates messages to current time.
        :return: None
        """
        self.update()


    def draw(self) -> None:
        """
        Creates footer frame and adds widgets.
        :return: None
        """
        footer_frame = tk.Frame(master=self.root, bg='gray')
        footer_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        add_user_button = tk.Button(master=footer_frame, text='Add User')
        add_user_button.configure(command=self.add_user_entry)
        add_user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)

        send_button = tk.Button(master=footer_frame, text='Send', width=10)
        send_button.configure(command=self.send_post)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=10, pady=5)

        reload_button = tk.Button(master=footer_frame, text='Load New Messages')
        reload_button.configure(command=self.reload)
        reload_button.pack(fill=tk.BOTH, padx=180, pady=5)


class MainApp(tk.Frame):
    """
    Draws widgets in main frame.
    Interacts with Body class and Footer class.
    """
    def __init__(self, root):
        """
        :param root: the main window of the Tkinter program
        """
        self.root = root
        self.user = None

        self.draw_main()
        self.draw_user_window()


    def add_user(self) -> None:
        """
        Calls set_user method in Body class to add new users to treewidget.
        :return: None
        """
        try:
            if self.user is None:
                raise Exception
            self.body.add_new_user(self.footer.new_user)
        except Exception:
            self.error_window('Not logged in.')       


    def send_msg(self) -> None:
        """
        Sends message to another user.
        Clears text_frame when message sent.
        :return: None
        """
        try:
            message = self.body.get_text_frame_entry()
            if self.user is None:
                raise Exception
            elif self.body.selected_user is None:
                raise AttributeError
            self.user.send(message, self.body.selected_user)
            self.body.set_text_frame_entry('')
        except TimeoutError:
            self.error_window('Timed out.')
        except AttributeError:
            self.error_window('Select a user.')
        except Exception:
            self.error_window('Not logged in.')


    def display_messages(self) -> None:
        """
        Calls display_text method in Body Class to display messages in msgs_box widget.
        :return: None
        """
        try:
            all_messages = self.user.retrieve_all()
            all_messages.reverse()
            mailbox = False
            for msg in all_messages:
                if self.body.selected_user == msg['from']:
                    display_msg = msg['message'] + '\n'
                    self.body.display_text(display_msg)
                    mailbox = True
            if mailbox is False:
                self.body.display_text('(No messages)')
        except TimeoutError:
            self.error_window('Timed out.')
        except AttributeError:
            self.error_window('Not logged in.')


    def close(self) -> None:
        """
        Closes the program when the 'Close' menu item is clicked.
        :return: None
        """
        self.root.destroy()

    
    def connect(self) -> None:
        """
        Connects user's information to server.
        Then sets treeview if connected.
        :return: None
        """
        try:
            self.username = self.input_username.get().rstrip()
            self.password = self.input_password.get().rstrip()
            self.user = ds_messenger.DirectMessenger(ds_messenger.HOST, self.username, self.password)
            self.user_messages = self.user.retrieve_all()
            self.body.set_users(self.user_messages)
            self.body.selected_user = None
            self.user_info_window.destroy() #exit login window once connected
        except TimeoutError:
            self.error_window('Timed out.')
        except Exception:
            self.error_window('Invalid username and/ or password.')


    def update(self) -> None:
        """
        Updates users_tree treewidget to show current messages.
        :return: None
        """
        try:
            self.body.reset_ui() #reset ui so no repeats in users_tree
            self.user_messages = self.user.retrieve_all()
            self.body.set_users(self.user_messages)
            self.body.selected_user = None
        except TimeoutError:
            self.error_window('Timed out.')
        except AttributeError:
            self.error_window('Not logged in.')


    def error_window(self, error: str) -> None:
        """
        Displays error popup window when error occurs.
        :error: error message
        :return: None
        """
        messagebox.showinfo(title='ERROR', message=error)

        
    def draw_user_window(self) -> None:
        """
        Adds widgets when Switch Users clicked from menu bar.
        :return: None
        """
        self.user_info_window = tk.Toplevel()
        self.user_info_window.title('Create a User or Log In')
        self.user_info_window.geometry('420x95')
        self.user_info_window.option_add('*tearOff', False)
        self.user_info_window.update()
        self.user_info_window.minsize(self.user_info_window.winfo_width(), self.user_info_window.winfo_height())
        self.user_info_window.maxsize(self.user_info_window.winfo_width(), self.user_info_window.winfo_height())

        user_info_footer = tk.Frame(master=self.user_info_window, height='25', bg='gray')
        user_info_footer.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        connect_button = tk.Button(master=user_info_footer, text='Connect')
        connect_button.configure(command=self.connect)
        connect_button.pack(fill=tk.BOTH, padx=150, pady=10, expand=True)

        user_username_frame = tk.Frame(master=self.user_info_window)
        user_username_frame.pack(fill=tk.X, side=tk.TOP, expand=True)
        user_text = tk.Label(master=user_username_frame, text='Username:')
        user_text.pack(fill=tk.X, side=tk.LEFT, expand=False)

        user_password_frame = tk.Frame(master=self.user_info_window)
        user_password_frame.pack(fill=tk.X, side=tk.TOP, expand=True)
        password_text = tk.Label(master=user_password_frame, text='Password:')
        password_text.pack(fill=tk.X, side=tk.LEFT, expand=False)

        self.input_username = tk.Entry(master=user_username_frame)
        self.input_username.pack(fill=tk.X, side=tk.TOP, padx=5, expand=True)
        self.input_password = tk.Entry(master=user_password_frame)
        self.input_password.pack(fill=tk.X, side=tk.BOTTOM, padx=5, expand=True)

        create_frame = tk.Frame(master=self.user_info_window, width='240')
        create_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)


    def draw_main(self) -> None:
        """
        Adds widgets to main frame.
        :return: None
        """
        self.footer = Footer(self.root, self.add_user, self.send_msg, self.update)
        self.body = Body(self.root, self.display_messages)
        
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_user = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_user, label='User')
        menu_user.add_command(label='Switch Users', command=self.draw_user_window)
        menu_user.add_command(label='Quit', command=self.close)


if __name__ == '__main__':
    main_window = tk.Tk()
    main_window.title('ICS 32 MESSENGER')
    main_window.geometry('720x500')
    main_window.option_add('*tearOff', False)

    MainApp(main_window)
    main_window.update()
    main_window.minsize(main_window.winfo_width(), main_window.winfo_height())

    main_window.mainloop()

