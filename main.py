import matplotlib.pyplot as plt
from bezier_curve import BezierCurve
from bspline_curve import BSplineCurve
from curve_renderer import CurveRenderer
from decasteljau_animator import DeCasteljauAnimator
from color_manager import ColorManager
from button_manager import ButtonManager

class InteractiveCurves:

    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(20, 8))
        self.fig.suptitle('Animated Bézier Curves and B-Spline')
         
        self.bezier_curve = BezierCurve()
        self.bspline_curve = BSplineCurve()

        self.bezier_renderer = CurveRenderer(self.ax1, 'Bézier')
        self.bspline_renderer = CurveRenderer(self.ax2, 'B-Spline')
        
        self.bezier_animator = DeCasteljauAnimator(self.ax1, self.bezier_curve)
        
        self.color_manager = ColorManager()
        
        self.bezier_buttons = ButtonManager(self.bezier_curve, self.bezier_renderer, 
                                          self.color_manager, 'bezier', self.bezier_animator)
        self.bspline_buttons = ButtonManager(self.bspline_curve, self.bspline_renderer, 
                                           self.color_manager, 'bspline')
        
        self.setup_ui()
        self.connect_events()
        self.update_all()
        
        self.pan_start = None
        self.pan_ax = None
        
        self.zoom_factor = 1.1 
        self.max_zoom_in = 0.1 
        self.max_zoom_out = 20 
        
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
    
    def setup_ui(self):
        self.bezier_buttons.create_buttons(x_offset=0.05)
        self.bspline_buttons.create_buttons(x_offset=0.55)
    
    def connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press_pan)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release_pan)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion_pan)
        
    def on_press_pan(self, event):
        if event.button == 3:  
            self.pan_start = (event.x, event.y)
            self.pan_ax = event.inaxes
    
    def on_motion_pan(self, event):
        if self.pan_start is None or self.pan_ax is None:
            return
        
        dx = event.x - self.pan_start[0]
        dy = event.y - self.pan_start[1]
        
        xlim = self.pan_ax.get_xlim()
        ylim = self.pan_ax.get_ylim()
        fig_size = self.fig.get_size_inches()*self.fig.dpi
        dx_data = dx/fig_size[0] * (xlim[1]-xlim[0])
        dy_data = dy/fig_size[1] * (ylim[1]-ylim[0])
        
        self.pan_ax.set_xlim(xlim[0]-dx_data, xlim[1]-dx_data)
        self.pan_ax.set_ylim(ylim[0]-dy_data, ylim[1]-dy_data)
        self.fig.canvas.draw_idle()

    def on_release_pan(self, event):
        self.pan_start = None
        self.pan_ax = None
        
    def on_press(self, event):
        if self.bezier_animator.animation_active:
            return
            
        if event.inaxes == self.ax1:
            self.bezier_curve.dragging = self.bezier_curve.get_closest_point_index(
                event.xdata, event.ydata)
        elif event.inaxes == self.ax2:
            self.bspline_curve.dragging = self.bspline_curve.get_closest_point_index(
                event.xdata, event.ydata)
    
    def on_release(self, event):
        self.bezier_curve.dragging = -1
        self.bspline_curve.dragging = -1
    
    def on_motion(self, event):
        if event.inaxes is None:
            return
        
        if self.bezier_animator.animation_active:
            return
        
        if self.bezier_curve.dragging >= 0 and event.inaxes == self.ax1:
            self.bezier_curve.update_point(self.bezier_curve.dragging, event.xdata, event.ydata)
            self.bezier_renderer.render_curve(self.bezier_curve)
            self.ax1.figure.canvas.draw_idle()
            
        elif self.bspline_curve.dragging >= 0 and event.inaxes == self.ax2:
            self.bspline_curve.update_point(self.bspline_curve.dragging, event.xdata, event.ydata)
            self.bspline_renderer.render_curve(self.bspline_curve)
            self.ax2.figure.canvas.draw_idle()
    
    def on_scroll(self, event):
        if event.inaxes not in [self.ax1, self.ax2]:
            return
        
        ax = event.inaxes
        x, y = event.xdata, event.ydata
        
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        if event.button == 'up':
            zoom = 1/self.zoom_factor  
        elif event.button == 'down':
            zoom = self.zoom_factor   
        else:
            return
        
        new_x_width = (xlim[1] - xlim[0]) * zoom
        new_y_height = (ylim[1] - ylim[0]) * zoom
        
        if (new_x_width < self.max_zoom_in or 
            new_x_width > self.max_zoom_out or
            new_y_height < self.max_zoom_in or
            new_y_height > self.max_zoom_out):
            return
        
        ax.set_xlim([
            x - (x - xlim[0]) * zoom,
            x + (xlim[1] - x) * zoom
        ])
        ax.set_ylim([
            y - (y - ylim[0]) * zoom,
            y + (ylim[1] - y) * zoom
        ])
        
        self.fig.canvas.draw_idle()
        
    def update_all(self):
        self.bezier_renderer.render_curve(self.bezier_curve)
        self.bspline_renderer.render_curve(self.bspline_curve)
    
    def show(self):
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.tight_layout()
        plt.show()


def main():
    
    curves = InteractiveCurves()
    curves.show()


if __name__ == "__main__":
    main()