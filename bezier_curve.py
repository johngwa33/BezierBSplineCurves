import numpy as np
from curve_base import CurveBase


class BezierCurve(CurveBase):
    def __init__(self, initial_points=None, color='#45B7D1'):
        if initial_points is None:
            initial_points = [[1, 2], [2, 4], [4, 1], [5, 3]]
        super().__init__(initial_points, color)
    
    def de_casteljau(self, points, t):
        """Algoritmul De Casteljau pentru curbele Bezier"""
        if len(points) == 1:
            return points[0]

        new_points = []
        for i in range(len(points) - 1):
            new_point = (1 - t) * points[i] + t * points[i + 1]
            new_points.append(new_point)
        
        return self.de_casteljau(new_points, t)
    
    def de_casteljau_all_levels(self, points, t):
        levels = [np.array(points)]
        current_points = np.array(points)
        
        while len(current_points) > 1:
            new_points = []
            for i in range(len(current_points) - 1):
                new_point = (1 - t) * current_points[i] + t * current_points[i + 1]
                new_points.append(new_point)
            current_points = np.array(new_points)
            levels.append(current_points)
        
        return levels
    
    def evaluate_curve(self, num_points=200):
        if len(self.points) < 2:
            return self.points
            
        t_values = np.linspace(0, 1, num_points)
        curve_points = []
        
        for t in t_values:
            point = self.de_casteljau(self.points, t)
            curve_points.append(point)
        
        return np.array(curve_points)