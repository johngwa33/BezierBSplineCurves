import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from bezier_curve import BezierCurve
import tkinter as tk
from tkinter import simpledialog


class ButtonManager:
    def __init__(self, curve, renderer, color_manager, curve_type, animator=None):
        self.curve = curve
        self.renderer = renderer
        self.color_manager = color_manager
        self.curve_type = curve_type
        self.animator = animator
        self.color_index = 1 
        self.buttons = {}
        
    def create_buttons(self, x_offset=0.05):
        button_height = 0.035  
        button_width = 0.07   
        y_pos = 0.02
        spacing = 0.075        
        
        if self.curve_type == 'bezier':
            positions = [
                (x_offset, y_pos),
                (x_offset + spacing, y_pos),
                (x_offset + 2*spacing, y_pos),
                (x_offset + 3*spacing, y_pos),
                (x_offset + 4*spacing, y_pos),
                (x_offset + 5*spacing, y_pos)
            ]
            
            button_configs = [
                ('add', '+ Point', self.add_point),        
                ('remove', '- Point', self.remove_point),  
                ('reset', 'Reset', self.reset_curve),
                ('hull', 'Hull', self.toggle_hull),        
                ('color', 'Color ▼', self.cycle_color),    
                ('animate', 'Animate', self.toggle_animation)
            ]
        else:
            positions = [
                (x_offset, y_pos),
                (x_offset + spacing, y_pos),
                (x_offset + 2*spacing, y_pos),
                (x_offset + 3*spacing, y_pos),
                (x_offset + 4*spacing, y_pos)
            ]
            
            button_configs = [
                ('add', '+ Point', self.add_point),     
                ('remove', '- Point', self.remove_point), 
                ('reset', 'Reset', self.reset_curve),
                ('hull', 'Hull', self.toggle_hull),       
                ('color', 'Color ▼', self.cycle_color)     
            ]
            
        for i, (key, label, callback) in enumerate(button_configs):
            ax_button = plt.axes([positions[i][0], positions[i][1], button_width, button_height])
            button = Button(ax_button, label)
            button.on_clicked(callback)
            
            if key == 'color':
                button.color = self.curve.color
                button.hovercolor = self.curve.color
            
            self.buttons[key] = button
    
    def add_point(self, event):
        if self.animator and self.animator.animation_active:
            return  # Nu permite adăugarea în timpul animației

        root = tk.Tk()
        root.withdraw()

        try:
            x_input = simpledialog.askstring("X coordinate", "Enter the X value:")
            if x_input is None:
                return  

        
            y_input = simpledialog.askstring("Y coordinate", "Enter the Y value:")
            if y_input is None:
                return  
            x = float(x_input)
            y = float(y_input)

        
            new_point = np.array([[x, y]])
            self.curve.points = np.vstack([self.curve.points, new_point])

            # Reafișează curba
            self.renderer.render_curve(self.curve)
            self.renderer.ax.figure.canvas.draw()

        except ValueError:
            print("Invalid coordinates. Please enter real numbers")

    
    def remove_point(self, event):
        if self.animator and self.animator.animation_active:
            return 
        self.curve.remove_point()
        self.renderer.render_curve(self.curve)
        self.renderer.ax.figure.canvas.draw()
    
    def reset_curve(self, event):
        if self.animator and self.animator.animation_active:
            return
            
        if isinstance(self.curve, BezierCurve):
            self.curve.points = np.array([[1, 2], [2, 4], [4, 1], [5, 3]], dtype=float)
        else: 
            self.curve.points = np.array([
                [0.5, 2], [1.5, 4], [2.5, 1], [3.5, 4.5], [4.5, 2], [5.5, 3]
            ], dtype=float)
        
        self.renderer.render_curve(self.curve)
        self.renderer.ax.figure.canvas.draw()
    
    def toggle_hull(self, event):
        self.curve.show_hull = not self.curve.show_hull
        self.buttons['hull'].label.set_text('Hide Hull' if self.curve.show_hull else 'Show Hull')
        self.renderer.render_curve(self.curve)
        self.renderer.ax.figure.canvas.draw()
    
    def cycle_color(self, event):
        self.color_index, color_name, color_value = self.color_manager.get_next_color(self.color_index)
        self.curve.color = color_value

        self.buttons['color'].label.set_text(f'{color_name} ▼')
        self.buttons['color'].color = color_value
        self.buttons['color'].hovercolor = color_value
        
        self.renderer.render_curve(self.curve)
        self.renderer.ax.figure.canvas.draw()
    
    def toggle_animation(self, event):
        if not self.animator:
            return
        
        if self.animator.animation_active:
            self.animator.stop_animation()
            self.buttons['animate'].label.set_text('Animate')
            self.renderer.render_curve(self.curve)
        else:
            self.animator.start_animation()
            self.buttons['animate'].label.set_text('Stop')
        
        self.renderer.ax.figure.canvas.draw()