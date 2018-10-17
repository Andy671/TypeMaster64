import sys
import os
import time
import tkinter
import _thread

ERROR_DURATION = 5

target_text = open('target.txt', 'r', encoding='utf-8').read()
label_text = None
is_error = False


def refreshUi():
    label_text.set(target_text)


def onKeyPressed(event):
    if is_error:
        print('It\'s error time. Chill off.')
        return

    global target_text

    symbol = repr(event.char)
    symbol = str(symbol)
    print('Pressed', symbol)  # repr(event.char))

    if event.char == target_text[0]:
        target_text = target_text[1:]
    elif event.char == '\r' and target_text[0] == '\n':
        target_text = target_text[1:]
    elif event.char != '':
        handleError()

    refreshUi()


def handleError():
    print('Error')
    global is_error
    is_error = True
    _thread.start_new_thread(continueAfterError,())
    return

def continueAfterError():
    global is_error
    time.sleep(5)
    is_error = False
    return


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("TypeMaster64")

    label_text = tkinter.StringVar()
    refreshUi()

    label = tkinter.Label(window, width=40, height=8,
                          textvariable=label_text, justify='left', anchor='nw')
    label.pack()
    window.bind("<Key>", onKeyPressed)
    window.mainloop()
