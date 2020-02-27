def check_float(nominal):
    try:
        return (float(nominal))
    except ValueError:
        return