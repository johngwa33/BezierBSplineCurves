import numpy as np
import matplotlib.patches as patches
import matplotlib.animation as animation


class DeCasteljauAnimator:
    
    def __init__(self, ax, bezier_curve):
        self.ax = ax
        self.bezier_curve = bezier_curve
        self.animation_active = False
        self.animation_obj = None
        self.t_current = 0.0
        self.animation_speed = 0.02
        
        self.construction_lines = []
        self.construction_points = []
        self.trace_points = []
        self.trace_line = None
        
        self.level_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    
    def clear_animation_elements(self):
        for lines in self.construction_lines:
            for line in lines:
                if line in self.ax.lines:
                    line.remove()
        self.construction_lines.clear()
        
        for points in self.construction_points:
            for point in points:
                if point in self.ax.patches:
                    point.remove()
        self.construction_points.clear()
        
        if self.trace_line and self.trace_line in self.ax.lines:
            self.trace_line.remove()
        self.trace_line = None
        self.trace_points.clear()
    
    def draw_construction_step(self, t):
        if len(self.bezier_curve.points) < 2:
            return
        
        self.clear_animation_elements()
        
        levels = self.bezier_curve.de_casteljau_all_levels(self.bezier_curve.points, t)
        
        for level_idx, level_points in enumerate(levels[:-1]): 
            if len(level_points) < 2:
                continue
                
            level_lines = []
            level_point_patches = []
            
            color = self.level_colors[level_idx % len(self.level_colors)]
            
            for i in range(len(level_points) - 1):
                line, = self.ax.plot([level_points[i][0], level_points[i+1][0]], 
                                   [level_points[i][1], level_points[i+1][1]], 
                                   color=color, linewidth=2, alpha=0.7)
                level_lines.append(line)
            
            if level_idx > 0:
                for point in level_points:
                    circle = patches.Circle(point, 0.05, facecolor=color, 
                                          edgecolor='black', linewidth=1, 
                                          alpha=0.8, zorder=8)
                    self.ax.add_patch(circle)
                    level_point_patches.append(circle)
            
            self.construction_lines.append(level_lines)
            self.construction_points.append(level_point_patches)
        
        final_point = levels[-1][0]
        final_circle = patches.Circle(final_point, 0.08, facecolor='red', 
                                    edgecolor='black', linewidth=2, 
                                    alpha=1.0, zorder=10)
        self.ax.add_patch(final_circle)
        self.construction_points.append([final_circle])
        
        self.trace_points.append(final_point.copy())
        
        if len(self.trace_points) > 1:
            trace_array = np.array(self.trace_points)
            self.trace_line, = self.ax.plot(trace_array[:, 0], trace_array[:, 1], 
                                          color=self.bezier_curve.color, 
                                          linewidth=3, alpha=0.8)
    
    def animate_frame(self, frame):
        self.t_current = (frame * self.animation_speed) % 1.0
        self.draw_construction_step(self.t_current)
        return []
    
    def start_animation(self):
        if self.animation_active:
            return
        
        self.animation_active = True
        self.trace_points.clear()
        
        frames = int(1.0 / self.animation_speed)
        self.animation_obj = animation.FuncAnimation(
            self.ax.figure, self.animate_frame, frames=frames,
            interval=50, repeat=True, blit=False
        )
        
        self.ax.figure.canvas.draw()
    
    def stop_animation(self):
        if not self.animation_active:
            return
        
        self.animation_active = False
        
        if self.animation_obj:
            self.animation_obj.event_source.stop()
            self.animation_obj = None
        
        self.clear_animation_elements()
        self.ax.figure.canvas.draw()