import secrets

def create_room_id():
    return secrets.token_urlsafe(6)


print(create_room_id())
