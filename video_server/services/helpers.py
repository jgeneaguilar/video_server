def to_int(value, default_value):
    value = value or default_value
    try:
        return int(value)
    except ValueError:
        return default_value
