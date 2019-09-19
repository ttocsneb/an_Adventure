import random
import time


def printSlow(value, min=1, max=30, end='\n', corrupt=False):
    value = str(value)
    for char in value:
        if corrupt and random.randint(0, 20) == 0:
            char = chr(random.randint(0x20, 0xff))
        print(char, end='', flush=True)
        time.sleep((random.random() * (max - min) + min)/1000)
    print('', end=end) # Print a newline


def printSlowColor(*args, end='\n', between='', **kwargs):
    """
    Print slow lines with support for color

    separate colors from text with a new argument

    ```
    printSlowColor(Fore.RED, "I am red\n", Fore.BLUE, "I am blue now")
    ```

    :arg str end: character to print at the end of the command
    :arg str between: character to print between each argument
    :arg number min: minimum delay between each character
    :arg number max: maximum delay between each character
    """
    for text in args:
        if text.startswith('\033'):
            print(text, end='')
        else:
            printSlow(text, end=between, **kwargs)
    print('', end=end)
