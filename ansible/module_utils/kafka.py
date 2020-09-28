

def kafkawrapper(function):
    def wrapper(*args, **kwargs):
        result = {"changed": False, "rc": 0}
        result.update(function(*args, **kwargs))
        return result
    return wrapper
