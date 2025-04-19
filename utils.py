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


# Aller en direction de la target sans sratégie 

def choose_move_to_target(target, pos, posible_steps):
    t1, t2 = target[0], target[1]
    a1, a2 = pos[0], pos[1]
    if a1<t1:
        if (a1+1, a2) in posible_steps:
            return "left"
    if a2<t2:
        if (a1, a2+1) in posible_steps:
            return "up" 
    if a1>t1:
        if (a1-1, a2) in posible_steps:
            return "right"
    if a2>t2:
        if (a1, a2-1) in posible_steps:
            return "down"
    else :
        return 'stay'

