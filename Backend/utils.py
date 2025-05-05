import uuid 

#Purpose: This file contains utility functions for the application.
# It include a function for generating unique IDs
def create_unique_id():
    random_key = uuid.uuid4()
    genid = str(random_key)
    return genid