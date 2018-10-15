import sys
from pynput import keyboard

test = """
I am really long string ' with some shitty text 432; 
helloWorld = 424; 
input.add(sometimes, but);
"""


if __name__ == '__main__':
    sys.stdout.flush()
    sys.stdout.write(
        'Welcome to the TypeMaster64. Get ready for pain in your ass.')
    sys.stdout.write(test)
