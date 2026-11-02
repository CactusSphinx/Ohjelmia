from tkinter import *
import random
import turtle
import time
import sys


class StartupWindow():
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1280x720")
        self.root.rowconfigure([0,1], weight=1, minsize=100)
        self.root.columnconfigure(0, weight=1, minsize=100)

        self.mainframe = Frame(self.root)

        self.font_list = ["Terminal", 24, "bold"]

        self.initiate_label = Label(text="TETRIS", font=self.font_list, master=self.mainframe)

        self.start_button = Button(text="Aloita peli", font=self.font_list, padx=10, pady=5, command=self.Start, bg="lightgray", master=self.mainframe)
        self.settings_button = Button(text="Asetukset", font=self.font_list, padx=10, pady=5, bg="lightgray", master=self.mainframe)

        self.Place()

        self.root.mainloop()

    def Place(self):
        self.initiate_label.grid(row=0, column=0)
        self.settings_button.grid(row=1, column=0, pady=5)
        self.start_button.grid(row=2, column=0)

        self.mainframe.grid(row=0, column=0, sticky="s")

    def Start(self):
        GameWindow()

class GameWindow():
    def __init__(self):

        self.num_rows = 20
        self.num_columns = 11
        self.block_size = 40
        self.default_speed = 0.18
        self.speed = self.default_speed

        self.score = 0
        self.counter = 0
        self.turn_iteration = 1
        self.game_started = False
        self.end_game = False
        self.speed_up = False
        self.clear = False
        self.StopPieces = True
        self.current_piece_blockID_pos = []
        self.blockID_occupation = []
        self.fillers = []
        self.color_dict = {}
        self.all_rows_dict = {}
        self.stats = []

        for list_number in range(0, self.num_rows):
            self.all_rows_dict[list_number+1] = [f"{list_number+1}S{x}" for x in range(self.num_columns)]

        self.block_colors = ("red",
                             "blue",
                             "yellow",
                             "purple",
                             "green",
                             "orange",
                             "pink",
                             "lightblue",
                             "lightgreen",
                             "black",
                             "white")

        self.canvas = turtle.Screen()
        self.canvas.title("TETRIS")
        self.canvas.setup(width=1.2*(self.block_size*self.num_columns-4.6), height=1.2*(self.block_size*self.num_rows+33.48))
        #self.canvas.setup(width=self.block_size*self.num_columns, height=self.block_size*(self.num_rows+1))
        turtle.TurtleScreen._RUNNING = True
        #self.canvas.cv._rootwindow.resizable(False, False)
        self.canvas.setworldcoordinates(llx=0, lly=0, urx=self.block_size*self.num_columns, ury=self.block_size*(self.num_rows+1))
        self.canvas.tracer(0)

        self.canvas.onkeypress(self.Left, "a")
        self.canvas.onkeypress(self.Left, "Left")

        self.canvas.onkeypress(self.Right, "d")
        self.canvas.onkeypress(self.Right, "Right")

        self.canvas.onkeypress(self.Down, "s")
        self.canvas.onkeypress(self.Down, "Down")

        self.canvas.onkeypress(self.TurnPiece, "w")
        self.canvas.onkeypress(self.TurnPiece, "Up")

        self.canvas.bgcolor("#313BC5")
        self.scoreboard_text = turtle.Turtle()
        self.scoreboard_text.penup()
        self.scoreboard_text.hideturtle()
        self.scoreboard_text.goto(10, self.block_size*self.num_rows+10)
        self.scoreboard_text.write("Pisteet: {}".format(self.score), font=("Terminal", int(0.6*self.block_size)))

        self.end_text = turtle.Turtle()
        self.end_text.color("#D60000")
        self.end_text.penup()
        self.end_text.hideturtle()


        for XLineIndex in range(self.num_rows+1):
            x_line_drawer = turtle.Turtle()
            x_line_drawer.color("black")
            x_line_drawer.hideturtle()
            x_line_drawer.penup()
            x_line_drawer.goto(0, XLineIndex*self.block_size)
            x_line_drawer.pendown()
            x_line_drawer.goto(self.block_size*self.num_columns, XLineIndex*self.block_size)

        for YLineIndex in range(self.num_columns+1):
            y_line_drawer = turtle.Turtle()
            y_line_drawer.color("black")
            y_line_drawer.hideturtle()
            y_line_drawer.penup()
            y_line_drawer.goto(YLineIndex*self.block_size, 0)
            y_line_drawer.pendown()
            y_line_drawer.goto(YLineIndex*self.block_size, self.block_size*self.num_rows)

        self.canvas.update()

        self.StartupComputer()

    def StartupComputer(self):
        self.blocks_with_coords = {}
        height = 0
        
        block_coord_finder = turtle.Turtle()
        block_coord_finder.penup()
        block_coord_finder.hideturtle()

        for current_row in range(1, self.num_rows+1):
            for current_column in range(self.num_columns):
                current_block = f"{current_row}S{current_column}"
                if current_block == "1S0":
                    pass
                elif int(block_coord_finder.pos()[0]) == self.block_size*(self.num_columns-1):
                    height += self.block_size
                    block_coord_finder.goto(0, height)
                else:
                    block_coord_finder.forward(self.block_size)
                self.blocks_with_coords[current_block] = block_coord_finder.pos()

        self.Game()

    def Left(self):
        new_pos_list = [None for x in range(4)]
        for index, pos in enumerate(self.current_piece_blockID_pos):
            new_possible_column = int(pos.split("S")[1]) - 1
            current_row = pos.split("S")[0]
            new_possible_pos = f"{current_row}S{new_possible_column}"
            if new_possible_pos in self.blockID_occupation or pos.split("S")[1] == "0":
                new_pos_list = []
                break
            else:
                new_pos_list[index] = new_possible_pos

        if new_pos_list != []:
            self.current_piece_blockID_pos = new_pos_list
            if not self.clear:
                self.clear = True
            self.RenderBlocks()

    def Right(self):
        new_pos_list = [None for x in range(4)]
        for index, pos in enumerate(self.current_piece_blockID_pos):
            new_possible_column = int(pos.split("S")[1]) + 1
            current_row = pos.split("S")[0]
            new_possible_pos = f"{current_row}S{new_possible_column}"
            if new_possible_pos in self.blockID_occupation or pos.split("S")[1] == str(self.num_columns-1):
                new_pos_list = []
                break
            else:
                new_pos_list[index] = new_possible_pos

        if new_pos_list != []:
            self.current_piece_blockID_pos = new_pos_list
            if not self.clear:
                self.clear = True
            self.RenderBlocks()

    def Down(self):
        self.speed_up = True
        self.speed = 0.025
        #print(self.canvas.window_width(), self.canvas.window_height())

    def TurnPiece(self):
        self.new_pos_list = [None for x in range(4)]
        previous_turn_iteration = self.turn_iteration

        if self.turn_iteration == 1:
            self.TurnPiece2(self.turn_list1)
            self.turn_iteration = 2
        elif self.turn_iteration == 2:
            self.TurnPiece2(self.turn_list2)
            self.turn_iteration = 3
        elif self.turn_iteration == 3:
            self.TurnPiece2(self.turn_list3)
            self.turn_iteration = 4
        elif self.turn_iteration == 4:
            self.TurnPiece2(self.turn_list4)
            self.turn_iteration = 1

        stop = False
        zero = False
        nine = False

        for pos in self.new_pos_list:
            if pos not in self.blocks_with_coords.keys():
                stop = True
                self.turn_iteration = previous_turn_iteration
                break
            if pos in self.blockID_occupation:
                stop = True
                self.turn_iteration = previous_turn_iteration
                break

        if not stop:
            for pos in self.new_pos_list:
                if str(pos).endswith("0"):
                    zero = True
                if str(pos).endswith(f"{self.num_columns-1}"):
                    nine = True
            if zero and nine:
                self.turn_iteration = previous_turn_iteration
            else:
                self.current_piece_blockID_pos = self.new_pos_list
                if not self.clear:
                    self.clear = True
                self.RenderBlocks()

    def TurnPiece2(self, turn_list):
        for index, pos in enumerate(self.current_piece_blockID_pos):
            current_row = int(pos.split("S")[0])
            current_column = int(pos.split("S")[1])

            row_add = int(turn_list[index].split("S")[0])
            column_add = int(turn_list[index].split("S")[1])

            self.new_pos_list[index] = f"{current_row+row_add}S{current_column+column_add}"

    def RenderBlocks(self):
        if self.clear:
            for index in self.filler:
                self.filler[index].clear()

        if not self.game_started:
            self.current_color = random.choice(self.block_colors)
            self.game_started = True

        self.filler = {1: None, 2: None, 3: None, 4: None}

        for filler_index, blockID in enumerate(self.current_piece_blockID_pos, 1):
            color = self.current_color

            self.RenderBlocks2(color, blockID)
            self.filler[filler_index] = self.current_filler

    def RenderBlocks2(self, color, blockID):
        filler = turtle.Turtle()
        filler.hideturtle()
        filler.penup()
        filler.goto(self.goto_block[blockID])
        filler.fillcolor(color)
        filler.begin_fill()
        filler.forward(self.block_size)
        filler.left(90)
        filler.forward(self.block_size)
        filler.left(90)
        filler.forward(self.block_size)
        filler.end_fill()
        self.current_filler = filler

    def InitiatePiece(self):
        self.StopPieces = False
        self.number = random.randint(1, 5)
        self.number2 = random.randint(1, 2)
        """
        if self.number != 1:
            self.counter += 1
            if self.counter == 10:
                self.number = 1
                self.counter = 0
        else:
            self.counter = 0
        """
        self.stats.append(self.number)

        a = self.num_rows - 18

        b = int(round(self.num_columns * 1 / 2, 0))

        if self.number == 1:  # I
            self.current_piece_blockID_pos = (f"{17+a}S{-2+b}", f"{17+a}S{-1+b}", f"{17+a}S{0+b}", f"{17+a}S{1+b}")
            self.turn_list1 = ("0S0", "1S-1", "2S-2", "3S-3")
            self.turn_list2 = ("0S0", "-1S-1", "-2S-2", "-3S-3")
            self.turn_list3 = ("0S0", "1S1", "2S2", "3S3")
            self.turn_list4 = ("0S0", "-1S1", "-2S2", "-3S3")

        if self.number == 2:  # T
            self.current_piece_blockID_pos = (f"{16+a}S{0+b}", f"{17+a}S{-1+b}", f"{17+a}S{0+b}", f"{17+a}S{1+b}")
            self.turn_list1 = ("1S1", "-1S1", "0S0", "1S-1")
            self.turn_list2 = ("1S-1", "1S1", "0S0", "-1S-1")
            self.turn_list3 = ("-1S-1", "1S-1", "0S0", "-1S1")
            self.turn_list4 = ("-1S1", "-1S-1", "0S0", "1S1")

        if self.number == 3:  # O
            self.current_piece_blockID_pos = (f"{16+a}S{-1+b}", f"{16+a}S{0+b}", f"{17+a}S{-1+b}", f"{17+a}S{0+b}")
            self.turn_list1 = ("0S0", "0S0", "0S0", "0S0")
            self.turn_list2 = ("0S0", "0S0", "0S0", "0S0")
            self.turn_list3 = ("0S0", "0S0", "0S0", "0S0")
            self.turn_list4 = ("0S0", "0S0", "0S0", "0S0")

        if self.number == 4: # S
            self.current_piece_blockID_pos = (f"{16+a}S{-1+b}", f"{16+a}S{0+b}", f"{17+a}S{0+b}", f"{17+a}S{1+b}")
            self.turn_list1 = ("0S1", "1S0", "0S-1", "1S-2")
            self.turn_list2 = ("0S-1", "0S-1", "0S1", "0S1")
            self.turn_list3 = ("0S2", "-1S1", "0S0", "-1S-1")
            self.turn_list4 = ("0S-2", "0S0", "0S0", "0S2")

        if self.number == 5:
            if self.number2 == 1: # J
                self.current_piece_blockID_pos = (f"{15+a}S{-1+b}", f"{15+a}S{0+b}", f"{16+a}S{0+b}", f"{17+a}S{0+b}")
                self.turn_list1 = ("1S0", "0S-1", "-1S0", "-2S1")
                self.turn_list2 = ("1S1", "2S0", "1S-1", "0S-2")
                self.turn_list3 = ("-1S0", "0S1", "1S0", "2S-1")
                self.turn_list4 = ("-1S-1", "-2S0", "-1S1", "0S2")
            else: # L
                self.current_piece_blockID_pos = (f"{15+a}S{1+b}", f"{15+a}S{0+b}", f"{16+a}S{0+b}", f"{17+a}S{0+b}")
                self.turn_list1 = ("0S-2", "1S-1", "0S0", "-1S1")
                self.turn_list2 = ("2S1", "1S2", "0S1", "-1S0")
                self.turn_list3 = ("-1S2", "-2S1", "-1S0", "0S-1")
                self.turn_list4 = ("-1S-1", "0S-2", "1S-1", "2S0")

    def DeletePieces(self, all_rows={}):
        do = True
        do2 = False

        while do:
            do = False

            for row_number in range(1, self.num_rows+1):
                all_rows[row_number] = 0

            for row_list in self.all_rows_dict:
                for ID in self.blockID_occupation:
                    if ID in self.all_rows_dict[row_list]:
                        all_rows[row_list] += 1
                if all_rows[row_list] == self.num_columns:
                    do = True
                    do2 = True
                    self.score += int(round(50 * (1 - 2 * self.speed) * self.num_columns / self.num_rows, 0))
                    self.scoreboard_text.clear()
                    self.scoreboard_text.write("Pisteet: {}".format(self.score), font=("Terminal", int(0.6*self.block_size)))

                    for r in self.all_rows_dict[row_list]:
                        self.blockID_occupation.remove(r)

                    for index, blockID in enumerate(self.blockID_occupation):
                        current_row = int(blockID.split("S")[0])
                        current_column = int(blockID.split("S")[1])
                        if current_row > row_list:
                            new_row = current_row - 1
                            new_blockID = f"{new_row}S{current_column}"
                            self.blockID_occupation[index] = new_blockID
                            self.color_dict[new_blockID] = self.color_dict[blockID]

                    break
                if do:
                    break

            if do == False and do2 == True:
                for n in self.fillers:
                    n.clear()

                self.fillers = []

                for ID in self.blockID_occupation:
                    self.RenderBlocks2(self.color_dict[ID], ID)
                    self.fillers.append(self.current_filler)

    def Game(self):
        self.canvas.listen()

        while not self.end_game:
            if self.StopPieces == True:
                self.InitiatePiece()

            for block in self.current_piece_blockID_pos:
                if block in self.blockID_occupation:
                    with open("paras", "r") as f:
                        best_score = f.read()

                    if self.score > int(best_score):
                        with open("paras", "w") as f:
                            f.write(str(self.score))
                            best_score = self.score

                    self.end_text.goto(17/100*self.block_size*self.num_columns, self.block_size*(self.num_rows+1)/2)
                    self.end_text.write("Peli loppui!"
                                        "\nParas tulos:"
                                        f"\n{best_score}", font=("Terminal", int(0.7*self.block_size), "bold"))

                    self.end_game = True
                    stats2 = {1 : 0,
                              2 : 0,
                              3 : 0,
                              4 : 0,
                              5 : 0}

                    for n in range(1, 6):
                        for block in self.stats:
                            if block == n:
                                stats2[n] += 1

                    print(stats2)
                    self.canvas.exitonclick()
                    continue

            self.goto_block = self.blocks_with_coords

            self.RenderBlocks()

            self.canvas.update()

            for height in self.current_piece_blockID_pos:
                next_possible_row = int(height.split("S")[0]) - 1
                current_height = height.split("S")[1]
                next_possible_height = f"{next_possible_row}S{current_height}"
                if height in self.all_rows_dict[1] or next_possible_height in self.blockID_occupation:
                    self.StopPieces = True
                    if self.speed_up:
                        self.speed_up = False
                        self.speed = self.default_speed
                    break

            initiate_list = []

            if not self.StopPieces:
                for height in self.current_piece_blockID_pos:
                    new_row = int(height.split("S")[0]) - 1
                    current_column = height.split("S")[1]
                    new_height = f"{new_row}S{current_column}"
                    initiate_list.append(new_height)
                self.current_piece_blockID_pos = initiate_list

            time.sleep(self.speed)

            self.clear = True

            if self.StopPieces:
                self.game_started = False
                self.clear = False

                for filler in self.filler.values():
                    self.fillers.append(filler)

                self.turn_iteration = 1

                for occupied_block in self.current_piece_blockID_pos:
                    self.blockID_occupation.append(occupied_block)
                    self.color_dict[occupied_block] = self.current_color

                self.DeletePieces()


GameWindow()