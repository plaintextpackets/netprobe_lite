# Input validation functions

from uuid import UUID

def is_uuid_4(uuid, version=4):
    
    try:
        uuid_obj = UUID(uuid, version=version)
    except ValueError:
        return False
    return True