import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Profile, Post
from NaClProfile import NaClProfile

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):

    class BodyError(Exception):
        pass

    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Post]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()

    def curr_index(self) -> int:
        """
        Return the current selected index of post in the post tree view.
        :return: the index
        """
        try:
            index = int(self.posts_tree.selection()[0])
        except IndexError as e:
            if str(e) == 'tuple index out of range':
                raise self.BodyError('There is nothing in the posts_tree widget') from e
        return index
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].get_entry()
        title = self._posts[index].get_title()
        self.set_text_entry(title + '\n' + entry)

    def get_text_entry(self) -> list:
        """
        Returns the title and text that is currently displayed in the entry_editor widget.
        :return: a list, the first slot is the title of the post (the first line)
        the second slot is the entry text
        """
        entry = self.entry_editor.get('1.0', 'end').rstrip()
        entry = entry.split('\n', 1)
        # when the entry_editor widget is empty
        if len(entry) == 0:
            entry.append('')
            entry.append('')
        # when there is only a title
        elif len(entry) == 1:
            entry.append('')
        return entry

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        self.entry_editor.delete('1.0', 'end')
        self.entry_editor.insert('1.0', text)

    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, posts:list):

        self.reset_ui()
        self._posts = posts
        for i in range(len(self._posts)):
            post_id = i
            self._insert_post_tree(post_id, self._posts[i])


    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, post: Post, profile: NaClProfile):
        import copy
        # we don't want to change the original post parameter
        postcopy = copy.deepcopy(post)
        postcopy.set_entry(profile.nacl_profile_decrypt(postcopy.get_entry()))
        self._posts.append(postcopy)
        self._insert_post_tree(len(self._posts) - 1, postcopy)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, post: Post):
        # entry = post.get_entry()
        title = post.get_title()
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(title) > 25:
            title = title[:24] + "..."
        
        self.posts_tree.insert('', id, id, text=title)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None, online_callback=None, add_post_callback=None) -> None:
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        self._add_post_callback = add_post_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using the get() function:

        self.is_online = tk.IntVar()
        # self.save_mode = None

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()

    def online_click(self) -> None:
        """
        Calls the callback function specified in the online_callback class attribute, if
        available, when the chk_button widget has been clicked.
        :return: None
        """
        if self._online_callback is not None:
            # chk_value = 1 when online mode is on, 0 when it is off
            chk_value = self.is_online.get()
            self._online_callback(chk_value)

    def add_post_click(self) -> None:
        """
        Calls the callback function specified in the add_post_callback class attribute, if
        available, when the add_post_button widget has been clicked.
        :return: None
        """
        if self._add_post_callback is not None:
            self._add_post_callback()

    def save_click(self) -> None:
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        :return: None
        """
        if self._save_callback is not None:

            self._save_callback()

    def set_status(self, message: str, color: str = None, change_back: bool = None) -> None:
        """
        Updates the text that is displayed in the footer_label widget, with
        change_back support.
        :param message: the message to display in footer_label
        :param color: the color for message
        :param change_back: if you want the footer_label to change back to
        'Ready.' after fixed amount of time
        :return: None
        """
        label = self.footer_label
        if color is None:
            label.configure(text=message)
        else:
            label.configure(text=message, fg=color)
        if change_back is not None:
            if change_back:
                label.after(2000, lambda: label.configure(text='Ready.', fg='black'))

    def _draw(self) -> None:
        """
        Call only once upon initialization to add widgets to the frame
        :return: None
        """
        save_button = tk.Button(master=self, text="Save Post", width=20, bg='light green')
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_post_button = tk.Button(master=self, text='Add Post', width=20, bg='cyan')
        add_post_button.configure(command=self.add_post_click)
        add_post_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        del_post_button = tk.Button(master=self, text='Delete Post', width=20, bg='red')
        del_post_button.configure(command=self.add_post_click)
        del_post_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class FileNameError(Exception):
    pass


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self._is_online = False
        self._profile_filename = None
        self._index = 0

    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')],
                                               defaultextension=[('Distributed Social Profile', '.dsu')])
        try:
            self._profile_filename = filename.name
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'name'":
                pass
                # raise FileNameError('Filename is empty') from e
        else:
            self._current_profile = NaClProfile()
            self._current_profile.generate_keypair()
            self._current_profile.username = 'ffyuanda'
            self._current_profile.password = 'ffyuanda123'
            self._current_profile.dsuserver = "168.235.86.101"
            self._current_profile.add_bio('')
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        try:
            self._profile_filename = filename.name
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'name'":
                pass
                # raise FileNameError('Filename is empty') from e
        else:
            self._current_profile = NaClProfile()
            self._current_profile.load_profile(self._profile_filename)
            self.body.set_posts(self._current_profile.get_posts())
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    def publish(self, np: NaClProfile):
        import ds_client
        send_type = 'pb'
        server = np.dsuserver
        port = 2021
        username = np.username
        password = np.password
        posts = np.get_posts()
        bio = np.get_bio()
        ds_client.send(np, send_type, server, port, username, password, posts,
                       bio)

    def add_post_process(self):
        """
        Adds the text currently in the entry_editor widget to the active DSU file.
        :return:
        """
        from a5 import posts_transclude
        if self._profile_filename is None:
            self.pop_up_msg('Create/Open a DSU file first!', color='red')
        else:
            post = Post()
            title = 'TYPE TITLE HERE'
            entry = 'TYPE ENTRY HERE'
            post.set_entry(entry)
            post.set_title(title)
            self._current_profile.add_post(post)
            self._current_profile = posts_transclude(self._current_profile)
            self._current_profile.save_profile(self._profile_filename)
            self.body.set_posts(self._current_profile.get_posts())
            self.body.set_text_entry("")
            self.footer.set_status('Post added!', 'green', change_back=True)

    def save_profile(self) -> None:
        """
        Saves the text currently in the entry_editor widget to the active DSU file.
        :return: None
        """
        from a5 import posts_transclude
        title = self.body.get_text_entry()[0]
        entry = self.body.get_text_entry()[1]
        try:
            self._index = self.body.curr_index()
        except Body.BodyError:
            msg = 'Nothing is selected to be saved!'
            self.pop_up_msg(msg, color='red')
        else:
            self._current_profile.edit_post(self._index, title, entry)
            self._current_profile = posts_transclude(self._current_profile)
            self._current_profile.save_profile(self._profile_filename)
            self.body.set_posts(self._current_profile.get_posts())
            self.footer.set_status('Saved!', 'green', change_back=True)
            if self._is_online:
                self.publish(self._current_profile)
                self.pop_up_msg('Uploaded!', color='green')

    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value: bool):

        self._is_online = value
        if self._is_online == 1:
            self.footer.set_status("Online", 'green')
        else:
            self.footer.set_status("Offline", 'red', change_back=True)

    def display_keys(self):

        def save_keys():
            public_key_text = public_key.get()
            private_key_text = private_key.get()
            if public_key_text != '' and private_key_text != '':
                if self._profile_filename is not None:
                    self._current_profile.public_key = public_key_text
                    self._current_profile.private_key = private_key_text
                    self._current_profile.keypair = public_key_text + private_key_text
                    self._current_profile.save_profile(self._profile_filename)

        window = tk.Toplevel()
        window.geometry('500x120')
        window.resizable(0, 0)

        public_key_label = tk.Label(window, text="Public key:")
        public_key_label.place(x=40, y=25)

        public_key = tk.Entry(window, width=52)
        public_key.insert(0, self._current_profile.public_key)
        public_key.place(x=110, y=25)

        private_key_label = tk.Label(window, text="Private key:")
        private_key_label.place(x=40, y=57)

        private_key = tk.Entry(window, width=52)
        private_key.insert(0, self._current_profile.private_key)
        private_key.place(x=110, y=57)

        save_button = tk.Button(window, text='save to the profile', command=save_keys)
        save_button.pack(side=tk.BOTTOM)

    def pop_up_msg(self, msg: str, size: str = None, color=None) -> None:
        """
        Pop up a message for user to read.
        :param msg: the message
        :param size: the size of the pop-up window
        :param color: the color of the message
        :return: None
        """
        import tkinter.font as tkFont
        font_style = tkFont.Font(size=20)

        window = tk.Toplevel()
        if size is None:
            window.geometry('500x60')
        else:
            window.geometry(size)
        window.resizable(0, 0)
        msg_label = tk.Label(window, text=msg, font=font_style, fg=color)
        msg_label.pack(fill=tk.BOTH)

    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        menu_file = tk.Menu(menu_bar)

        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_bar.add_cascade(menu=menu_file, label='File')

        # Settings widget
        menu_settings = tk.Menu(menu_bar)
        menu_settings.add_command(label='Current keys', command=self.display_keys)
        menu_bar.add_cascade(menu=menu_settings, label='Settings')

        self.root.config(menu=menu_bar)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed,
                             add_post_callback=self.add_post_process)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()