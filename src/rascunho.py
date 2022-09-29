def chunks_from_file(self, chunksize=8192):
    """ Read file chunks. """
    file_chunks = []
    with open(self, "rb") as f_file:
        while True:
            chunk = f_file.read(chunksize)
            if chunk:
                yield chunk
                file_chunks.append(chunk)
            else:
                break
    return file_chunks
