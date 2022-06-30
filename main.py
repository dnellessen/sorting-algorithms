from tkinter import *
from tkinter.ttk import Scale

import numpy as np
import random
import time

import algorithms


class Timer:
    start = None
    running = False

    @staticmethod
    def difference():
        return time.perf_counter() - Timer.start


class Bars:
    def __init__(self, array):
        self.array = array
        self.selected = None

        self.canvas_margin = 10
        self.canvas = Canvas(
            win, width=WIDTH-self.canvas_margin, height=HEIGHT)

        self.bar_margin = 0
        self.bar_width = (WIDTH - self.canvas_margin) / len(array)

    def draw(self):
        x0, x1 = self.bar_margin, self.bar_width
        for index, element in enumerate(self.array):
            color = 'red' if index == self.selected else 'white'

            self.canvas.create_rectangle(
                x0,
                HEIGHT,
                x1,
                HEIGHT-element*1,
                fill=color,
                outline=color,
                tags='bar',
            )
            x0 += self.bar_width
            x1 += self.bar_width

        self.canvas.pack()

    def update(self, array, selected=None):
        self.array = array
        self.selected = selected

        self.canvas.delete('bar')
        self.draw()

        if Timer.running:
            timer_label.config(text=f'{round(Timer.difference(), 2)}s')

        win.update_idletasks()


class Array:
    max_len = 500
    length = 200

    def __init__(self):
        self.step = self.max_len/self.length
        self.array = [int(i) for i in np.arange(0, self.max_len, self.step)]

    @property
    def get(self):
        return self.array

    def change(self, x):
        self.length = int(len_scale.get())

        if self.length == int(len_label.cget("text")):
            return

        len_label.config(text=self.length)

        bars.bar_margin = 0
        bars.bar_width = (WIDTH - bars.canvas_margin) / self.length

        self.step = self.max_len/self.length
        self.array = [int(i) for i in np.arange(0, self.max_len, self.step)]

        self.shuffle(animate=False)

    def shuffle(self, animate=True):
        for i in reversed(range(1, len(self.array))):
            x = random.randint(0, i)
            self.array[i], self.array[x] = self.array[x], self.array[i]
            if animate:
                bars.update(self.array)
        bars.update(self.array)

    def sort(self):
        config('disabled')

        Timer.running = True
        Timer.start = time.perf_counter()

        algorithm = algorithms.get(menu_var.get()).func
        algorithm(self.array, bars)

        bars.selected = None
        bars.draw()

        Timer.running = False
        win.after(5000, lambda: timer_label.config(text='0.00s'))

        config('normal')


def config(state):
    menu.config(state=state)
    shuffle_btn.config(state=state)
    sort_btn.config(state=state)
    len_scale.config(state=state)



WIDTH, HEIGHT = 800, 550


array = Array()
algorithms.init()


win = Tk()
win.title('Sorting Algorithms')
win.geometry(f'{WIDTH}x{HEIGHT}')
win.resizable(False, False)


bars = Bars(array.get)
array.shuffle()
bars.draw()


menu_var = StringVar()
menu_var.set(algorithms.names[-1])
menu_var.trace('w', lambda x, y, z: tcomplexities_label.config(
    text=algorithms.get(menu_var.get()).timecomplexity))

menu = OptionMenu(win, menu_var, *algorithms.names)
menu.config(width=10, font=('Helvetica', 12), disabledforeground='white')
menu.place(x=10, y=10)


sort_btn = Button(text='Sort', width=5, command=array.sort)
sort_btn.place(x=140, y=5)

shuffle_btn = Button(text='Shuffle', width=5, command=array.shuffle)
shuffle_btn.place(x=225, y=5)


len_label = Label(text=array.length)
len_label.place(x=520, y=10)
len_scale = Scale(from_=10, to=array.max_len, value=array.length, orient=HORIZONTAL, length=200,
                  command=array.change)
len_scale.place(x=320, y=10)


timer_label = Label(text='0.00s', anchor='e', width=6)
timer_label.place(x=WIDTH-70, y=10)

tcomplexities_label = Label(
    text=algorithms.get(menu_var.get()).timecomplexity, anchor='center', width=15)
tcomplexities_label.place(x=580, y=10)


win.mainloop()
