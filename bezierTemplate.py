from tkinter import *
import sys

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 2  # half of point size (must be integer)
CCOLOR = "#0000FF"  # blue (color of control-points and polygon)

BCOLOR = "#000000"  # black (color of bezier curve)
BWIDTH = 2  # width of bezier curve

ACCURACY = 100

pointList = []  # list of (control-)points
elementList = []  # list of elements (used by Canvas.delete(...))

DEFAULT_K = 3
DEFAULT_M = 100

scale_k = None
scale_m = None
switch_algorithm = None
current_algorithm = None

DECASTELJAU = 'decasteljau'
DEBOOR = 'deboor'
ALGORITHM = DEBOOR

"""

------------------------------------------------------------------------------------------------------------------------

Abgabe von Michael Bykovski
Matrikelnummer: 477734

------------------------------------------------------------------------------------------------------------------------

"""


def drawPoints():
    """ draw (control-)points """
    for p in pointList:
        element = can.create_oval(p[0] - HPSIZE, p[1] - HPSIZE,
                                  p[0] + HPSIZE, p[1] + HPSIZE,
                                  fill=CCOLOR, outline=CCOLOR)
        elementList.append(element)


def drawPolygon():
    """ draw (control-)polygon conecting (control-)points """
    if len(pointList) > 1:
        for i in range(len(pointList) - 1):
            element = can.create_line(pointList[i][0], pointList[i][1],
                                      pointList[i + 1][0], pointList[i + 1][1],
                                      fill=CCOLOR)
            elementList.append(element)


def de_casteljau(t, point_list):
    """
    der de casteljau algorithmus

    :return: calculated_point
    :rtype: point
    """
    if len(point_list) < 2:
        return 0

    temp_point_list = []

    for i in range(len(point_list)):
        if i < len(point_list) - 1:
            new_point = []
            first_point = point_list[i]
            second_point = point_list[i + 1]

            new_point.append((1 - t) * float(first_point[0]))
            new_point.append((1 - t) * float(first_point[1]))

            new_point[0] += t * float(second_point[0])
            new_point[1] += t * float(second_point[1])

            temp_point_list.append(new_point)

    if len(temp_point_list) == 1:
        return temp_point_list[0]

    if len(temp_point_list) > 1:
        return de_casteljau(t, temp_point_list)


def deboor(j, i, degree, controlpoints, knotvector, t):
    """
    The deboor algorithm
    Information taken from Vorlesung: S.293

    :param j: iterator j
    :type j: int
    :param i: iterator i
    :type i: int
    :param degree: degree of b-spline curve
    :type degree: int
    :param controlpoints: the points of the curve polygon
    :type controlpoints: list
    :param knotvector: knot vector
    :type knotvector: list
    :param t: t value
    :type t: float
    :return: the result value on the curve
    :rtype: list (Point)
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


def drawBezierCurve():
    """ draw bezier curve defined by (control-)points """
    points = []
    m = scale_m.get()

    if ALGORITHM == DECASTELJAU:
        if len(pointList) >= 3:
            for i in range(m):
                current_t = float(i) / m
                points.append(de_casteljau(current_t, pointList))

    elif ALGORITHM == DEBOOR:
        knotvector = []
        k = scale_k.get()
        m = scale_m.get()
        n = len(pointList)

        if n < k:
            return

        # knotvector is n + k + 1
        for _ in range(k):
            knotvector.append(0)

        # + 1 because range(n) iterates to (n - 1)
        for i in range(1, n - (k - 1) + 1):
            knotvector.append(i)

        for _ in range(k):
            knotvector.append(n - (k - 2))

        # testing
        # knotvector = [0, 1, 2, 3, 4, 5, 6, 7]

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
            points.append(deboor(k - 1, r, k, pointList, knotvector, current_t))

    # render the points i collected as lines
    for i in range(len(points)):
        if i < len(points) - 1:
            elementList.append(
                can.create_line(
                    points[i][0],
                    points[i][1],
                    points[i + 1][0],
                    points[i + 1][1],
                    fill=BCOLOR,
                    width=BWIDTH,
                )
            )


def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawPolygon()
    drawBezierCurve()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    print("left mouse button clicked at ", event.x, event.y)
    pointList.append([event.x, event.y])
    draw()


def toggle_algorithm():
    global ALGORITHM

    if ALGORITHM == DECASTELJAU:
        ALGORITHM = DEBOOR
    elif ALGORITHM == DEBOOR:
        ALGORITHM = DECASTELJAU

    current_algorithm['text'] = 'Current algorithm: {}'.format(ALGORITHM)
    switch_algorithm['text'] = 'Switch to algorithm: {}'.format(DECASTELJAU if ALGORITHM == DEBOOR else DEBOOR)


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 1:
        print("pointViewerTemplate.py")
        sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>", mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    options_frame = Frame(mw)
    options_frame.pack(side='bottom')
    scale_k_label = Label(options_frame, text='Scale K')
    scale_k_label.pack()
    scale_k = Scale(options_frame, from_=1, to=20, orient=HORIZONTAL, resolution=1)
    scale_k.set(DEFAULT_K)
    scale_k.pack()

    scale_m_label = Label(options_frame, text='Scale M')
    scale_m_label.pack()
    scale_m = Scale(options_frame, from_=10, to=1000, orient=HORIZONTAL, resolution=10)
    scale_m.set(DEFAULT_M)
    scale_m.pack()

    current_algorithm = Label(options_frame, text='Current algorithm: {}'.format(ALGORITHM))
    current_algorithm.pack()
    switch_algorithm = Button(
        options_frame,
        text='Switch to algorithm: {}'.format(DECASTELJAU),
        command=toggle_algorithm
    )
    switch_algorithm.pack()
    # start
    mw.mainloop()
