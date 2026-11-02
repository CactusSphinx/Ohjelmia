from tkinter import *
import turtle
from math import *

class ui():
    def __init__(self):

        self._version = "1.0"

        # ROOT:
        self.root = Tk()
        self.root.title(f"Kuvaajan piirtäjä versio {self._version}")
        self.root.iconbitmap("nimetön.ico")
        self.root.geometry("1920x1080")
        self.root.rowconfigure([0,1], weight=1, minsize=100)
        self.root.columnconfigure(0, weight=1, minsize=100)

        # FRAMES:
        self.mainframe = Frame(self.root)

        # NECESSARY VARIABLES:
        self.nv_validity_check = 0

        # PRESET VARIABLES:
        self.font_list = ["Courier New", 30]
        self.light_or_dark = "light"
        self.mode = 1

        # LABELS:
        self.version_label = Label(text=f"Kuvaajan piirtäjä VERSIO {self._version}", font=self.font_list, master=self.root)
        self.version_label.place(x=0, y=0)
        self.information_label = Label(text="Kirjoita funktio:", font=self.font_list, master=self.mainframe, cursor="@larrow.cur")
        self.invalid_function_input_label = Label(text="Aloita 'y='", font=self.font_list, fg="red", master=self.mainframe)
        self.function_color_input_label = Label(text="Syötä funktion kuvaajan väri:", font=self.font_list, master=self.mainframe)

        # INPUTS:
        self.function_input = Entry(font=self.font_list, master=self.mainframe, borderwidth=5)
        self.function_color_input = Entry(font=self.font_list, master=self.mainframe, borderwidth=5)

        # BUTTONS:
        self.darkmode_button = Button(text="Aktivoi valoisa tila", font=self.font_list, master=self.mainframe, borderwidth=5, command=self.ui_appearance)
        self.enter_button = Button(text="PIIRRÄ", font=self.font_list, master=self.mainframe, borderwidth=5, command=self.function_validity_check)
        self.mode_button = Button(text="Tarkka, hitain", font=self.font_list, master=self.mainframe, borderwidth=5, command=self.change_mode)

        self.ui_appearance()

        self.start()

    def start(self):
        self.mainframe.grid(row=0, column=0, sticky="S")
        self.darkmode_button.grid(row=0, column=0)
        self.information_label.grid(row=1, column=0, pady=10)
        self.function_input.grid(row=2, column=0)
        self.function_color_input_label.grid(row=4, column=0, pady=10)
        self.function_color_input.grid(row=5, column=0)
        self.mode_button.grid(row=6, column=0, pady=50)
        self.enter_button.grid(row=7, column=0)

        self.function_input.bind("<Return>", self.function_validity_check)

        self.root.mainloop()

    def function_validity_check(self, event=None):
        if self.nv_validity_check == 1:
            self.invalid_function_input_label.grid_forget()
            self.nv_validity_check = 0

        self.function = self.function_input.get()

        if self.function.startswith("y="):
            self.draw_graph()
        else:
            self.invalid_function_input_label.grid(row=3, column=0)
            self.nv_validity_check = 1

    def draw_graph(self):
        value_dict = {}
        x = -100
        range_list = []

        if self.mode == 1:
            x_addition_value = 0.1
            self.range = 2001
        if self.mode == 2:
            x_addition_value = 0.01
            self.range = 19999

        while x <= 100:
            x += x_addition_value
            range_list.append(x)

        for value_x in range_list:
            if value_x == 0:
                continue

            self.function_replaced = self.function.replace("x", str(value_x))[2:]

            self.function_replaced_simplified = eval(self.function_replaced)

            value_dict.update({value_x : self.function_replaced_simplified})

        graph(value_dict, self.function_color_input.get(), self.range)

    def ui_appearance(self):
        if self.light_or_dark == "light":
            color_switcher_background = "#121212"
            color_switcher_foreground = "white"
            color_switcher_button = "gray"
            self.light_or_dark = "dark"
            self.darkmode_button["text"] = "Aktivoi valoisa tila"
        else:
            color_switcher_background = "#F0F0F0"
            color_switcher_foreground = "black"
            color_switcher_button = "lightgray"
            self.light_or_dark = "light"
            self.darkmode_button["text"] = "Aktivoi pimeä tila"

        widget_dict =  additional_functions.darkmode(self)

        for _ in widget_dict["frames"]:
            _.configure(bg=color_switcher_background)
        for _ in widget_dict["buttons and inputs"]:
            _.configure(fg=color_switcher_foreground, bg=color_switcher_button)
        for _ in widget_dict["labels"]:
            _.configure(fg=color_switcher_foreground, bg=color_switcher_background)
        for _ in widget_dict["other_labels"]:
            _.configure(bg=color_switcher_background)
        for _ in widget_dict["others"]:
            _.configure(fg=color_switcher_foreground, bg=color_switcher_button)

    def change_mode(self):
        if self.mode == 1:
            self.mode = 2
            self.mode_button.configure(text="Epätarkka, nopein")
        elif self.mode == 2:
            self.mode = 1
            self.mode_button.configure(text="Tarkka, hitain")

class graph():
    def __init__(self, value_dict, graph_color, _range):

        cv = turtle.Screen()
        turtle.TurtleScreen._RUNNING = True
        cv.setup(width=1280, height=720)
        cv.tracer(0)

        # SETTING UP X AXLE:
        x_axle_main = turtle.Turtle()
        x_axle_main.penup()
        x_axle_main.width(2)
        x_axle_main.goto(x=0, y=-1000)
        x_axle_main.pendown()
        x_axle_main.goto(x=0, y=1000)

        # SETTING UP X AXLE VALUES:
        for x_axle_num in range(-100, 100, 10):
            if x_axle_num == 0:
                continue
            x_val = turtle.Turtle()
            x_val.penup()
            x_val.hideturtle()
            x_val.goto(x=x_axle_num*10, y=0)
            x_val.write(x_axle_num)

        # OTHER X-AXLES:
        for other_x_a in range(-100, 100, 5):
            if other_x_a == 0:
                continue
            other_x_axle = turtle.Turtle()
            other_x_axle.penup()
            other_x_axle.hideturtle()
            other_x_axle.color("gray")
            other_x_axle.goto(x=other_x_a*10, y=-1000)
            other_x_axle.pendown()
            other_x_axle.goto(x=other_x_a*10, y=1000)

        # SETTING UP Y AXLE:
        y_axle_main = turtle.Turtle()
        y_axle_main.penup()
        y_axle_main.hideturtle()
        y_axle_main.width(2)
        y_axle_main.goto(x=-1000, y=0)
        y_axle_main.pendown()
        y_axle_main.goto(x=1000, y=0)

        # OTHER Y-AXLES:
        for other_y_a in range(-100, 100, 5):
            if other_y_a == 0:
                continue
            other_y_axle = turtle.Turtle()
            other_y_axle.penup()
            other_y_axle.hideturtle()
            other_y_axle.color("gray")
            other_y_axle.goto(x=-1000, y=other_y_a*10)
            other_y_axle.pendown()
            other_y_axle.goto(x=1000, y=other_y_a*10)

        # SETTING UP Y AXLE VALUES:
        for y_axle_num in range(-100, 100, 10):
            y_val = turtle.Turtle()
            y_val.penup()
            y_val.hideturtle()
            y_val.goto(x=3, y=y_axle_num*10)
            y_val.write(y_axle_num)

        cv.update()

        # DRAWING GRAPH:
        graph_pen = turtle.Turtle()
        graph_pen.penup()
        graph_pen.hideturtle()

        if graph_color != "":
            color_list = {"punainen" : "red", "vihreä" : "green", "sininen" : "blue", "oranssi" : "orange", "keltainen" : "yellow"}
            if graph_color in color_list.keys():
                graph_color = color_list["{}".format(graph_color)]
            graph_pen.color(graph_color)
        else:
            graph_pen.color("red")

        graph_pen.goto(x=list(value_dict.items())[0][0]*10, y=list(value_dict.items())[0][1]*10)
        graph_pen.pendown()

        for _index in range(_range):
            graph_pen.goto(x=list(value_dict.items())[_index][0]*10, y=list(value_dict.items())[_index][1]*10)

        cv.update()


class additional_functions():
    def darkmode(self=None):
        widget_dict = {"frames": [self.root, self.mainframe],
                      "buttons and inputs": [self.darkmode_button, self.function_input, self.function_color_input, self.enter_button, self.mode_button],
                      "labels": [self.version_label, self.information_label, self.function_color_input_label],
                      "other_labels": [self.invalid_function_input_label],
                      "others": [],
                      "graph": []}
        return widget_dict

ui()
