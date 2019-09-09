
def validate(d:dict, name:str, type_func, default, validate_func):
    try:
        x = type_func(d.get(name, default))
        result = validate_func(x, default)
    except:
        result = default
    return result

