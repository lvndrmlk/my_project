from deq import Deq
from r2point import R2Point
from sympy import *

class Figure:
    """ Абстрактная фигура """
    prev_ans = 0
    int_cnt = 0 # intersection counter

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0
    
    def find_intersections(self):
        return 0

        
class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)
    
    def find_intersections(self):
        return 0
    

class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)
    
    def find_intersections(self):
        self.int_cnt += 1 if self.p.x**2 + self.p.y**2 == 1 else 0
        return self.int_cnt


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)
    @staticmethod
    def find_intersections(self):
        x, y = symbols('x y')
        circle_eq = Eq(x**2 + y**2, 1)

        a = self.p
        b = self.q
        
        line_eq = Eq((x - a.x)*(b.y - a.y), (y - a.y)*(b.x - a.x))

        
        solutions = solve([circle_eq, line_eq], (x, y))
        
        for sol in solutions:
            try:
                x_val = float(sol[0])
                y_val = float(sol[1])
            except(TypeError):
                continue
            
            if (min(b.x, a.x) <= x_val <= max(b.x, a.x) and 
                min(b.y, a.y) <= y_val <= max(b.y, a.y)):
                self.int_cnt += 1
        
        return self.int_cnt


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        self.to_front = False
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
            self.to_front = True
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
        for n in range(self.points.size()):
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

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        return self
    
    def find_intersections(self):
        self.int_cnt = Segment.find_intersections()
        a = None
        b = None
        c = None
        if self.to_front == True:
            b = self.points.first()
            tmp = self.points.pop_first()
            a = self.points.first()
            self.points.push_first(tmp)
            c = self.points.last()
        else:
            b = self.points.last()
            tmp = self.points.pop_last()
            c = self.points.last()
            self.points.push_last(tmp)
            a = self.points.first()

        sol_num = Segment(a, b).find_intersections() + Segment(b, c).find_intersections()
        if sol_num != self.prev_ans:
            self.int_cnt += sol_num
        self.prev_ans = sol_num
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
