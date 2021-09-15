
def string_to_bool(liste):
    for i, s in enumerate(liste):
        if s == 'FALSE':
            liste[i] = False
        elif s == 'TRUE':
            liste[i] = True
