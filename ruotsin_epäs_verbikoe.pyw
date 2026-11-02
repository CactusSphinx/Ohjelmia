from tkinter import *
import random

class GUI:
    def __init__(self):
        #Window & Settings:
        self.root = Tk()
        self.root.title("Ruotsin epäsäännölisten verbien koe")
        self.root.geometry('1280x720')

        self.root.rowconfigure([0, 1], weight = 1, minsize = 200)
        self.root.columnconfigure(0, weight = 1, minsize = 200)
        #Font:
        self.font_tuple = ("Comic Sans MS", 17, "bold")
        #Frames:
        self.credits = Frame(self.root)
        self.settings = Frame(self.root)
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        #Configuring settings frame:
        self.credits.place(x = 0, y = 0)
        self.settings.grid(row = 0, column = 0, sticky = "S")#place(anchor = CENTER, relx = .5, rely = .4)
        #Labels:
        self.credit_label = Label(master = self.credits, text = "Versio 1.0, 28-1-2023", font = self.font_tuple)
        self.verb_label = Label(master = self.frame1, font = self.font_tuple)
        self.hello_label = Label(master = self.settings, text = "Välkommen, kuinka monta verbiä haluat?", font = self.font_tuple)
        self.instruction_label = Label(master = self.frame1, text = "Taivuta verbiä:", font = self.font_tuple)
        self.right_label = Label(master = self.frame2, fg = "green", font = self.font_tuple)
        self.wrong_label = Label(master = self.frame2, fg = "red", font = self.font_tuple)
        self.not_numeric = Label(master = self.root, text="Määrän täytyy olla luku", font = self.font_tuple, fg = "red")

        self.credit_label.pack()       
        self.hello_label.pack()
        #Entries:
        self.answer_entry = Entry(master = self.frame1, width = 20, borderwidth = 3, font = self.font_tuple, bg = "gray")
        self.verb_amount = Entry(master = self.settings, width = 30, borderwidth = 3, font = self.font_tuple, bg = "gray")

        self.verb_amount.pack()
        #Buttons:
        self.next = Button(master = self.frame2, text = "Seuraava", font = self.font_tuple, borderwidth = 3, bg = "gray", padx = 5, pady = 3, command = self.next_question)
        #Binds:
        self.verb_amount.bind("<Return>", self.num_check)
        #Counter:
        self.amount_counter = 0
        #Make the program appear on its own:
        self.root.mainloop()
    def num_check(self, event):
        #Retrieving set amount of verbs:
        self.set_amount_verbs = self.verb_amount.get()
        try:
            self.not_numeric.grid_forget()
        except:
            pass
        #Checking if user set amount is a number:
        if not self.set_amount_verbs.isnumeric():
            self.not_numeric.grid(row = 1, column = 0, sticky = 'n')
        else:
            #Unbinding "<Return>" (change made 24.2.2024):
            self.verb_amount.unbind("<Return>")
            self.start("<Return>")
    def start(self, event):
        #Forgetting settings frame & setting up frame1:
        self.settings.grid_forget()
        self.frame1.grid(row = 0, column = 0, sticky = "S")#place(anchor = CENTER, relx = .5, rely = .4)
        self.current_verb = random.choice(open('SvenskaVerbs.txt', 'r').read().splitlines())
        #Fixing broken characters with f/fix_characters:
        self.current_verb = self.fix_characters(self.current_verb)
        #Making var current_verb a list:
        self.current_verb_list = self.current_verb.split()
        #Configuring & packing:
        self.verb_label.configure(text = f"{self.current_verb_list[0]}".upper(), bg = "yellow")
        self.instruction_label.grid(row = 0, column = 0, pady = 5)
        self.verb_label.grid(row = 0, column = 1, pady = 5, sticky = "W")
        self.answer_entry.grid(row = 1, columnspan = 2)
        #Bindings:
        self.answer_entry.bind("<Return>", self.enter)
    def enter(self, event):
        #Unbinding "<Return>" (change made 1.9.2023):
        self.answer_entry.unbind("<Return>")
        #Retrieving user input:
        self.user_answer = self.answer_entry.get().lower()
        #Listing:
        self.user_answer_list = self.user_answer.split()
        print(self.user_answer_list)
        #Settin up frame2:
        self.frame2.grid(row = 1, column = 0, sticky = "N")#place(anchor = CENTER, relx = .5, rely = .54)
        #Configuring right answer form:
        self.right_answer = f"{self.current_verb_list[1]}, {self.current_verb_list[2]}, {self.current_verb_list[3]}"
        #If answered right:
        self.answer_index = 0
        #Search for right answers in the user answer:
        self.right_answer_present = [f"{self.current_verb_list[1]}",
                                     f",{self.current_verb_list[1]}",
                                     f"{self.current_verb_list[1]},",
                                     f",{self.current_verb_list[1]},"]
        self.right_answer_imperfect = [f"{self.current_verb_list[2]}",
                                       f",{self.current_verb_list[2]}",
                                       f"{self.current_verb_list[2]},",
                                       f",{self.current_verb_list[2]},"]
        self.right_answer_supinum = [f"{self.current_verb_list[3]}",
                                     f",{self.current_verb_list[3]}",
                                     f"{self.current_verb_list[3]},",
                                     f",{self.current_verb_list[3]},"]
        #Checking for right answers in correct order:
        for ANS in self.user_answer_list:
            if self.answer_index == 0:
                if ANS not in self.right_answer_present:
                    self.right_present = -1
                else:
                    self.right_present = 1
            if self.answer_index == 1:
                if ANS not in self.right_answer_imperfect:
                    self.right_imperfect = -1
                else:
                    self.right_imperfect = 1
            if self.answer_index == 2:
                if ANS not in self.right_answer_supinum:
                    self.right_supinum = -1
                else:
                    self.right_supinum = 1
            self.answer_index += 1
        print(f"{self.right_present}, {self.right_imperfect}, {self.right_supinum}")
        if self.right_present != -1 and self.right_imperfect != -1 and self.right_supinum != -1:
            self.right_answer_read = random.choice(open('SvenskaAnswerRight.txt', 'r').read().splitlines())
            self.right_answer_read = self.fix_characters(self.right_answer_read)
            self.right_label.configure(text = self.right_answer_read)
            self.right_label.grid(row = 0, column = 0)
        #If answered wrong:
        else:               
            self.wrong_answer_read = text = random.choice(open('SvenskaAnswerWrong.txt', 'r').read().splitlines())
            self.wrong_answer_read = self.fix_characters(self.wrong_answer_read)
            self.wrong_number = 0
            self.wrong_tense = ""
            if self.right_present == -1:
                self.wrong_tense = f"preesensin {self.current_verb_list[1]}"
                self.right_index = 1
                self.wrong_number += 1
            if self.right_imperfect == -1:
                if self.wrong_number == 1:
                    if self.right_supinum != -1:
                        self.wrong_tense += f" ja imperektin {self.current_verb_list[2]}"
                    else:
                        self.wrong_tense += f", imperektin {self.current_verb_list[2]}"
                else:
                    self.wrong_tense = f"imperfektin {self.current_verb_list[2]}"
                self.right_index = 2
                self.wrong_number += 1
            if self.right_supinum == -1:
                if self.wrong_number in [1,2]:
                    self.wrong_tense += f" ja supiinin {self.current_verb_list[3]}"
                else:
                    self.wrong_tense = f"supiinin {self.current_verb_list[3]}"
                self.right_index = 3
                self.wrong_number += 1
            self.wrong_label.configure(text = f"{self.wrong_answer_read}\nOikea vastaus on {self.wrong_tense}!")
            self.wrong_label.grid(row = 0, column = 0)
        self.next.grid(row = 1, column = 0, pady = 5)
    def next_question(self):
        #Adding 1 to the counter:
        self.amount_counter += 1
        #Forgetting & Resetting:
        self.answer_entry.delete(0, END)
        self.verb_label.grid_forget()
        try:   
            self.right_label.grid_forget()       
            self.wrong_label.grid_forget()
        except:
            pass
        self.next.grid_forget()
        #Going back up to start if counter hasn't reached the set amount by the user:
        if self.amount_counter != int(self.set_amount_verbs):
            self.start("<Return>")
        #However, if the amount has been reached, the program will terminate:
        else:
            self.instruction_label.grid_forget()
            self.answer_entry.grid_forget()
            Label(text = "Bra jobbat! Olet päässyt loppuun.", font = self.font_tuple).place(anchor = CENTER, relx = .5, rely = .4)
            self.root.bind("<Button-1>", self.exit_program)
    def fix_characters(self, to_be_fixed):
        #Fixing broken characters:
        self.fix = ["Ã¶","Ã¤","Ã¥"]
        self.fixed = ["ö","ä","å"]
        fixed_text = to_be_fixed.replace(self.fix[0], self.fixed[0]).replace(self.fix[1], self.fixed[1]).replace(self.fix[2], self.fixed[2])
        return fixed_text
    def exit_program(self, event):
        quit()
GUI()
