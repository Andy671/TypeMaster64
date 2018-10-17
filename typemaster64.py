import sys
import os
import time
import tkinter
import _thread
import random

ERROR_DURATION = 10
QUOTES_LIST = []

target_text = ''
left_text = ''
left_text_string = None
speed_string = None

is_error = False

time_first_character_pressed = 0
time_last_character_pressed = 0
characters_pressed = 0


def getRandomQuote():
    global QUOTES_LIST
    if len(QUOTES_LIST) == 0:
        lines = open('quotes.txt', 'r', encoding='utf-8').readlines()
        QUOTES_LIST = [x.strip() for x in lines]
    choice = random.choice(QUOTES_LIST)
    for i in range(int(len(choice)/50)):
        choice = choice[:50 * (i+1) + i*2] + '\n' + choice[50 * (i+1) + i*2:]
    
    return choice
        


def initText():
    global target_text, left_text, characters_pressed, time_first_character_pressed
    characters_pressed = 0
    time_first_character_pressed = 0
    target_text = open('target.txt', 'r', encoding='utf-8').read()
    left_text = target_text


def refreshUi():
    global left_text_string
    left_text_string.set(left_text)

    try:
        speed_val = int(characters_pressed * 60 /
                        (time_last_character_pressed - time_first_character_pressed))
        speed_string.set(str(speed_val) + 'CPM')
    except ZeroDivisionError:
        pass


def onKeyPressed(event):
    if is_error:
        print('It\'s error time. Chill off.')
        return

    global left_text, time_first_character_pressed, time_last_character_pressed, characters_pressed

    symbol = repr(event.char)
    symbol = str(symbol)
    print('Pressed', symbol)  # repr(event.char))

    if event.char == left_text[0] or (event.char == '\r' and left_text[0] == '\n'):
        left_text = left_text[1:]
        characters_pressed += 1
        time_last_character_pressed = time.time()
    elif event.char != '':
        handleError()

    if time_first_character_pressed == 0:
        time_first_character_pressed = time.time()

    refreshUi()


def handleError():
    print('Error')
    global is_error
    is_error = True
    os.system('afplay /System/Library/Sounds/Glass.aiff')
    _thread.start_new_thread(errorThread, ())
    return


def errorThread():
    global is_error, left_text_string
    
    quote = getRandomQuote()
    for i in range(ERROR_DURATION):
        left_text_string.set(quote + '\n\nTime: ' + str(ERROR_DURATION - i))
        time.sleep(1)

    initText()
    refreshUi()
    is_error = False
    return


if __name__ == '__main__':
    window = tkinter.Tk()
    window.config(padx=24, pady=24)
    window.title("TypeMaster64")
    window.resizable(False, False)

    left_text_string = tkinter.StringVar()
    speed_string = tkinter.StringVar()

    initText()
    refreshUi()

    label_speed = tkinter.Label(
        window, width=20, height=1, textvariable=speed_string)
    label_speed.config(font=('Courier', 24))
    label_speed.pack()

    label_main_content = tkinter.Label(window, width=50, height=15,
                                       textvariable=left_text_string, justify='left', anchor='nw')
    label_main_content.config(
        font=('Courier', 18), underline=0, bg='black', fg='white', padx=8, pady=8)
    label_main_content.pack()

    window.bind('<Key>', onKeyPressed)
    window.mainloop()
