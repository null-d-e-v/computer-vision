from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from os import path
from click import command

from matplotlib.pyplot import text

from dectection_core import MATCH_METHODS
from dectection_core import custom_cv_from_match

from detection_app_utilities import pop_up
from detection_app_utilities import rect_settings


app = Tk()
app.wm_title("Object Detection System by [nulldev]")
app.geometry("500x500")
app.resizable(0, 0)
app.rowconfigure(index=0, weight=1)
app.columnconfigure(index=0, weight=1)
app.grid

methods_keys = list(MATCH_METHODS.keys())

# ----- GLOBAL VARS -----

selected_method = 0
detection_result = ""
rect_rgb_param = (255, 255, 255)
rect_thickness_param = 2

# ----- EVENTS -----


def set_method(option):
    option = method.get()

    global selected_method
    selected_method = MATCH_METHODS[option]


def set_map_image_path():
    global map_file_finder_route

    file = filedialog.askopenfile(
        initialdir="./resources",
        title="Map image",
        filetypes=(("jpg", "*.jpg"), ("png", "*.png")),
    )

    if not file:
        return

    map_file_finder_route.delete(0, END)
    map_file_finder_route.insert(0, file.name)


def set_target_image_path():
    global target_file_finder_route

    file = filedialog.askopenfile(
        initialdir="./resources",
        title="Map image",
        filetypes=(("jpg", "*.jpg"), ("png", "*.png")),
    )

    if not file:
        return

    target_file_finder_route.delete(0, END)
    target_file_finder_route.insert(0, file.name)


def set_output_folder_path():
    global output_file_finder_route

    folder = filedialog.askdirectory(initialdir=".", title="Output folder")

    if not folder:
        return

    if folder[-1] != "/" or folder[-1] != "\\":
        folder += "/"

    folder = path.normcase(folder)

    output_file_finder_route.delete(0, END)
    output_file_finder_route.insert(0, folder)


def set_rect_params(rgb, thickness):
    global rect_rgb_param
    global rect_thickness_param

    print(rgb, thickness)

    rect_rgb_param = rgb
    rect_thickness_param = thickness


# ----- UI -----

# Image viewer
result_image_label = Label(app, text="No load image")
result_image_label.grid(row=0, columnspan=3, sticky="nsew")


def reload_all_detection():
    global detection_result
    global selected_method
    global result_image_label

    detection_result = custom_cv_from_match(
        map_file_finder_route.get(),
        target_file_finder_route.get(),
        selected_method,
        output_file_finder_route.get(),
        rect_rgb_param,
        rect_thickness_param,
    )

    if detection_result is None:
        pop_up("Error", "No image load")
        return

    load_image = Image.open(detection_result[0]).resize(
        (result_image_label.winfo_width(), result_image_label.winfo_height())
    )
    load_image_component = ImageTk.PhotoImage(load_image)

    result_image_label.configure(text="", image=load_image_component)
    result_image_label.image = load_image_component

    pop_up(
        "Ok", "Generated image!\nExecution: {time}s".format(time=detection_result[1])
    )


# Map image selector
map_file_finder_action = Button(
    app, text="Select map image", command=set_map_image_path
)
map_file_finder_action.grid(row=1, column=2, sticky="we")
map_file_finder_route = Entry(app)
map_file_finder_route.grid(row=1, columnspan=2, sticky="we")

# Target image selector
target_file_finder_action = Button(
    app, text="Select target image", command=set_target_image_path
)
target_file_finder_action.grid(row=2, column=2, sticky="we")
target_file_finder_route = Entry(app)
target_file_finder_route.grid(row=2, columnspan=2, sticky="we")

# Output folder selector
output_file_finder_action = Button(
    app, text="Select out folder", command=set_output_folder_path
)
output_file_finder_action.grid(row=3, column=2, sticky="we")
output_file_finder_route = Entry(app)
output_file_finder_route.grid(row=3, columnspan=2, sticky="we")


# Methods selector
method = StringVar(app)
method.set(methods_keys[0])
methods_drop = OptionMenu(app, method, *methods_keys, command=set_method)
methods_drop.grid(row=4, column=0, sticky="we")

# Rect settings
rect_settings_action = Button(
    app, text="Rect settings", command=lambda: rect_settings(set_rect_params, rect_rgb_param, rect_thickness_param)
)
rect_settings_action.grid(row=4, column=1)

# Reload action
reload_action = Button(app, text="Reload", command=reload_all_detection)
reload_action.grid(row=4, column=2)

app.mainloop()
