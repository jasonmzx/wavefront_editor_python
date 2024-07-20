import pywavefront
import numpy as np

class Chunk:
    def __init__(self, faces, triangles, centre_point=[None, None, None]):
        #self.vertices = vertices
        self.faces = faces
        self.triangles = triangles
        self.centre_point = centre_point

    def __str__(self):
        return "Faces: " + str(self.faces) + "\nCentre Point: " + str(self.centre_point)



def get_monolithic_mesh(filepath: str):
# This function doesn't chunk, it just loads and returns vertices and faces

    scene = pywavefront.Wavefront(filepath, collect_faces=True)

    verts = scene.vertices
    faces = scene.mesh_list[0].faces

    for face_grp in scene.mesh_list[1:]:        
        faces.extend(face_grp.faces)


    for face in faces:
        print(face)
    
        # Print first 10 faces
    for face in faces[:10]:
        print("Face Vertices: ", verts[face[0]], verts[face[1]], verts[face[2]])
    
    # print first 10 vertices
    for vert in verts[:10]:
        print("Vertex: ", vert)

    print("Number of Vertices: ", len(verts))

    return verts, faces    


# ------------------- Chunking & It's Helpers -------------------


def get_XZ_chunked_mesh(filepath: str, N_CHUNKS: int):

    verts, faces = get_monolithic_mesh(filepath)

    chunks = [] # List of Chunk objects

    #* Sorting by X then Z assures rendering consistency, just X is still a mess

    sorted_faces_by_x = sorted(faces, key=lambda face: verts[face[0]][0]) # Sort faces by their X values
    sorted_faces_by_xz = sorted(sorted_faces_by_x, key=lambda face: verts[face[0]][2]) # Sort faces by their Z values

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

    Z_chunk_midpoints = []

    for i in range(len(chunk_boundaries_Z)-1):
        Z_chunks_face_subsets.append([])
        Z_chunk_midpoints.append(None)


    for face in sorted_faces_by_xz:
        # Get Face vertices
        v0 = verts[face[0]] # Vertex 1

        # Parition faces into correct Z chunks
        for i in range(len(chunk_boundaries_Z)-1):
            if v0[2] > chunk_boundaries_Z[i] and v0[2] < chunk_boundaries_Z[i+1]: # Lower < v0 < Upper
                
                # TODO: if this is slow, find a way to not reset midpoint for every face
                Z_chunk_midpoints[i] = (chunk_boundaries_Z[i] + chunk_boundaries_Z[i+1]) / 2 

                Z_chunks_face_subsets[i].append(face)
                break
    
    #print("Z Chunk Midpoints: ", Z_chunk_midpoints)

    # *------------- X Partitioning over Z -------------

    for i in range(len(Z_chunks_face_subsets)):
        
        faces_subset = Z_chunks_face_subsets[i]

        if len(faces_subset) == 0:
            continue

        Z_midpoint = Z_chunk_midpoints[i]

        x_chunks_face_lists = []

        x_chunks_triangles = []

        X_chunks_midpoints = []

        # Initialize lists to store faces for each chunk

        for i in range(len(chunk_boundaries_X)-1):
            
            x_chunks_face_lists.append([])
            x_chunks_triangles.append([])

            X_chunks_midpoints.append(None)

        for face in faces_subset:

            # Get Face vertices
            v0 = verts[face[0]]
            # Match v0 to a range and put it into appropriate chunk

            for i in range(len(chunk_boundaries_X)-1):
                
                if v0[0] > chunk_boundaries_X[i] and v0[0] < chunk_boundaries_X[i+1]:  # Lower < v0 < Upper

                    #TODO: if this is slow, find a way to not reset midpoint for every face
                    X_chunks_midpoints[i] = (chunk_boundaries_X[i] + chunk_boundaries_X[i+1]) / 2

                    x_chunks_face_lists[i].append(face)
                    x_chunks_triangles[i].append( (verts[face[0]], verts[face[1]], verts[face[2]]) )
                    
                    break


        for XZ_chunk_subset, XZ_chunk_triangles, X_midpoint in zip(x_chunks_face_lists, x_chunks_triangles, X_chunks_midpoints):
            if len(XZ_chunk_subset) == 0:
                continue
                
            centre_point = [X_midpoint, 0, Z_midpoint] # Z Midpoint per iteration is pre-determined by Z partitioning

            chunk = Chunk(XZ_chunk_subset, XZ_chunk_triangles, centre_point)
            chunks.append(chunk)

    return chunks, verts