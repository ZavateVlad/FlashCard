from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
data = pandas.read_csv('data/german_words.csv')
data = data.to_dict(orient='records')
random_word = {}
to_learn = {}


try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/german_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global random_word, flip_timer
    # Protection against spam
    screen.after_cancel(flip_timer)
    random_word = random.choice(data)
    canvas.itemconfig(card_title, text='German', fill='black')
    canvas.itemconfig(card_word, text=random_word['German'], fill='black')
    canvas.itemconfig(card, image=front)
    # Flips the card whenever the button is pressed
    # (It changes to german and after 3 seconds changes to english,
    # but if the button is not pressed again, the english translation remains)
    flip_timer = screen.after(3000, func=flip)


def flip():
    canvas.itemconfig(card, image=back)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=random_word['English'], fill='white')


def is_known():
    to_learn.remove(random_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv')
    next_card()


screen = Tk()
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
# Initializes the first run, and then is not used anymore
# (If the user does not click any button, the flip occurs anyway
flip_timer = screen.after(3000, func=flip)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front = PhotoImage(file='images/card_front.png')
back = PhotoImage(file='images/card_back.png')
card = canvas.create_image(400, 263, image=front)
card_title = canvas.create_text(400, 150, text='', font=('Ariel', 25, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Ariel', 40, 'italic'))
canvas.grid(row=0, column=0, columnspan=2)

wrong = PhotoImage(file='images/wrong.png')
red_button = Button(image=wrong, highlightthickness=0, command=next_card)
red_button.grid(row=1, column=0)

correct = PhotoImage(file='images/right.png')
correct_button = Button(image=correct, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)

next_card()

screen.mainloop()
