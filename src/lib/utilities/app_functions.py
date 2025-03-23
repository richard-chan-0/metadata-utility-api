from warnings import warn


def deprecate_function():
    warn("This function is deprecated", DeprecationWarning, stacklevel=2)


def read_dict(dict_path: str, dict_obj: dict):
    keys = dict_path.split(".")
    for key in keys:
        if not isinstance(dict_obj, dict):
            return

        value = dict_obj.get(key)
        if not value:
            return
        dict_obj = value

    return value
