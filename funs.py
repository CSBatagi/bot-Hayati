
def format_matrix(m):
    names, steamids, join_list, not_join_list = ([] for i in range(4))
    for i, s in enumerate(m):
        names.append(s[0])
        steamids.append(s[1])
        if len(s) > 3 and s[3] == "TRUE":
            not_join_list.append(True)
            join_list.append(False)
        elif len(s) > 2 and s[2] == "TRUE":
            join_list.append(True)
            not_join_list.append(False)
        else:
            join_list.append(False)
            not_join_list.append(False)

    return names, steamids, join_list, not_join_list 
             
