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

m = 100  # Anzahl der Splines
k = 3   # Grad des Polynoms


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
                point_list[i][0],
                point_list[i][1],

                point_list[i+1][0],
                point_list[i+1][1],

                fill=color, width=LINE_WIDTH
            )
            canvas_element_list.append(element)


def deboor(j, i, degree, controlpoints, knotvector, t):
    """
    Deboor Algorithmus
    Seite 293 Vorlesung

    :param j:
    :param i:
    :param degree:
    :param controlpoints:
    :param knotvector:
    :param t:
    :return:
    """
    if j == 0:
        if i == len(controlpoints):
            return controlpoints[i - 1]
        else:
            return controlpoints[i]

    a = (t - knotvector[i])
    b = (knotvector[i - j + degree] - knotvector[i])

    if b == 0:
        a_j_i = 0
    else:
        a_j_i = a / b

    first_result = deboor(j - 1, i - 1, degree, controlpoints, knotvector, t)
    second_result = deboor(j - 1, i, degree, controlpoints, knotvector, t)
    return [
        ((1 - a_j_i) * first_result[0]) + (a_j_i * second_result[0]),
        ((1 - a_j_i) * first_result[1]) + (a_j_i * second_result[1])
    ]


def draw_bezier_curve():
    """
    Erstellt Kontrollpunkte abhängig von m und k
    Zeichnet die dazugehörige Bezier-Kurve
    """
    global k, m, canvas_element_list, control_point_list

    points = []

    knotvector = []
    n = len(control_point_list)
    print(k)

    if n < k:
        return

    # knotvector is n + k + 1
    for _ in range(k):
        knotvector.append(0)

    # + 1 because range(n) iterates to (n - 1)
    # +1 weil range
    for i in range(1, n - (k - 1) + 1):
        knotvector.append(i)

    for _ in range(k):
        knotvector.append(n - (k - 2))

    for i in range(m):
        # interpolate between zero and m in the knotvector
        current_t = max(knotvector) * (i / m)
        r = None

        for j in range(len(knotvector)):
            if knotvector[j] <= current_t < knotvector[j + 1]:
                r = j
                break

        if r is None:
            raise Exception('t is not in the knotvector!')

        # deboor(j, i, degree, pointList, knotVector, t)
        points.append(deboor(k - 1, r, k, control_point_list, knotvector, current_t))

    # render the points i collected as lines
    for i in range(len(points)):
        if i < len(points) - 1:
            canvas_element_list.append(
                canvas.create_line(
                    points[i][0],
                    points[i][1],
                    points[i + 1][0],
                    points[i + 1][1],
                    fill=BEZIER_COLOR,
                    width=BEZIER_WIDTH,
                )
            )


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
    draw_bezier_curve()


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
