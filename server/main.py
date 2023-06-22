# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
from urllib.parse import unquote

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    b64 = "5Y+C5pWw"
    text = base64.b64decode(b64)
    print(text.decode('utf-8'))

    s = bytes("参数", 'utf-8')
    text = base64.b64encode(s).decode()
    print(text)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
