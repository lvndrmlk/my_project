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
        return self.int_cnt == 0

    def add(self, p):
        return Point(p, self.int_cnt)
    
    
class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, int_cnt):
        self.int_cnt = int_cnt
        self.p = p

    def find_intersections(self):
        self.int_cnt = 1 if self.p.x**2 + self.p.y**2 == 1 else 0
        return self.int_cnt

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, int_cnt = 0)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, int_cnt):
        self.p, self.q = p, q
        self.int_cnt = int_cnt


    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

        
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
        

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.int_cnt)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            self.int_cnt -= 1
            return Segment(r, self.q, self.int_cn)
        else:
            self.int_cnt -= 1
            return Segment(self.p, r, self.int_cnt)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, int_cnt):    #deq.points: |1|2|3| deq.count: |1|2|1| 
        self.int_cnt = int_cnt                              #count: 4
        self.int_count = 0
        self.points = Deq()
        self.count = Deq()
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
            self.int_count = Segment(self.points.last(), self.points.first(), 0).find_intersections()

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()         #deq.points: -|2|3|
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                # count ints
                self.int_count += Segment(p, self.points.first(), 0).find_intersections()
                if p.x**2 + p.y**2 ==1:
                     self.int_count += 1
                if self.points.last().x**2 + self.points.last().y**2 ==1:
                     self.int_count += 1
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека     deq.points: -|2|-|
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self.int_count += Segment(p, self.points.last(), 0).find_intersections()
                p = self.points.pop_last()
            self.points.push_last(p)    #deq.points: -|2|3|    

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)      #deq.points: 4|2|3|  deq.count: |1|2|2| 
                                                        #count: 5
        else:
            self.int_count = None

        return self
    
# deq.point: |5|4|2|3| deq.count: |2|1|2|1| count: 6

    def find_intersections(self):
        a = None
        b = None
        c = None 

        if self.to_front == True:
            c = self.points.first()
            tmp = self.points.pop_first()
            b = self.points.first()
            self.points.push_first(tmp)
            a = self.points.last()
        else:
            c = self.points.last()
            tmp = self.points.pop_last()
            b = self.points.last()
            self.points.push_last(tmp)
            a = self.points.first()
            
        if self.int_count != None: 
            self.int_cnt += Segment(a, b, 0).find_intersections() + \
            Segment(a, c, 0).find_intersections() - self.int_count

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
