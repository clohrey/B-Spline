# coding: utf-8

from tkinter import *

WIDTH = 400
HEIGHT = 400

POINT_SIZE = 2

CONTROL_POINT_COLOR = "#0000FF"

BEZIER_COLOR = "#ff0080"
BEZIER_WIDTH = 2

LINE_WIDTH = 1

control_point_list = []
canvas_element_list = []

drawing_sample_points = True

m = 20  # Anzahl der Splines
k = 4   # Grad des Polynoms


def draw_points(point_list, color):
    """
    interpolierte Kontrollpunkte zeichnen
    :param point_list:
    :param color:
    """
    global canvas_element_list
    
    for point in point_list:
        element = canvas.create_oval(
            point[0] - POINT_SIZE, point[1] - POINT_SIZE,
            point[0] + POINT_SIZE, point[1] + POINT_SIZE,
            fill=color, outline=color
        )
        canvas_element_list.append(element)


def draw_polygon(point_list, color):
    """
    Geraden zwischen zwei interpolierten Kontrollpunkten zeichnen
    :param point_list:
    :param color:
    :return:
    """
    global canvas_element_list

    if len(point_list) > 1:
        for i in range(len(point_list) - 1):
            element = canvas.create_line(
                point_list[i][0], point_list[i][1],
                point_list[i+1][0], point_list[i+1][1],
                fill=color, width=LINE_WIDTH
            )
            canvas_element_list.append(element)


def draw_bezier_curve():
    """
    Erstellt Kontrollpunkte abhängig von m und k
    Zeichnet die dazugehörige Bezier-Kurve
    """
    global control_point_list, m, k


def set_m(slider_m):
    global m
    m = int(slider_m)
    draw()


def set_k(slider_k):
    global k
    k = int(slider_k)
    draw()


def quit_tk(root=None):
    """ quit programm """
    if root is None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    canvas.delete(*canvas_element_list)
    draw_points(control_point_list, CONTROL_POINT_COLOR)
    draw_polygon(control_point_list, CONTROL_POINT_COLOR)

    del control_point_list[:]


def set_draw_sample_points():
    """interpolierte Kontrollpunkte zeichnen"""
    global drawing_sample_points
    drawing_sample_points ^= drawing_sample_points
    draw()


def clear_all():
    canvas.delete(*canvas_element_list)
    del control_point_list[:]


def mouse_event(event):
    control_point_list.append([event.x, event.y])
    draw()


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print("pointViewerTemplate.py")
        sys.exit(-1)

    main_window = Tk()
    main_window.title = "B-spline"

    canvas_frame = Frame(main_window, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    canvas_frame.pack(side="top")
    canvas = Canvas(canvas_frame, width=WIDTH, height=HEIGHT)
    canvas.bind("<Button-1>", mouse_event)
    canvas.pack()

    clear_quit_frame = Frame(main_window)
    clear_quit_frame.pack(side="left")
    clear_button = Button(clear_quit_frame, text="Clear", command=clear_all)
    clear_button.pack(side="left")
    clear_quit_frame = Frame(main_window)
    clear_quit_frame.pack(side="right")
    exit_button = Button(clear_quit_frame, text="Quit", command=(lambda root=main_window: quit_tk(root)))
    exit_button.pack()

    checkbox_frame = Frame(main_window)
    checkbox_frame.pack(side="bottom")

    color_button = Button(checkbox_frame, text="Change Color")
    color_button.pack(side="bottom")

    checkbox = Checkbutton(checkbox_frame, text="Show Points", variable=True, command=set_draw_sample_points)
    checkbox.select()
    checkbox.pack(side="bottom")

    slider_label_m = Label(checkbox_frame, text="m =")
    slider_label_m.pack(side="left")
    m_slider = Scale(checkbox_frame, from_=1, to=400, orient=HORIZONTAL, command=set_m)
    m_slider.set(20)
    m_slider.pack(side="left")

    slider_label_k = Label(checkbox_frame, text="k =")
    slider_label_k.pack(side="left")
    k_slider = Scale(checkbox_frame, from_=2, to=5, orient=HORIZONTAL, command=set_m)
    k_slider.set(20)
    k_slider.pack(side="left")

    main_window.mainloop()
