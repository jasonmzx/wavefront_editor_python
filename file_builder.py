from obj_chunker import Chunk

def serialize_chunk_map_to_file(chunks : list, filepath : str):
    with open(filepath, "w") as file:
        for chunk in chunks:
            file.write(str(chunk.centre_point) + "\n")
            for face in chunk.faces:
                file.write(str(face) + "\n")
