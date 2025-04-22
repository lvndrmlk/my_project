from deq import Deq
from r2point import R2Point
from sympy import *


class Figure:
    """ Абстрактная фигура """
    int_cnt = 0

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """
    
    def find_intersections(self):
        return 0

    def add(self, p):
        return Point(p)
    
    
class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def find_intersections(self):
        return int(self.p.on_circle)

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    # returns intersections only for interval
    def _find_intersections(self):
        x, y = symbols('x y')
        circle_eq = Eq(x**2 + y**2, 1)

        a = self.p
        b = self.q
        
        line_eq = Eq((x - a.x)*(b.y - a.y), (y - a.y)*(b.x - a.x))
        solutions = solve([circle_eq, line_eq], (x, y))
        
        cnt_interval = 0

        for sol in solutions:
            try:
                x_val = float(sol[0])
                y_val = float(sol[1])
            except(TypeError):
                continue
            c = Point(R2Point(x_val, y_val))
            if ((min(b.x, a.x) <= x_val <= max(b.x, a.x) and 
                min(b.y, a.y) <= y_val <= max(b.y, a.y))) and \
                a != c and b != c:
                cnt_interval += 1

        return cnt_interval


    def find_intersections(self):
        self.int_cnt = (self._find_intersections() + self.p.on_circle + self.q.on_circle)
        return self.int_cnt
        

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.int_cnt)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, int_cnt):     
        self.int_cnt = int_cnt                             
        self.points = Deq()
        self.points.push_first(b)
        self.to_front = True
        if b.is_light(a, c):
            self.points.push_first(a) # 0.5|1.1|-|-|-|-3.3
            self.points.push_last(c)
            self.to_front = False
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))


    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for _ in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):
            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            # add checker for segment (last first)
            self.int_cnt -= Segment(self.points.first(), self.points.last())._find_intersections()
            #берет не ту точку, скипает ребро 
            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()    
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                # лажа, цикл не все освещенные ребра перебирает.
                self.int_cnt -= Segment(p, self.points.first()).find_intersections()
                p = self.points.pop_first() # internal point
                self.int_cnt -= int(p.on_circle)
            else:
                self.int_cnt -= p.on_circle
            self.points.push_first(p)
            self.int_cnt += p.on_circle

            # удаление освещённых рёбер из конца дека   
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self.int_cnt -= Segment(p, self.points.last()).find_intersections()
                p = self.points.pop_last()
            else:
                self.int_cnt -= p.on_circle
            self.points.push_last(p) 
            self.int_cnt += p.on_circle     

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            # check intersections on circle for t
            self.points.push_first(t)  
        return self
    

    def find_intersections(self):
        if self.to_front == True:
            a = self.points.pop_first()
            b = self.points.first()
            self.points.push_first(a)
            c = self.points.last()
            self.int_cnt += Segment(a, c)._find_intersections() + \
            Segment(b, c)._find_intersections() + int(c.on_circle)
        else:
            a = self.points.first()
            c = self.points.last()
            b = self.points.pop_last()
            self.points.push_first(b)
            self.int_cnt += Segment(a, c)._find_intersections() + \
            Segment(b, c)._find_intersections() + int(c.on_circle)

        return self.int_cnt


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
