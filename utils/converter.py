def sec_2_min(time_in_seconds: int) -> tuple[int, int]:
    minutes, seconds = 0, 0
    
    if time_in_seconds >= 60:
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
    else:
        seconds = time_in_seconds
    
    return minutes, seconds