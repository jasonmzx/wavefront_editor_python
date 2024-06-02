import pyvista as pv
import numpy as np
import random

# Source Imports
import obj_chunker
import file_builder

def random_color():
    return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def load_chunks_into_pv(chunks, verts):
    
    plotter = pv.Plotter() #Init plotter
    plotter.title = "XZ Chunked Mesh"
    vertices_array = np.array(verts)
    
    bunched_midpoints = []
    bunched_titles = []

    for chunk in chunks:

        # Debug Chunk Centrepoint printing
        print("Chunk Centrepoint: ", chunk.centre_point)
        
        # Convert chunk.centre_point which is a list of 3 floats to a tuple of 3 floats
        # This is because pyvista requires a tuple of 3 floats for the centre_point argument

        chunk.centre_point[1] = 2 # Set Y to 2 for testing

        bunched_midpoints.append(tuple(chunk.centre_point))
        
        
        # Construction of string of chunk.centre_points that have a precision limit on all floats for display
        reduced_floats_vec3_str = [f"{x:.2f}" for x in chunk.centre_point]
        display = "XZ: " + reduced_floats_vec3_str[0] + ", " + reduced_floats_vec3_str[2]

        bunched_titles.append(display)


        faces_np = np.empty((len(chunk.faces), 4), dtype=np.int64)
        faces_np[:, 0] = 3 # number of vertices in each face (COL 1)
        faces_np[:, 1:] = chunk.faces

        poly_data = pv.PolyData(vertices_array, faces_np)

        plotter.add_mesh(poly_data, show_edges=True, color=random_color())

    plotter.add_point_labels(bunched_midpoints, bunched_titles, font_size=24, point_size=10, name="center_text")

    plotter.show()


chunks, verts = obj_chunker.get_XZ_chunked_mesh("objects/DE_AZTEC.obj", 5)

# file_builder.serialize_chunk_map_to_file(chunks, verts, "chunk_map.txt")

load_chunks_into_pv(chunks, verts)

for chunk in chunks:
    print('\n')
    print("Centre Point: ", chunk.centre_point)
    print("N# Faces: ", len(chunk.faces))
    print("N# Triangles: ", len(chunk.triangles))

file_builder.build_full_chunk_map(chunks, "full_chunk_map.txt")

#* -- Monotilhic Mesh (No Chunks at all) 

# verts, faces = obj_chunker.get_monolithic_mesh("objects/Landscape01.obj")

# vertices_array = np.array(verts)

# faces_np = np.empty((len(faces), 4), dtype=np.int64)
# faces_np[:, 0] = 3 # number of vertices in each face (COL 1)
# faces_np[:, 1:] = faces

# plotter = pv.Plotter() #Init plotter

# poly_data = pv.PolyData(vertices_array, faces_np)

# plotter.add_mesh(poly_data, show_edges=True, color="red")

# #plotter.add_text("Center", position=(0,0), font_size=24, color="blue", font="arial", shadow=True, name="center_text")

# plotter.show()