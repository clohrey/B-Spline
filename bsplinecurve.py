#coding: utf-8
from Tkinter import *
from Canvas import *
from tkColorChooser import askcolor
import sys

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 2  # half of point size (must be integer)
CCOLOR = "#0000FF"  # blue (color of control-points and polygon)

BCOLOR = "#ff0080"  # black (color of bezier curve)
BWIDTH = 2  # Strichbreite der Bezier-Kurve
draw_sample_points = True

pointList = []  # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))

k = 4 # Polynomgrad
m = 20 # Anzahl Splines


def draw_points(points, color):
    """ Zeichnen der (interpolierten) Kontrollpunkte """
    global elementList
    for p in points:
        # Punkt zeichnen
        element = can.create_oval(p[0] - HPSIZE, p[1] - HPSIZE,
                                  p[0] + HPSIZE, p[1] + HPSIZE,
                                  fill=color, outline=color)
        # zur Canvas elementlist hinzufügen
        elementList.append(element)


def draw_polygon(points, color, line_width=1):
    """ Zeichnen der Geraden zwischen zwei (interpolierten) Kontrollpunkten"""
    global elementList
    if len(points) > 1:
        for i in range(len(points) - 1):
            element = can.create_line(points[i][0], points[i][1],
                                      points[i + 1][0], points[i + 1][1],
                                      fill=color, width=line_width)
            elementList.append(element)


def draw_bezier_curve():
    """ Generiert die nötigen Kontrollpunkte abhängig von 'm' und 'k' und zeichnet die entsprechende Bezier-Kurve"""
    global pointList, m, k
    deboor_points = []

    if len(pointList) >= k:
        knotvector = (k - 1) * [0] + range(len(pointList) - (k - 1)) + [len(pointList) - (k - 1)] * (k)

        for i in range(m + 1):
            t = (float(i) / m) * knotvector[-1]
            deboor_points.append(init_deboor(k - 1, pointList, knotvector, t))

        # interpolierten Punkte sollen gezeichnet werden
        if draw_sample_points:
            draw_points(deboor_points, BCOLOR)
        draw_polygon(deboor_points, BCOLOR, BWIDTH)


def deboor(j, i, degree, controlpoints, knotvector, t):
    """de Boor Baum aufbauen"""
    alpha = 0
    b1 = []
    b2 = []
    # es gibt noch keinen vorherigen Punkt *
    if j == 0:
        return controlpoints[i]
    x = (knotvector[i - j + degree + 1] - knotvector[i])

    if x != 0:
        alpha = (t - knotvector[i]) / x
    # vorheriger punkt
    for e in deboor(j - 1, i - 1, degree, controlpoints, knotvector, t):
        b1.append((1 - alpha) * e)
    # aktueller punkt *
    for e in deboor(j - 1, i, degree, controlpoints, knotvector, t):
        b2.append(alpha * e)

    return [x[0] + x[1] for x in zip(b1, b2)]


def init_deboor(degree, controlpoints, knotvector, t):
    r = None

    #drunter?
    if not r:
        r = len(knotvector) - (k + 1)

    for index, knot in enumerate(knotvector):
        # wenn letzter Knoten im Baum erreicht wurde
        if knot > t:
            r = index - 1
            break
    return deboor(degree, r, degree, controlpoints, knotvector, t)


def get_color():
    """Color-Picker für Strichfarbe"""
    global BCOLOR
    color = askcolor()
    BCOLOR = color[1]
    draw()


def set_draw_sample_points():
    """interpolierte Kontrollpunkte zeichnen"""
    global draw_sample_points
    draw_sample_points = not draw_sample_points
    draw()


def set_m(new_m):
    """setzen der Anzahl von Splines"""
    global m
    m = int(new_m)
    draw()


def set_k(new_k):
    """Setzen des gewünschten Polynomgrads"""
    global k
    k = int(new_k)
    draw()

def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    draw_points(pointList, CCOLOR)
    draw_polygon(pointList, CCOLOR)
    draw_bezier_curve()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    pointList.append([event.x, event.y])
    draw()


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print "bsplinecurve.py"
        sys.exit(-1)

    # create main window
    mw = Tk()
    mw.title("schöne Kurven")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>", mouseEvent)
    can.pack()

    eFr = Frame(mw)
    eFr.pack(side="left")
    bClear = Button(eFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    sFr = Frame(mw)
    sFr.pack(side="bottom")

    checkbox = Checkbutton(sFr, text="interpolierte Punkte anzeigen", variable=True, command=set_draw_sample_points)
    checkbox.select()
    checkbox.pack(side="bottom")

    Button(sFr, text='Farbwähler', command=get_color).pack(side="bottom")

    label = Label(sFr, text="m =")
    label.pack(side="left")
    m_slider = Scale(sFr, from_=1, to=400, orient=HORIZONTAL, command=set_m)
    m_slider.set(20)
    m_slider.pack(side="left")

    label = Label(sFr, text="k =")
    label.pack(side="left")
    k_slider = Scale(sFr, from_=2, to=5, orient=HORIZONTAL, command=set_k)
    k_slider.set(4)
    k_slider.pack(side="left")

    # start
    mw.mainloop()

