from hashlib import sha256

def encode_data(data: str) -> str:
    return sha256(data.encode()).hexdigest()