from hashlib import md5


def get_md5(origin):
    m = md5(origin.encode('utf-8'))
    return m.hexdigest()
