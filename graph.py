from graphics import *
from time import *

vertex_radius = 30

class Vertex:
    def __init__(self, point, num):
        self.center = point
        self.circle = Circle(point, vertex_radius)
        self.circle.setFill("white")
        self.circle.setWidth(5)
        self.edges = []
        self.num = num
        self.text = Text(self.center, str(self.num))
        self.text.setSize(20)
        

    def check_clicked(self, point):
        dx = point.getX() - self.center.getX()
        dy = point.getY() - self.center.getY()

        return (dx**2 + dy**2) < vertex_radius**2
    
    def check_near(self, point):
        dx = point.getX() - self.center.getX()
        dy = point.getY() - self.center.getY()

        return (dx**2 + dy**2) < (vertex_radius*2 + 5)**2

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def draw(self, win):
        self.circle.draw(win)
        self.text.draw(win)

    def undraw(self):
        self.circle.undraw()
        self.text.undraw()


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.line = Line(v1.center, v2.center)
        self.line.setWidth(5)
        v1.edges.append(self)
        v2.edges.append(self)

    def draw(self, win):
        self.line.draw(win)
        self.v1.undraw()
        self.v2.undraw()
        self.v1.draw(win)
        self.v2.draw(win)

    def undraw(self):
        self.line.undraw()

    def check_clicked(self, point):
        xv1 = self.v1.center.getX()
        yv1 = self.v1.center.getY()
        xv2 = self.v2.center.getX()
        yv2 = self.v2.center.getY()

        px = point.getX()
        py = point.getY()

        if px <= max(xv1, xv2) and px >= min(xv1, xv2) and py <= max(yv1, yv2) and py >= min(yv1, yv2):
            if xv1 - xv2 == 0:
                return px <= xv1 + 10 and px >= xv1 + 10
    
            line_slope = (yv1 - yv2) / (xv1 - xv2)
            b = yv1 - line_slope*xv1

            con1 = py <= line_slope * px + b + 10 and py >= line_slope * px + b - 10
            con2 = py  <= line_slope * (px + 10) + b and py >= line_slope * (px - 10) + b
            return con1 or con2
        return False
    
    def check_near(self, point):
        xv1 = self.v1.center.getX()
        yv1 = self.v1.center.getY()
        xv2 = self.v2.center.getX()
        yv2 = self.v2.center.getY()

        px = point.getX()
        py = point.getY()

        if px <= max(xv1, xv2) + 40 and px >= min(xv1, xv2) - 40 and py <= max(yv1, yv2) + 40 and py >= min(yv1, yv2) - 40:
            if xv1 - xv2 == 0:
                return px <= xv1 + 40 and px >= xv1 + 40
    
            line_slope = (yv1 - yv2) / (xv1 - xv2)
            b = yv1 - line_slope*xv1

            con1 = py <= line_slope * px + b + 40 and py >= line_slope * px + b - 40
            con2 = py  <= line_slope * (px + 40) + b and py >= line_slope * (px - 40) + b
            return con1 or con2
        return False
    

    def delete_edge(self, win):
        self.v1.remove_edge(self)
        self.v2.remove_edge(self)
        win.edges.remove(self)
        self.undraw()



class Graph:
    def __init__(self):
        self.win = GraphWin("circle", 800, 600, autoflush = False)
        self.vertexes = []
        self.edges = []
        self.vertex_num = 0
    
    def add_vertex(self, vertex):
        self.vertexes.append(vertex)

    def create_vertex(self, point):
        graph.vertex_num += 1
        new_vertex = Vertex(point, graph.vertex_num)
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
                
                while(True):
                    if(self.win.checkKey() == "BackSpace"):
                        v1.undraw()
                        self.vertexes.remove(v1)
                        for e in v1.edges:
                            e.delete_edge(self)
                        return True
                    
                    second_click = self.win.checkMouse()
                    if second_click != None:
                        v1.circle.setOutline("black")
                        for v2 in self.vertexes:
                            if v1 != v2 and v2.check_clicked(second_click):
                                self.create_edge(v1, v2)
                                return True
                        
                        return False
                    
                    #v1.circle.setOutline("black")

        return False
    
    def check_edge_click(self, point):
        for e in self.edges:
            if e.check_clicked(point):
                e.line.setOutline("red")
                while(True):
                    if(self.win.checkMouse() != None):
                        e.line.setOutline("black")
                        return True
                    
                    if(self.win.checkKey() == "BackSpace"):
                        e.delete_edge(self)
                        return True

        return False
    
    def check_click_near_vertex(self, point):
        for v in self.vertexes:
            if v.check_near(point):
                return True
        return False
    
    def check_click_near_edge(self, point):
        for e in self.edges:
            if e.check_near(point):
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
    click_point = None
    while(True):
        click_point = graph.win.checkMouse()
        if click_point != None:
            if not graph.check_vertex_click(click_point):
                if not graph.check_edge_click(click_point):
                    if not graph.check_click_near_vertex(click_point) and not graph.check_click_near_edge(click_point):
                        graph.create_vertex(click_point)
                        

        key_pressed = graph.win.checkKey()
        if key_pressed != "":
            match key_pressed:
                case "Escape":
                    break
                case "BackSpace":
                    graph.delete_graph()
                    graph.vertex_num = 0
    
    graph.win.close()