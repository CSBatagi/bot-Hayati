
def ll_to_bool(liste):
    for i, s in enumerate(liste):
        if not s or s[0] == 'FALSE' :
            liste[i] = False
        elif s[0] == 'TRUE':
            liste[i] = True
