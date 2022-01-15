# -*- coding: utf-8 -*-


import graph

def scd(ADT):
    selected_vertex=graph.sort_by_degree(ADT)[0]


    saturation_degrees=dict(zip(ADT.vertex(),
                              [0]*ADT.order()))


    chromatic_number_upper_bound=range(ADT.degree(selected_vertex)+1)


    color_assignments={}
    color_assignments[selected_vertex]=0


    while len(color_assignments)<ADT.order():
        saturation_degrees.pop(selected_vertex)


        for node in ADT.edge(selected_vertex):
            if node in saturation_degrees:
                saturation_degrees[node]+=1


        check_vertices_degree=[node for node in saturation_degrees if saturation_degrees[node]==max(saturation_degrees.values())]

 
        if len(check_vertices_degree)>1:
            degree_distribution=[ADT.degree(node) for node in check_vertices_degree]
            selected_vertex=check_vertices_degree[degree_distribution.index(max(degree_distribution))]
        else:
            selected_vertex=check_vertices_degree[0]

  
        excluded_colors=[color_assignments[node] for node in ADT.edge(selected_vertex) if node in color_assignments]
        selected_color=[color for color in chromatic_number_upper_bound if color not in excluded_colors][0]
        color_assignments[selected_vertex]=selected_color

    return color_assignments