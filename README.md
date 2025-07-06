# BezierBSplineCurves

# Interactive Bézier and B-Spline Curves Visualization
![image](https://github.com/user-attachments/assets/b60942fe-28bb-467e-8849-d6fa41823faa)

An interactive Python application that demonstrates Bézier curves and B-Splines with real-time manipulation, animation, and visualization of the De Casteljau algorithm.

## Features

- **Dual Curve Visualization**: Simultaneous display of Bézier curves and B-Splines
- **Interactive Controls**:
  - Drag points to modify curves in real-time
  - Add/remove control points
  - Toggle convex hull display
  - Change curve colors
  - Reset to default configurations
- **Bézier Curve Animation**: Visualize the De Casteljau algorithm construction process
- **Advanced Interaction**:
  - Pan with right-click drag
  - Zoom with mouse scroll
  - Precise point placement via coordinate input

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/johngwa33/BezierBSplineCurves.git
   cd BezierBSplineCurves

2. Install required dependencies:

   ```bash
   pip install numpy matplotlib scipy
3. Run the application:

   ```bash
   python main.py

## Technical Details

### Core Classes Overview

#### `InteractiveCurves` (Inside main.py)
**Purpose**: Manages the entire application workflow and user interactions  
**Key Features**:
- Creates dual-plot layout (Bézier left, B-Spline right)
- Handles mouse events (dragging, panning, zooming)
- Coordinates between curve objects and renderers  
**Dependencies**: All other classes in the project

---

### Curve Base Classes

#### `CurveBase` (Abstract Base Class)
**Purpose**: Provides common functionality for both curve types  
**Key Features**:
- Implements control point management (add/remove/drag)
- Computes convex hulls using SciPy
- Maintains visualization state (color, hull visibility)  
**Inherited By**: `BezierCurve`, `BSplineCurve`

#### `BezierCurve`
**Purpose**: Implements Bézier curve mathematics  
**Key Algorithms**:
- De Casteljau's algorithm (recursive and full-levels variants)  
**Special Behavior**:
- Colors endpoints differently from control points
- Requires minimum 2 points for rendering

#### `BSplineCurve`
**Purpose**: Implements B-Spline mathematics  
**Key Algorithms**:
- Basis function calculation (recursive Cox-de Boor)
- Non-uniform knot vector generation  
**Special Behavior**:
- Requires `degree + 1` points to render
- Uses uniform purple coloring for all points

---

### Visualization Classes

#### `CurveRenderer`
**Purpose**: Handles all curve visualization aspects  
**Key Features**:
- Manages Matplotlib artists (lines, points, hulls)
- Implements consistent styling for both curve types
- Maintains aspect ratio and grid visibility

#### `DeCasteljauAnimator`
**Purpose**: Visualizes the Bézier construction process  
**Key Features**:
- Animated intermediate lines and points
- Color-coded construction levels
- Real-time trace of the curve being built  
**Animation Control**:
- Adjustable speed via `animation_speed`
- Smooth interpolation between frames

---

### UI Components

#### `ButtonManager`
**Purpose**: Creates and manages interactive controls  
**Key Features**:
- Dynamically generates curve-specific buttons
- Handles Tkinter dialogs for point coordinates
- Manages button states during animation  
**UI Patterns**:
- Toggle buttons (Hull/Animate)
- Cycling buttons (Colors)
- Action buttons (Add/Remove/Reset)

#### `ColorManager`
**Purpose**: Maintains consistent color schemes  
**Color Palette**:
- 6 predefined aesthetically-matched colors
- Cycling system with name display  
**Usage**:
- Called when users click color buttons
- Updates both curve and button colors
