from graphics import *
from time import *

vertex_radius = 30

class Vertex:
    def __init__(self, point):
        self.center = point
        self.circle = Circle(point, vertex_radius)
        self.circle.setFill("white")
        self.edges = []

    def check_clicked(self, point):
        dx = point.getX() - self.center.getX()
        dy = point.getY() - self.center.getY()

        return (dx**2 + dy**2) < vertex_radius**2

    def draw(self, win):
        self.circle.draw(win)

    def undraw(self):
        self.circle.undraw()


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.line = Line(v1.center, v2.center)
        v1.edges.append(self)
        v2.edges.append(self)

    def draw(self, win):
        self.line.draw(win)

    def undraw(self):
        self.line.undraw()



class Graph:
    def __init__(self):
        self.win = GraphWin("circle", 800, 600, autoflush = False)
        self.vertexes = []
        self.edges = []
    
    def add_vertex(self, vertex):
        self.vertexes.append(vertex)

    def create_vertex(self, point):
        new_vertex = Vertex(point)
        new_vertex.draw(self.win)
        self.add_vertex(new_vertex)

    def add_edge(self, edge):
        self.edges.append(edge)

    def create_edge(self, v1, v2):
        new_edge = Edge(v1, v2)
        new_edge.draw(self.win)
        self.add_edge(new_edge)

    def check_collision(self, point):
        return
    
    def check_vertex_click(self, point):
        for v1 in self.vertexes:
            if v1.check_clicked(point):
                v1.circle.setOutline("red")
                second_click = self.win.getMouse()
                self.win.checkKey()
                for v2 in self.vertexes:
                    if v1 != v2 and v2.check_clicked(second_click):
                        v1.circle.setOutline("black")
                        self.create_edge(v1, v2)
                        return True
                
                v1.circle.setOutline("black")
                return True

        return False
            


    def delete_graph(self):
        for v in self.vertexes:
            v.undraw() 
        self.vertexes = []

        for e in self.edges:
            e.undraw()
        self.edges = []



def setObjCoords(obj, newX, newY):
    obj.move(newX - obj.getCenter().getX(), newY - obj.getCenter().getY())


if __name__ == '__main__':
    graph = Graph()
    clickPoint = None
    while(True):
        clickPoint = graph.win.checkMouse()
        if clickPoint != None:
            if not graph.check_vertex_click(clickPoint):
                graph.create_vertex(clickPoint)

        keyPressed = graph.win.checkKey()
        if keyPressed != "":
            match keyPressed:
                case "Escape":
                    break
                case "BackSpace":
                    graph.delete_graph()
        
    graph.win.close()