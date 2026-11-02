#from additional_functions import keycode_list, listbox_insert_list, darkmode, fix_characters, graph
#from raw_wpm_graph import graph
from tkinter import *
import time
import random
import threading

# HUOMIO: Ohjelma ei toimi ilman tiedostoja, joista löytyvät sanat ja virkkeet.

class program():
    def __init__(self):

        self.version = "1.4"
        
        #Preset variables:
        self.progression_value = 1
        self.last_keysym = None
        self.underline_number = -1
        self.space_iteration = 0
        self.amount_of_words_check = 0
        self.answer_list = []
        self.answer_str = ""
        self.definite_anslist = []
        self.event_keycode_list = additional_functions.keycode_list()
        self.light_or_dark = "light"
        self.color_switcher_foreground = "black"
        self.start_timer = False
        self.current_letter_index = 0
        self.progression_var = -1
        self.wpm_list = []
        self.fontsize = 25
        self.typing_language = "English1"
        self.space_indexes = []
        self.difficult_words = []
        self.customization_window_size_reset = False
        #Font:
        self.font_tuple = ("Courier", 23, "bold")
        self.font_list_typing = ["Courier", self.fontsize, "bold"]
        self.font_tuple_label = ("Courier", 30, "bold")
        #Root:
        self.root = Tk()
        self.root.title('Typing speed test')
        #self.root.iconbitmap('icon.ico')
        #self.root.resizable(False, False)
        self.root.rowconfigure([0,1], weight=1, minsize=100)
        self.root.columnconfigure(0, weight=1, minsize=100)
        self.root.geometry('1280x720')
        #Frames:
        self.settings = Frame(self.root)
        self.customize = Frame(self.root)
        self.customize2 = Frame(self.root)
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.own_text_input_frame = Frame(self.root)
        #Labels:
        self.hello_label = Label(text="Welcome to the typing test!", master=self.settings, font=self.font_tuple)
        self.answer_label_done = Label(master=self.root, font=self.font_list_typing)
        self.answer_label_undone = Label(master=self.root, font=self.font_list_typing)
        self.invalid_words_amount = Label(text="You must type a number!", master=self.root, font=self.font_tuple, fg="red")
        self.current_wpm_label = Label(master=self.root, font=self.font_tuple)
        self.wpm_label = Label(master=self.frame1, font=self.font_tuple_label)
        self.accuracy_label = Label(master=self.frame1, font=self.font_tuple_label)
        self.progression_label = Label(master=self.root, font=("Courier", 32, "bold"))
        self.own_text_input_label = Label(text="Write here words you want to type in the test.", master=self.own_text_input_frame, font=self.font_tuple)
        self.font_selection_label = Label(text="Font selection", master=self.customize, font=self.font_tuple)
        self.font_size_selection_label = Label(text="Font size", master=self.customize2, font=self.font_tuple)
        self.language_select_label = Label(text="Test language", master=self.customize, font=self.font_tuple)
        self.info_label = Label(text=f"Typing test program version {self.version}\n\n"
                                     "Point: Type the text on the screen as quickly and precisely as possible.\n"
                                     "Note: The graph is not accurate when typed text is short\n"
                                     "while the real WPM is still accurate.\n\n"
                                     "Keybinds:\n"
                                     "Tab -> Switch to next text.\nDel -> Return to title screen from typing.\n"
                                     "A/D -> Move in the WPM graph.\n", master=self.root, font=("Courier", 21, "bold"))
        #Entries:
        self.words_amount = Entry(master=self.settings, font=self.font_tuple, width=10, borderwidth=3, bg="lightgray")
        self.own_text_input_entry = Entry(font=self.font_tuple, master=self.own_text_input_frame, width=60, borderwidth=3, bg="lightgray")
        #Buttons:
        self.words = Button(text="Words", font=self.font_tuple, master=self.settings, padx=10, pady=5, command=self.question_type_words_amount, borderwidth=3, bg="lightgray")
        self.quotes = Button(text="Quotes", font=self.font_tuple, master=self.settings, padx=15, pady=5, command=self.question_type_quotes, borderwidth=3, bg="lightgray")
        self.next = Button(text="Next", font=self.font_tuple, master=self.frame2, padx=30, pady=5, command=self.next_question, borderwidth=3, bg="lightgray")
        self.restart = Button(text="Restart program", font=self.font_tuple, master=self.frame2, padx=14, pady=5, command=self.restart_program, borderwidth=3, bg="lightgray")
        self.redo = Button(text="Redo", font=self.font_tuple, master=self.frame2, padx=31, pady=5, command=self.redo_current, borderwidth=3, bg="lightgray")
        self.dark_mode = Button(text="Light/Dark Mode", font=self.font_tuple, master=self.settings, padx=10, pady=5, command=self.light_dark_switch, borderwidth=3, bg="lightgray")
        self.raw_wpm_graph_button = Button(text="Import raw WPM graph", font=self.font_tuple, master=self.root, padx=10, pady=5, command=self.import_raw_wpm_graph, borderwidth=3, bg="lightgray")
        self.info = Button(text="Info", font=self.font_tuple, master=self.settings, padx=10, pady=5, command=self.information, borderwidth=3, bg="lightgray")
        self.enter_customization = Button(text="Customize", font=self.font_tuple, master=self.settings, padx=10, pady=5, command=self.customization, borderwidth=3, bg="lightgray")
        self.exit_customization = Button(text="Exit", font=self.font_tuple, master=self.customize2, padx=10, pady=5, command=lambda: self.set_settings("fix"), borderwidth=3, bg="lightgray")
        self.enable_or_disable_progression_label = Button(text="Disable progression label", font=self.font_tuple, master=self.customize2, padx=10, pady=5, command=self.change_progression_value, borderwidth=3, bg="lightgray")
        self.own_text_input_button = Button(text="Enter own text", font=self.font_tuple, master=self.customize2, padx=10, pady=5, command=self.own_text_input, borderwidth=3, bg="lightgray")
        self.own_text_input_button_done = Button(text="Done", font=self.font_tuple, master=self.own_text_input_frame, padx=10, pady=5, command=lambda: self.own_text_input("exit"), borderwidth=3, bg="lightgray")
        #Text entries:
        #Other widgets:
        self.custom_list_font = Listbox(master=self.customize, font=self.font_tuple, highlightcolor="white", highlightthickness=3, selectbackground="lightblue", borderwidth=3, width=25)
        self.language_select = Listbox(master=self.customize, font=self.font_tuple, highlightcolor="white", highlightthickness=3, selectbackground="lightblue", borderwidth=3, width=25)

        self.screensize_scale = Scale(master=self.customize2, from_=23, to=80, font=self.font_tuple, length=200, width=25, orient=HORIZONTAL)
        #Config. font listbox:
        font_list = additional_functions.listbox_insert_list()
        for index, current_font in enumerate(font_list):
            self.custom_list_font.insert(index, current_font)
        #Config. language listbox:
        self.language_select.insert(0, "English1")
        self.language_select.insert(1, "English2")
        self.language_select.insert(2, "Suomi")
        self.language_select.insert(3, "Difficult words")

        self.set_settings()
        
    def own_text_input(self, event=None):
        if event is None:
            self.customize.pack_forget()
            self.customize2.pack_forget()
            self.root.focus_set()

            self.own_text_input_label.pack()
            self.own_text_input_entry.pack(pady=10)
            self.own_text_input_button_done.pack(pady=5)
            self.own_text_input_frame.grid(row=0, column=0)

        elif event == "exit":
            self.own_text_input_frame.grid_forget()
            self.root.focus_set()

            self.customize.pack()
            self.customize2.pack()

    def change_progression_value(self):
        if self.progression_value == 1:
            self.progression_value = 0
            self.enable_or_disable_progression_label.configure(text="Enable progression label")
        else:
            self.progression_value = 1
            self.enable_or_disable_progression_label.configure(text="Disable progression label")

    def information(self):
        self.settings.grid_forget()

        self.info_label.grid(row=0, column=0)
        self.root.bind("<Button-1>", self.set_settings)

    def customization(self):
        if self.root.winfo_height() < 760:
            self.previous_winfo_width = self.root.winfo_width()
            self.previous_winfo_height = self.root.winfo_height()

            self.winfo_height = 760
            self.root.geometry(f'{self.root.winfo_width()}x{self.winfo_height}')

            self.automatic_winfo_width = self.root.winfo_width()
            self.automatic_winfo_height = self.winfo_height

            self.customization_window_size_reset = True
        self.settings.grid_forget()
        self.root.focus_set()

        self.font_selection_label.grid(row=0, column=0)
        self.custom_list_font.grid(row=1, column=0)
        self.language_select_label.grid(row=0, column=1)
        self.language_select.grid(row=1, column=1)
        self.enable_or_disable_progression_label.pack(pady=3.5)
        self.font_size_selection_label.pack()
        self.screensize_scale.pack(pady=7)
        self.exit_customization.pack()
        self.own_text_input_button.pack(pady=5)

        self.customize.pack()
        self.customize2.pack()

        def perform():
            self.answer_label_done.configure(font=self.font_list_typing)
            self.answer_label_undone.configure(font=self.font_list_typing)

        def change_size(event):
            self.fontsize = int(self.screensize_scale.get())
            self.font_list_typing[1] = self.fontsize
            perform()

        def change_font(event):
            self.font_list_typing[0] = self.custom_list_font.get(self.custom_list_font.curselection())
            perform()

        def change_language(event):
            self.typing_language = self.language_select.get(self.language_select.curselection())

        self.screensize_scale.configure(command=change_size)
        self.custom_list_font.bind("<<ListboxSelect>>", change_font)
        self.language_select.bind("<<ListboxSelect>>", change_language)

    def wpm_thread(self):
        timestamp = 0
        while self.start_timer:
            time.sleep(0.5)
            timestamp += 0.5
            wpm = (len(self.answer_str) / 5) / timestamp * 60
            self.wpm_list.append(wpm)
        if not self.start_timer:
            timestamp = 0

    def resize_thread(self):
        self.answer_label_done.place(anchor=E, relx=self.root.winfo_width()*(-1/640000)+(1011/2000), rely=0.5)#.grid(row=0, column=0)

    def import_raw_wpm_graph(self):
        additional_functions.graph(self.wpm_list, self.light_or_dark)

    def set_settings(self, event=None):
        if self.customization_window_size_reset:
            if self.automatic_winfo_width == self.root.winfo_width()\
            and self.automatic_winfo_height == self.root.winfo_height():
                self.root.geometry(f"{self.previous_winfo_width}x{self.previous_winfo_height}")
            self.customization_window_size_reset = False
        try:
            self.customize.pack_forget()
            self.customize2.pack_forget()
            self.info_label.grid_forget()
            self.root.unbind("<Button-1>")
            self.root.focus_set()
        except:
            pass
        if event is not None:
            pass
        else:
        #Program starts:
            self.hello_label.grid(row=0, column=1, columnspan=4, pady=5)
            self.quotes.grid(row=1, column=0, padx=0)
            self.words.grid(row=1, column=1, padx=5)
            self.dark_mode.grid(row=1, column=3)
            self.info.grid(row=1, column=4, padx=5)
            self.enter_customization.grid(row=1, column=5)

        self.settings.grid(row=0, column=0, sticky='s')
        self.root.mainloop()

    def question_type_quotes(self):
        self.question_type = "quotes"
        self.root.focus_set()
        try:
            self.words_amount.grid_forget()
            self.quotes.grid_configure(padx=0)
            self.words.grid_configure(padx=5)
        finally:
            pass
        if self.typing_language == "English1" or self.typing_language == "English2" or self.typing_language == "Difficult words":
            self.word = random.choice(open('quotes_english').read().splitlines())
        elif self.typing_language == "Suomi":
            self.word = random.choice(open('quotes_finnish').read().splitlines())
            self.word = additional_functions.fix_characters(self.word)

        self.start()

    def question_type_words_amount(self):
        self.words_amount.grid(row=1, column=2, padx=5)
        if self.amount_of_words_check == 0:
            self.words_amount.configure(font=("Courier", 23, "bold", "italic"))
            self.words_amount.insert(0, "Num. words")
            self.amount_of_words_check = 1
        self.words_amount.bind("<Button-1>", self.words_amount_remove_text)
        self.words.grid_configure(padx=0)
        self.quotes.grid_configure(padx=5)
        self.words_amount.bind("<Return>", self.question_type_words)

    def question_type_words(self, event=None):
        self.question_type = "words"
        self.words_amount.grid_forget()
        self.quotes.grid_configure(padx=0)
        self.words.grid_configure(padx=5)
        integer_validity_check = self.words_amount.get()

        if not integer_validity_check.isnumeric():
            self.invalid_words_amount.grid(row=1, column=0, sticky='n', pady=5)
            self.question_type_words_amount()
        else:
            try:
                self.invalid_words_amount.grid_forget()
            finally:
                pass
        
            self.root.focus_set()
            if self.own_text_input_entry.get() == "":
                if self.typing_language == "English1":
                    file = "words_english"
                elif self.typing_language == "English2":
                    file = "top_1000_most_common_words"
                elif self.typing_language == "Suomi":
                    file = "words_finnish"
                elif self.typing_language == "Difficult words":
                    file = "difficult_words"
                self.word = random.choice(open(file).read().splitlines())
                for index in range(int(integer_validity_check)-1):
                    self.word += " " + random.choice(open(file).read().split())
                if self.typing_language == "Suomi": self.word = additional_functions.fix_characters(self.word)
            else:
                self.word = random.choice(self.own_text_input_entry.get().split())
                for index in range(int(integer_validity_check)-1):
                    self.word += " " + random.choice(self.own_text_input_entry.get().split())
            self.start()
            
    def typing_over(self):
        self.clear_question_screen()
        self.root.unbind("<Delete>")

        for i in self.space_indexes:
            self.definite_anslist.insert(i, " ")
        
        #Calc. WPM & acc.:
        self.accuracy_and_wpm()
        #Frame 1:
        self.frame1.grid(row=0, column=0, sticky='s', pady=10)
        #Widgets:
        self.wpm_label.grid(row=1, column=0)
        self.accuracy_label.grid(row=0, column=0)
        #Frame 2:
        self.frame2.grid(row=1, column=0, sticky='n')
        #Buttons:
        self.next.grid(row=0, column=0, padx=5)
        self.redo.grid(row=0, column=1, padx=5)
        self.restart.grid(row=1, column=0, columnspan=2, pady=10)
        self.raw_wpm_graph_button.place(anchor=CENTER, relx=0.5, rely=0.8075)
        #Tab press:
        self.root.bind("<Tab>", self.next_question)

    def lctrl_backspace(self, event):
        # difficult words:
        if self.answer_list[-1] == " ":
            del self.space_indexes[-1]
        
        answer_label_current_string = self.answer_str
        answer_label_current_string_list = answer_label_current_string.split()

        if [*answer_label_current_string][-1] == " ":
            self.space_iteration -= 1
            self.current_letter_index = len(''.join(self.word.split()[:self.space_iteration])) + self.space_iteration
        else:
            self.current_letter_index -= len(answer_label_current_string_list[-1])

        del answer_label_current_string_list[-1]

        if len(answer_label_current_string_list) > 0:
            new_string = ' '.join(answer_label_current_string_list) + " "
        else:
            new_string = ""
        self.answer_str = new_string
        self.answer_list = [*self.answer_str]

        self.answer_label_done.configure(text=new_string)
        self.answer_label_undone.configure(text=self.word[self.current_letter_index:])

        if self.answer_label_done['text'] == self.word[:len(self.answer_label_done['text'])]:
            green_or_red = "green"
        else:
            green_or_red = "red"
        self.answer_label_done.configure(fg=green_or_red)
        if self.underline_number > self.current_letter_index:
            self.answer_label_done.configure(underline=-1)

    def tab_press(self, event):
        self.clear_question_screen()

        self.reinitialize_difficult_words_variables()
        
        if self.question_type == "quotes":
            self.question_type_quotes()
        else:
            self.question_type_words()

    def accuracy_and_wpm(self):
        self.ending_time = time.time()
        time_used = self.ending_time - self.starting_time

        #print(' '.join(''.join(list) for list in self.definite_anslist))

        #difficult words:
        if self.typing_language != "Suomi" and self.question_type != "quotes" and self.own_text_input_entry.get() == "":
            for i,o in enumerate(self.word.split()):
                if ' '.join(''.join(list) for list in self.definite_anslist).split()[i] != o:
                    self.difficult_words.append(o)

            if self.difficult_words:
                with open("difficult_words", "a") as f:
                    f.write("\n" + '\n'.join([i for i in self.difficult_words]))
                #print(self.difficult_words)
            self.reinitialize_difficult_words_variables()
        
        #acc.:
        answer_list = self.answer_str.split()
        answer_str_words_amount = len(answer_list)

        word_list = self.word.split()

        wrong_letters = 0
        right_letters = 0
        additional_letters = 0

        for current_word_index in range(len(word_list)):
            if current_word_index+1 > answer_str_words_amount:
                wrong_letters += len(word_list[current_word_index])
                continue

            current_word = word_list[current_word_index]
            current_word_break = [*current_word]

            current_ans_word = answer_list[current_word_index]
            current_ans_word_break = [*current_ans_word]

            for current_letter_index, current_letter in enumerate(current_word_break):
                if current_letter_index+1 > len(current_ans_word_break):
                    wrong_letters += 1
                    continue

                if current_letter == current_ans_word_break[current_letter_index]:
                    right_letters += 1
                else:
                    wrong_letters += 1

            if len(current_ans_word_break) > len(current_word_break):
                additional_letters += len(current_ans_word_break) - len(current_word_break)
                wrong_letters += additional_letters
                #print(f"f{len(current_ans_word_break)}a{len(current_word_break)}")

        total_string_lenght = len(self.word) - len(word_list) + 1
        accuracy = (right_letters - additional_letters) / total_string_lenght
        #print(f"{right_letters} - {additional_letters} / {total_string_lenght}")

        #wpm:
        words_per_minute = ((len(self.answer_str) / 5) / (time_used / 60)) * accuracy

        self.wpm_label.configure(text="WPM: {:.1f}".format(words_per_minute))
        self.accuracy_label.configure(text="Accuracy: {:.1f}%".format(accuracy*100))
        #print(right_letters)
        #print(wrong_letters)

    def reinitialize_difficult_words_variables(self):

        self.definite_anslist = []
        self.space_indexes = []
        self.difficult_words = []
        
    def clear_question_screen(self):
        self.start_timer = False

        self.progression_label.place_forget()
        self.answer_label_done.place_forget()
        self.answer_label_undone.place_forget()
        self.root.unbind("<KeyPress>")
        self.root.unbind("<Control-BackSpace>")
        self.root.unbind("<Tab>")

        self.progression_var = -1
        self.underline_number = -1
        self.current_letter_index = 0
        self.answer_list = []
        self.answer_label_done.configure(underline=-1)

    def clear_screen(self):
        self.frame1.grid_forget()
        self.frame2.grid_forget()

        self.next.grid_forget()
        self.redo.grid_forget()
        self.restart.grid_forget()
        self.wpm_label.grid_forget()
        self.accuracy_label.grid_forget()
        self.raw_wpm_graph_button.place_forget()

    def next_question(self, event=None):
        self.clear_screen()
        self.root.unbind("<Tab>")

        if self.question_type == "words":
            self.question_type_words()
        if self.question_type == "quotes":
            self.question_type_quotes()

    def restart_program(self, event=None):
        self.root.unbind("<Tab>")
        if event is not None:
            self.clear_question_screen()
            
            self.reinitialize_difficult_words_variables()
            
            self.root.unbind("<Delete>")
        else:
            self.clear_screen()
        self.set_settings("restart")

    def redo_current(self):
        self.clear_screen()

        self.start()

    def press_space(self, mode=None):
        current_word_index = len(self.answer_str.split())
        # Space:
        if mode is None:
            self.space_iteration += 1
            self.current_letter_index = len(''.join(self.word.split()[:current_word_index])) + self.space_iteration
            self.answer_list.append(" ")
            if len(''.join(self.answer_list).split()[-1]) < len(self.word.split()[self.space_iteration-1]):
                self.underline_number = len(self.answer_list)-2
                self.answer_label_done.configure(underline=self.underline_number)
        # Backspace:
        elif mode == "BS":
            self.space_iteration -= 1
            self.current_letter_index = len(''.join(self.word.split()[:current_word_index-1])) + self.space_iteration + len(''.join(self.answer_list).split()[-1])

            del self.answer_list[-1]

    def words_amount_remove_text(self, event):
        self.words_amount.delete(0, END)
        self.words_amount.configure(font=self.font_tuple, fg=self.color_switcher_foreground)

    def light_dark_switch(self):
        if self.light_or_dark == "light":
            self.light_or_dark = "dark"
            
            color_switcher_background = "#121212"
            self.color_switcher_foreground = "white"
            color_switcher_button = "gray"
        else:
            self.light_or_dark = "light"
            color_switcher_background = "#F0F0F0"
            self.color_switcher_foreground = "black"
            color_switcher_button = "lightgray"

        widget_dict = additional_functions.darkmode(self)

        for _ in widget_dict["frames"]:
            _.configure(bg=color_switcher_background)
        for _ in widget_dict["buttons"]:
            _.configure(fg=self.color_switcher_foreground, bg=color_switcher_button)
        for _ in widget_dict["labels"]:
            _.configure(fg=self.color_switcher_foreground, bg=color_switcher_background)
        for _ in widget_dict["other_labels"]:
            _.configure(bg=color_switcher_background)
        for _ in widget_dict["others"]:
            _.configure(fg=self.color_switcher_foreground, bg=color_switcher_button)

    def start(self):
        self.space_iteration = 0
        self.underline_number = -1
        self.settings.grid_forget()

        self.progression_label.configure(text=f"0/{len(self.word.split())}")
        self.answer_label_done.configure(text="", bg="yellow")
        self.answer_label_undone.configure(text=self.word, bg="yellow")
        if self.progression_value == 1:
            self.progression_label.place(anchor=CENTER, relx=0.5, rely=0.2)

        self.answer_label_undone.place(anchor=W, relx=0.5, rely=0.5)#grid(row=0, column=1)

        self.root.bind("<KeyPress>", self.timer)
        self.root.bind("<Control-BackSpace>", self.lctrl_backspace)
        self.root.bind("<Tab>", self.tab_press)
        self.root.bind("<Delete>", self.restart_program)

    def timer(self, event):
        if event.keycode not in self.event_keycode_list and not self.start_timer:
            self.start_timer = True

            self.wpm_list = []
            self.definite_anslist = [[] for i in range(len(self.word.split()))]
            #print(self.definite_anslist)

            thread1 = threading.Thread(target=self.wpm_thread)
            thread1.start()

            thread2 = threading.Thread(target=self.resize_thread)
            thread2.start()

            self.starting_time = time.time()

        if event.keysym == "BackSpace":
            self.last_keysym = event.keysym
            if self.answer_list[-1] == " ":
                del self.space_indexes[-1]
                self.press_space("BS")
            elif self.current_letter_index > -1:
                del self.answer_list[-1]
                self.current_letter_index -= 1
            if self.current_letter_index-1 == self.underline_number:
                self.answer_label_done.configure(underline=-1)
        else:
            if event.keycode not in self.event_keycode_list and event.keysym != "space":
                self.answer_list.append(event.char)

                self.definite_anslist[self.space_iteration].append(event.char)
                #print(self.definite_anslist)

                self.current_letter_index += 1
                self.last_keysym = event.keysym
            elif event.keysym == "space" and self.start_timer and self.last_keysym != "space":
                self.last_keysym = "space"
                self.space_indexes.append(len(self.definite_anslist) + len(self.space_indexes))
                self.press_space()
            else:
                pass

        self.answer_str = ''.join(self.answer_list)

        if len(self.answer_str.split()) > self.progression_var:
            self.progression_var += 1
            self.progression_label.configure(text=f"{self.progression_var}/{len(self.word.split())}")

        self.answer_label_done.configure(text=self.answer_str)
        self.answer_label_undone.configure(text=self.word[self.current_letter_index:])

        if self.answer_label_done['text'] == self.word[:len(self.answer_label_done['text'])]:
            redorgreen = "green"
        else:
            redorgreen = "red"
        self.answer_label_done.configure(fg=redorgreen)

        if len(self.answer_str.split()) == len(self.word.split()) and len(self.answer_str.split()[-1]) == len(self.word.split()[-1])\
           or len(self.answer_str.split())-1 == len(self.word.split()):
            self.typing_over()
        self.answer_label_undone.configure(underline=0)

class additional_functions():
    def keycode_list():
        return [9, 13, 16,
                17, 18, 19,
                20, 27, 32,
                33, 34, 35,
                36, 37, 38,
                39, 40, 45,
                46, 91, 93,
                96, 97, 98,
                99, 100, 101,
                102, 103, 104,
                105, 106, 107,
                109, 110, 112,
                113, 114, 115,
                116, 117, 118,
                119, 120, 121,
                122, 123, 144,
                145, 186, 219,
                220]

    def listbox_insert_list():
        return ["Courier New", "Times New Roman", "Comic Sans MS", "Calibri", "Arial", "Bahnschrift", "Consolas",
                "Candara", "Microsoft Tai Le", "Segoe Print", "Verdana", "Helvetica", "Fixedsys", "Gabriola", "Impact",
                "Ink Fre", "Marlett", "Modern", "Small Fonts", "Symbol", "Webdings", "Terminal"]

    def darkmode(self=None):
        dictionary = {"frames" : [self.root, self.settings, self.customize, self.customize2, self.frame1, self.frame2, self.own_text_input_frame],
                      "buttons" : [self.next, self.words, self.quotes, self.redo, self.restart, self.dark_mode, self.raw_wpm_graph_button, self.info, self.enter_customization, self.exit_customization, self.enable_or_disable_progression_label, self.own_text_input_button_done, self.own_text_input_button],
                      "labels" : [self.hello_label, self.wpm_label, self.accuracy_label, self.progression_label, self.info_label, self.font_selection_label, self.font_size_selection_label, self.language_select_label, self.own_text_input_label],
                      "other_labels" : [self.answer_label_done, self.answer_label_undone, self.invalid_words_amount],
                      "others" : [self.words_amount, self.custom_list_font, self.screensize_scale, self.language_select, self.own_text_input_entry],
                      "graph" : []}
        return dictionary

    def fix_characters(to_be_fixed):
        fix = ["Ã¶","Ã¤","Ã¥","Ã–","Ã„","Ã…"]
        fixed = ["ö","ä","å","Ö","Ä","Å"]
        fixed_text = to_be_fixed.replace(fix[0], fixed[0]).replace(fix[1], fixed[1]).replace(fix[2], fixed[2])\
                    .replace(fix[3], fixed[3]).replace(fix[4], fixed[4]).replace(fix[5], fixed[5])
        return fixed_text

    def graph(wpm_list=None, light_or_dark=None):
        import turtle
        global lower_moving_varx, upper_moving_varx
        #Var:
        distance_multiplier = -427

        lower_moving_varx = -427
        upper_moving_varx = 427
        #Screen:
        turtle.TurtleScreen._RUNNING = True
        screen = turtle.Screen()
        screen.title("Raw WPM graph : (seconds, wpm)")
        screen.setup(width=854, height=498)
        if light_or_dark == "dark":
            screen.bgcolor("black")
        screen.cv._rootwindow.resizable(False, False)
        turtle.setworldcoordinates(llx=-427, lly=-249, urx=427, ury=249)
        screen.tracer(0)
        #Settings up graph - x axle:
        for index in range(20):
            screen_setup_x = turtle.Turtle()
            if light_or_dark == "dark":
                screen_setup_x.color("white")
            if index%4 != 0:
                screen_setup_x.color("gray")
            screen_setup_x.penup()
            screen_setup_x.goto(-427, index*25-240)
            screen_setup_x.pendown()
            screen_setup_x.setx(25000-427)
            screen_setup_x.hideturtle()
        #Setting up graph - y axle:
        screen_setup_y = turtle.Turtle()
        screen_setup_y.penup()
        screen_setup_y.goto(-427, -240)
        if light_or_dark == "dark":
            screen_setup_y.color("white")
        screen_setup_y.pendown()
        screen_setup_y.sety(500-240)
        screen_setup_y.hideturtle()

        #Showing numbers - x axle (TIME):
        for index in range(1, 500):
            number = turtle.Turtle()
            number.penup()
            number.hideturtle()
            number.goto(index*50-427, -240)
            if light_or_dark == "dark":
                number.color("white")
            number.write(f"{index}")
        #Showing numbers - y axle (WPM):
        for index in range(10):
            number = turtle.Turtle()
            number.penup()
            number.hideturtle()
            number.goto(-423, index*50-240)
            if light_or_dark == "dark":
                number.color("white")
            number.write(f"{index*50}")
        #Drawing graph:
        pointer = turtle.Turtle()
        pointer.color("red")
        pointer.penup()
        pointer.goto(distance_multiplier, wpm_list[0]-240)
        pointer.pendown()
        for iteration in wpm_list:
            distance_multiplier += 25
            pointer.goto(distance_multiplier, iteration-240)
        screen.update()

        #Making screen movable!
        def moving_screen_right():
            global lower_moving_varx, upper_moving_varx
            turtle.setworldcoordinates(llx=lower_moving_varx+854, lly=-249, urx=upper_moving_varx+854, ury=249)
            lower_moving_varx += 854
            upper_moving_varx += 854

        def moving_screen_left():
            global lower_moving_varx, upper_moving_varx
            if lower_moving_varx > -427:
                turtle.setworldcoordinates(llx=lower_moving_varx-854, lly=-249, urx=upper_moving_varx-854, ury=249)
                lower_moving_varx -= 854
                upper_moving_varx -= 854

        screen.onkeypress(moving_screen_right, "d",)
        screen.onkeypress(moving_screen_left, "a")
        screen.listen()


program()
