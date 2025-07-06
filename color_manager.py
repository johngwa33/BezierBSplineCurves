class ColorManager:
    def __init__(self):
        self.color_options = {
            'Red': "#DB0505",
            'Blue': '#45B7D1',
            'Green': "#29D50E",
            'Purple': '#9B59B6',
            'Orange': '#FF8C42',
            'Teal': '#26A69A'
        }
        self.color_names = list(self.color_options.keys())
    
    def get_next_color(self, current_index):
        next_index = (current_index + 1) % len(self.color_names)
        color_name = self.color_names[next_index]
        color_value = self.color_options[color_name]
        return next_index, color_name, color_value