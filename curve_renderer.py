import matplotlib.patches as patches
from bezier_curve import BezierCurve


class CurveRenderer:
    
    def __init__(self, ax, title):
        self.ax = ax
        self.title = title
        self.setup_axes()
    
    def setup_axes(self):
        self.ax.set_title(self.title, fontsize=14, fontweight='bold')
        self.ax.set_xlim(0, 6)
        self.ax.set_ylim(0, 5)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
    
    def render_curve(self, curve):
        self.clear_curve(curve)
        
        curve.control_line, = self.ax.plot(
            curve.points[:, 0], curve.points[:, 1], 
            'o--', color='gray', alpha=0.5, linewidth=1, markersize=4
        )
        
        if len(curve.points) >= 2:
            curve_points = curve.evaluate_curve()
            if len(curve_points) > 1:
                curve.curve_line, = self.ax.plot(
                    curve_points[:, 0], curve_points[:, 1], 
                    color=curve.color, linewidth=3
                )
                
        if curve.show_hull and len(curve.points) >= 3:
            hull_points = curve.compute_convex_hull()
            if len(hull_points) > 2:
                curve.hull_line, = self.ax.plot(
                    hull_points[:, 0], hull_points[:, 1], 
                    '--', color='red', linewidth=2, alpha=0.7, 
                    label='Convex Hull'
                )
        
        self.render_control_points(curve)

        self.ax.set_title(self.title, fontsize=14, fontweight='bold', color=curve.color)
    
    def render_control_points(self, curve):
        if isinstance(curve, BezierCurve):
            colors = ['#4ECDC4' if i in [0, len(curve.points)-1] else '#45B7D1' 
                     for i in range(len(curve.points))]
        else: 
            colors = ['#9B59B6'] * len(curve.points)
        
        for i, (point, color) in enumerate(zip(curve.points, colors)):
            circle = patches.Circle(point, 0.1, facecolor=color, edgecolor='black', 
                                  linewidth=2, zorder=10)
            self.ax.add_patch(circle)
            curve.points_patches.append(circle)
    
    def clear_curve(self, curve):
        for patch in curve.points_patches:
            patch.remove()
        curve.points_patches.clear()
        
        for line in [curve.curve_line, curve.control_line, curve.hull_line]:
            if line is not None:
                line.remove()
        
        curve.curve_line = None
        curve.control_line = None
        curve.hull_line = None