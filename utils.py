def map_waste_color(color):
    return [int(color == 'green'), int(color == 'yellow'), int(color == 'red')]

def next_waste_color(color):
    colors = ['green', 'yellow', 'red']
    for i, c in enumerate(colors):
        try:
            if color == c:
                return colors[i+1]
        except Exception as e:
            if e is IndexError:
                print("color is red : not next color")
