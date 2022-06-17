import numpy
import pygame

class CramerSolver():
    def __init__(self, v1, v2, v3) -> None:

        self.W =    numpy.linalg.det(numpy.array([[v1.x**2, v1.x, 1], [v2.x**2, v2.x, 1], [v3.x**2, v3.x, 1]]))
        self.W_a =  numpy.linalg.det(numpy.array([[v1.y, v1.x, 1], [v2.y, v2.x, 1], [v3.y, v3.x, 1]]))
        self.W_b =  numpy.linalg.det(numpy.array([[v1.x**2, v1.y, 1], [v2.x**2, v2.y, 1], [v3.x**2, v3.y, 1]]))
        self.W_c =  numpy.linalg.det(numpy.array([[v1.x**2, v1.x, v1.y], [v2.x**2, v2.x, v2.y], [v3.x**2, v3.x, v3.y]]))

        self.a = self.W_a/self.W
        self.b = self.W_b/self.W
        self.c = self.W_c/self.W
    
    def result(self):
        return {"a" : self.a, "b" : self.b, "c" : self.c}