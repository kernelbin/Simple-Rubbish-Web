def md5_with_salt(text: str, salt: str)->str:
    import hashlib
    md5 = hashlib.md5()
    md5.update((text+salt).encode())
    return md5.hexdigest()


def encode_json(obj):
    import json
    encoder = json.JSONEncoder()
    return encoder.encode(obj)


def decode_json(obj):
    import json
    decoder = json.JSONDecoder()
    return decoder.decode(obj)


def make_response(code, **data):
    return encode_json(dict(**{
        "code": code
    }, **data))
