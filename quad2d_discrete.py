import math

class quad2d_discrete:

    g = 9.81

    def __init__(self, m, td):
        self.m = m
        self.td = td
        self.x = 0
        self.dx = 0
        self.z = 0
        self.dz = 0
        self.w = 0

    def step(self, F, dw):

        ddx = -F*math.sin(self.w) - F*math.sin(dw*self.td^2/2)
        ddz = F*math.cos(self.w) + F.math.cos(dw*self.td^2/2)

        self.x = self.x + self.td*self.dx + self.td^2*ddx/2
        self.dx = self.dx + self.td*ddx

        self.z = self.z + self.td * self.dz + self.td ^ 2 * ddz / 2
        self.dz = self.dz + self.td * ddz

        self.w = self.w + self.td*dw
