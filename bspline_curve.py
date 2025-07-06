import numpy as np
from curve_base import CurveBase


class BSplineCurve(CurveBase):
 
    def __init__(self, initial_points=None, degree=3, color='#45B7D1'):
        if initial_points is None:
            initial_points = [[0.5, 2], [1.5, 4], [2.5, 1], [3.5, 4.5], [4.5, 2], [5.5, 3]]
        super().__init__(initial_points, color)
        self.degree = degree
    
    def generate_knots(self, n, p):
        if n <= p:
            return np.array([0] * (p + 1) + [1] * (p + 1))
        
        knots = []
        
        for i in range(p + 1):
            knots.append(0.0)
        
        for i in range(1, n - p):
            knots.append(i / (n - p))
        
        for i in range(p + 1):
            knots.append(1.0)
        
        return np.array(knots)
    
    def basis_function(self, i, p, t, knots):
        if p == 0:
            return 1.0 if (knots[i] <= t < knots[i + 1]) or (t == 1.0 and knots[i] <= t <= knots[i + 1]) else 0.0
        
        left_coeff = 0.0
        right_coeff = 0.0
        
        if knots[i + p] - knots[i] != 0:
            left_coeff = (t - knots[i]) / (knots[i + p] - knots[i]) * self.basis_function(i, p - 1, t, knots)
        
        if knots[i + p + 1] - knots[i + 1] != 0:
            right_coeff = (knots[i + p + 1] - t) / (knots[i + p + 1] - knots[i + 1]) * self.basis_function(i + 1, p - 1, t, knots)
        
        return left_coeff + right_coeff
    
    def evaluate_curve(self, num_points=300):
        n = len(self.points)
        if n <= self.degree:
            return self.points
        
        knots = self.generate_knots(n, self.degree)
        
        curve_points = []
        t_values = np.linspace(0, 1, num_points)
        
        for t in t_values:
            t = max(0, min(1, t))
            
            point = np.zeros(2)
            for i in range(n):
                basis = self.basis_function(i, self.degree, t, knots)
                point += basis * self.points[i]
                
            if np.isfinite(point).all():
                curve_points.append(point)
        
        return np.array(curve_points) if curve_points else self.points
    
    def can_remove_point(self):
        return len(self.points) > self.degree + 1