import numpy as np
from scipy.spatial import ConvexHull
from abc import ABC, abstractmethod


class CurveBase(ABC):
    
    def __init__(self, initial_points, color='#45B7D1'):
        self.points = np.array(initial_points, dtype=float)
        self.color = color
        self.show_hull = False
        self.dragging = -1
        
        self.curve_line = None
        self.control_line = None
        self.points_patches = []
        self.hull_line = None
    
    @abstractmethod
    def evaluate_curve(self, num_points=200):
        pass
    
    def compute_convex_hull(self):
        if len(self.points) < 3:
            return self.points
        
        try:
            hull = ConvexHull(self.points)
            hull_points = self.points[hull.vertices]
            hull_points = np.vstack([hull_points, hull_points[0]])
            return hull_points
        except:
            return self.points
    
    def add_point(self):
        new_point = np.array([[np.random.uniform(0.5, 5.5), np.random.uniform(0.5, 4.5)]])
        self.points = np.vstack([self.points, new_point])
    
    def remove_point(self):
        if self.can_remove_point():
            self.points = self.points[:-1]
    
    def can_remove_point(self):
        return len(self.points) > 2
    
    def get_closest_point_index(self, x, y, threshold=0.2):
        distances = np.sqrt((self.points[:, 0] - x)**2 + (self.points[:, 1] - y)**2)
        closest_idx = np.argmin(distances)
        return closest_idx if distances[closest_idx] < threshold else -1
    
    def update_point(self, index, x, y):
        if 0 <= index < len(self.points):
            self.points[index] = [x, y]