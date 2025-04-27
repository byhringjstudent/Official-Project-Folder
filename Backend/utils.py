import uuid 

def create_unique_id():
    random_key = uuid.uuid4()
    genid = str(random_key)
    return genid