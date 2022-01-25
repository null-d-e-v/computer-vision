from operator import ge
from tkinter import *
from sys import exit
from click import command

from matplotlib.pyplot import text


def validate_int(number):
    if number:
        try:
            int(number)
            return True
        except:
            return False

    return False


def pop_up(title, label):

    pop_root = Tk()
    pop_root.wm_title(title)
    pop_root.geometry("")

    def remove_pop_up():
        pop_root.destroy()

    pop_label = Label(pop_root, text=label)
    pop_label.grid(row=0, column=0)

    pop_close = Button(pop_root, text="ok", command=remove_pop_up)
    pop_close.grid(row=1, column=0)

    pop_root.mainloop()


def rect_settings(setter_callback, default_rgb, default_thickness):
    rect_root = Tk()
    rect_root.wm_title("Rect settings")
    rect_root.geometry("")

    Label(rect_root, text="R").grid(row=0, column=0)
    Label(rect_root, text="G").grid(row=0, column=1)
    Label(rect_root, text="B").grid(row=0, column=2)

    r_input = Entry(rect_root)
    r_input.grid(row=1, column=0)
    r_input.insert(0, default_rgb[0])

    g_input = Entry(rect_root)
    g_input.grid(row=1, column=1)
    g_input.insert(0, default_rgb[1])

    b_input = Entry(rect_root)
    b_input.grid(row=1, column=2)
    b_input.insert(0, default_rgb[2])

    Label(rect_root, text="Thickness").grid(row=2, columnspan=3)
    thickness_input = Entry(rect_root)
    thickness_input.grid(row=3, columnspan=3, sticky="we")
    thickness_input.insert(0, default_thickness)

    def send_data():
        if not (
            validate_int(r_input.get())
            and validate_int(g_input.get())
            and validate_int(b_input.get())
            and validate_int(thickness_input.get())
        ):
            pop_up("Error", "Error found in rect settings")
            return
        else:
            setter_callback(
                (int(r_input.get()), int(g_input.get()), int(b_input.get())),
                int(thickness_input.get()),
            )

            rect_root.destroy()

    send_button = Button(rect_root, text="Ok", command=send_data)
    send_button.grid(row=4, columnspan=3)
