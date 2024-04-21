import pywavefront
import numpy as np

class Chunk:
    def __init__(self, faces):
        #self.vertices = vertices
        self.faces = faces
        self.centre_point = [None, None, None]

    def __str__(self):
        return "Faces: " + str(self.faces) + "\nCentre Point: " + str(self.centre_point)



def get_monolithic_mesh(filepath: str):
# This function doesn't chunk, it just loads and returns vertices and faces

    scene = pywavefront.Wavefront(filepath, collect_faces=True)

    verts = scene.vertices
    faces = scene.mesh_list[0].faces

    return verts, faces    


# ------------------- Chunking & It's Helpers -------------------


def get_XZ_chunked_mesh(filepath: str, N_CHUNKS: int):

    verts, faces = get_monolithic_mesh(filepath)

    chunks = [] # List of Chunk objects

    # Sorting by X then Z assures rendering consistency, just X is still a mess

    sorted_faces_by_x = sorted(faces, key=lambda face: verts[face[0]][0]) # X sort
    sorted_faces_rows = sorted(sorted_faces_by_x, key=lambda face: verts[face[0]][2]) # Z sort

    # Find X and Z Dimensions of the model

    x_min = min(verts, key=lambda x: x[0])[0]
    x_max = max(verts, key=lambda x: x[0])[0]

    z_min = min(verts, key=lambda x: x[2])[2]
    z_max = max(verts, key=lambda x: x[2])[2]

    print("X Min: ", x_min)
    print("X Max: ", x_max)

    dim_x = x_max - x_min # -ve to +ve range of X
    chunk_size = dim_x / N_CHUNKS # Size of chunk (normalized to obj)


    LOW_BOUND_OFFSET = 0.00000000002

    # X Chunk Boundaries

    chunk_boundaries_X = [(x_min-LOW_BOUND_OFFSET)]

    while(True):
        chunk_boundaries_X.append(chunk_boundaries_X[-1] + chunk_size)
        if chunk_boundaries_X[-1] >= x_max:
            break

    # Z Chunk Boundaries

    chunk_boundaries_Z = [(z_min-LOW_BOUND_OFFSET)]

    while(True):
        chunk_boundaries_Z.append(chunk_boundaries_Z[-1] + chunk_size)
        if chunk_boundaries_Z[-1] >= z_max:
            break

    # *------------- Z Partitioning -------------

    Z_chunks_face_subsets = []

    for i in range(len(chunk_boundaries_Z)-1):
        Z_chunks_face_subsets.append([])


    for face in sorted_faces_rows:
        # Get Face vertices
        v0 = verts[face[0]] # Vertex 1

        # Parition faces into correct Z chunks
        for i in range(len(chunk_boundaries_Z)-1):
            if v0[2] > chunk_boundaries_Z[i] and v0[2] < chunk_boundaries_Z[i+1]:
                Z_chunks_face_subsets[i].append(face)
                break
    
    # *------------- X Partitioning over Z -------------

    for faces_subset in Z_chunks_face_subsets:
        if len(faces_subset) == 0:
            continue

        x_chunks_face_lists = []

        # Initialize lists to store faces for each chunk

        for i in range(len(chunk_boundaries_X)-1):
            x_chunks_face_lists.append([])

        for face in faces_subset:

            # Get Face vertices
            v0 = verts[face[0]]
            # Match v0 to a range and put it into appropriate chunk

            for i in range(len(chunk_boundaries_X)-1):
                if v0[0] > chunk_boundaries_X[i] and v0[0] < chunk_boundaries_X[i+1]: # Is In between
                    x_chunks_face_lists[i].append(face)
                    break

        for XZ_chunk_subset in x_chunks_face_lists:
            
            if len(XZ_chunk_subset) == 0:
                continue

            chunk = Chunk(XZ_chunk_subset)
            chunks.append(chunk)

    return chunks, verts