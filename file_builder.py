from obj_chunker import Chunk

REVERSE_LOOKUP = {}

with open("cpp_vertex_mapping.txt", "r") as file:
    lines = file.readlines()
    
    for line in lines:
        # Example line: `VID: 234255, (-7.378388, 0.490569, 7.379428)`

        # Remove whitespace
        line = line.strip()

        # Split the line by the first comma only
        line = line.split(",", 1)

        # Extract the VID
        vid = line[0].split(": ")[1]

        # Extract the coordinates, strip surrounding spaces and parentheses
        coord_str = line[1].strip()[1:-1]  # Remove leading '(' and trailing ')'

        # Convert coord_str to a tuple of floats
        coords = tuple(float(x) for x in coord_str.split(", "))

        # Use the tuple of coordinates as the key in the dictionary
        REVERSE_LOOKUP[coords] = vid

        print(f"{coords} : {vid}")



def serialize_chunk_map_to_file(chunks : list, vertices : list, filepath : str):
    with open(filepath, "w") as file:
        for chunk in chunks:

            CENTRE_POINT_STR = str(chunk.centre_point)
            
            # Remove left and right square brackets
            CENTRE_POINT_STR = "# "+ CENTRE_POINT_STR[1:-1]

            file.write(CENTRE_POINT_STR + "\n")

            for face in chunk.faces:
                
                reindexed_face = []

                # Every face is an array of 3 vertices
                
                for vert,idx in zip(face, range(3)):
                    tuple_3_vertex_str = vertices[vert]
                    
                    VID = REVERSE_LOOKUP[tuple_3_vertex_str]

                    reindexed_face.append(int(VID))

                FACE_STR = str(reindexed_face)

                # Remove left and right square brackets
                FACE_STR = FACE_STR[1:-1]

                file.write(FACE_STR + "\n")




def generate_prefixed_zeros_str(num_zeros: int, num: int):
    num_str = str(num)
    num_zeros_str = "0" * (num_zeros - len(num_str))
    return num_zeros_str + num_str

# Triangles is a List of List of 3 vertices (each vertex is a tuple of 3 floats)

def build_full_chunk_map(chunks: list, filepath: str):
    # Set to keep track of unique triangle strings
    unique_triangles = set()

    with open(filepath, "w") as file:

        for chunk in chunks:
            CENTRE_POINT_STR = str(chunk.centre_point)
            
            # Remove left and right square brackets
            CENTRE_POINT_STR = "# " + CENTRE_POINT_STR[1:-1]
            file.write(CENTRE_POINT_STR + "\n")

            for triangle in chunk.triangles:
                TRIANGLE_STR = str(triangle)
                TRIANGLE_STR = TRIANGLE_STR[1:-1]

                # Append the triangle string only if it's unique
                if TRIANGLE_STR not in unique_triangles:
                    file.write(TRIANGLE_STR + "\n")
                    unique_triangles.add(TRIANGLE_STR)


def build_chunk_map_into_many_files(chunks: list, filepath: str):
    # Set to keep track of unique triangle strings

    unique_triangles = set()
    
    max_n_chunks_per_file = 15

    for idx, chunk in enumerate(chunks):
        file_idx = divmod(idx, max_n_chunks_per_file)[0]

        filename = filepath + '_' + generate_prefixed_zeros_str(4, file_idx) + ".txt"

        with open(filename, "a") as file:
            CENTRE_POINT_STR = str(chunk.centre_point)
            
            # Remove left and right square brackets
            CENTRE_POINT_STR = "# " + CENTRE_POINT_STR[1:-1]
            file.write(CENTRE_POINT_STR + "\n")

            for triangle in chunk.triangles:
                TRIANGLE_STR = str(triangle)
                TRIANGLE_STR = TRIANGLE_STR[1:-1]

                # Append the triangle string only if it's unique
                if TRIANGLE_STR not in unique_triangles:
                    file.write(TRIANGLE_STR + "\n")
                    unique_triangles.add(TRIANGLE_STR)

def reindex_lookup():
    pass