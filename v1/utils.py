from . import Objects

def get_user(id:str):
    for i in Objects.entities.User._instances:
        if i.id == id:
            return i
    return Objects.entities.User(id)

def get_channel(id:str):
    for i in Objects.entities.Channel._instances:
        if i.id == id:
            return i
    return Objects.entities.Channel(id)