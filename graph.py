from graphics import *
from time import *


def setObjCoords(obj, newX, newY):
    obj.move(newX - obj.getCenter().getX(), newY - obj.getCenter().getY())


if __name__ == '__main__':
    win = GraphWin("circle", 400, 300, autoflush = False)
    point1 = Point(200, 150)
    point2 = Point(250, 200)
    circle = Rectangle(point1, point2)
    circle.draw(win)
    update()
    clickPoint = None
    while(win):
        clickPoint = win.checkMouse()
        if clickPoint != None:
            setObjCoords(circle, clickPoint.getX(), clickPoint.getY())
        
    win.close()