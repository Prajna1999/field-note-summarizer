from fastapi import UploadFile
def read_capped(file: UploadFile,limit :int)->bytes:

    chunks=[]
    total_byte_length=0

    while chunk:=file.file.read(1024 * 1024):
        total_byte_length+=len(chunk)

        if total_byte_length>limit:
            raise ValueError(f"File exceeds limit {limit} byte limit.")
        chunks.append(chunk)

    return b"".join(chunks)

