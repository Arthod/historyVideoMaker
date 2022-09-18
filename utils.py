def lerps_linear(val_start: float, val_stop: float, count: int) -> list[float]:
    b = val_start
    a = (val_stop - b) / (count - 1)
    
    return [a * i + b for i in range(count)]

def lerps_expoential(val_start: float, val_stop: float, count: int) -> list[float]:
    b = pow(val_stop / val_start, 1 / (count - 1))
    a = val_start
    return [a * pow(b, i) for i in range(count)]