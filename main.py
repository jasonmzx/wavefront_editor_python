import pyvista as pv
import numpy as np
import random

# Source Imports
import obj_chunker

def random_color():
    return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def load_chunks_into_pv(chunks, verts):
    
    plotter = pv.Plotter() #Init plotter
    plotter.title = "XZ Chunked Mesh"
    vertices_array = np.array(verts)
    
    for chunk in chunks:

        faces_np = np.empty((len(chunk.faces), 4), dtype=np.int64)
        faces_np[:, 0] = 3 # number of vertices in each face (COL 1)
        faces_np[:, 1:] = chunk.faces

        poly_data = pv.PolyData(vertices_array, faces_np)

        plotter.add_mesh(poly_data, show_edges=True, color=random_color())

        plotter.add_point_labels((0,0.5,0), [str("1")], font_size=24, point_size=10, name="center_text")

    plotter.show()


chunks, verts = obj_chunker.get_XZ_chunked_mesh("objects/OZ.obj", 5)

load_chunks_into_pv(chunks, verts)


# Monotilhic Mesh

# verts, faces = obj_chunker.get_monolithic_mesh("objects/XZ.obj")

# vertices_array = np.array(verts)

# faces_np = np.empty((len(faces), 4), dtype=np.int64)
# faces_np[:, 0] = 3 # number of vertices in each face (COL 1)
# faces_np[:, 1:] = faces

# plotter = pv.Plotter() #Init plotter

# poly_data = pv.PolyData(vertices_array, faces_np)

# plotter.add_mesh(poly_data, show_edges=True, color="red")

# #plotter.add_text("Center", position=(0,0), font_size=24, color="blue", font="arial", shadow=True, name="center_text")

# plotter.show()