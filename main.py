import sys
import tkinter
import pandas as pd
import random

CARD_FRONT = "../flash-cards-py/images/card_front.png"
CARD_BACK = "../flash-cards-py/images/card_back.png"

BACKGROUND_COLOR = "#B1DDC6"
WORD_DICTIONARY = {}
current_key = 0


def flip_front():
    global current_key

    canvas.itemconfig(picture, image=card_front)
    canvas.itemconfig(lang_text, text="French")
    if len(WORD_DICTIONARY["French"]) > 1:
        current_key = random.randint(0, len(WORD_DICTIONARY["French"]) - 1)
        canvas.itemconfig(word_text, text=WORD_DICTIONARY["French"][current_key])
        reset_timer()
    else:
        canvas.itemconfig(word_text, text="No more Worlds remaining")
        sys.exit()


def flip_back():
    canvas.itemconfig(picture, image=card_back)
    canvas.itemconfig(lang_text, text="English")
    canvas.itemconfig(word_text, text=WORD_DICTIONARY["English"][current_key])


def correct():
    WORD_DICTIONARY["French"].pop(current_key, None)
    WORD_DICTIONARY["English"].pop(current_key, None)
    save_file()
    flip_front()
    reset_timer()


def incorrect():
    flip_front()
    reset_timer()


def reset_timer():
    window.after(3000, flip_back)


def readfile():
    df = pd.DataFrame.empty
    try:
        df = pd.read_csv("data/remaining_words_to_learn.csv")

    except FileNotFoundError:
        df = pd.read_csv("data/french_words.csv")


    dicts = df.to_dict()
    return dicts


def save_file():
    global WORD_DICTIONARY
    df = pd.DataFrame.from_dict(WORD_DICTIONARY)
    df.to_csv("data/remaining_words_to_learn.csv", index=False)


WORD_DICTIONARY = readfile()

# window
window = tkinter.Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, pady=30, padx=30)

# canvas
canvas = tkinter.Canvas(width=800, height=600, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = tkinter.PhotoImage(file=CARD_FRONT)
card_back = tkinter.PhotoImage(file=CARD_BACK)
picture = canvas.create_image(410, 300, image=card_front)
lang_text = canvas.create_text(410, 150, text="Title", font=('Arial', 25, 'italic'))
word_text = canvas.create_text(410, 263, text="Word", font=('Arial', 35, 'bold'))
canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

# buttons

right_image = tkinter.PhotoImage(file="../flash-cards-py/images/right.png")
wrong_image = tkinter.PhotoImage(file="../flash-cards-py/images/wrong.png")
button_wrong = tkinter.Button(image=wrong_image, command=correct, bg=BACKGROUND_COLOR, highlightthickness=0)
button_right = tkinter.Button(image=right_image, bg=BACKGROUND_COLOR, command=correct, highlightthickness=0)
button_wrong.grid(row=2, column=0)
button_right.grid(row=2, column=1)

if WORD_DICTIONARY is not None:
    flip_front()
else:
    exit()

window.mainloop()
