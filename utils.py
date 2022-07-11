

# converts a time string in the form of HH:MM into a time integer as minutes since midnight
def timeStringToTime(timeString):
    hours = int(timeString.split(":")[0])
    minutes = int(timeString.split(":")[1])

    return minutes + hours * 60

# converts a time integer as minutes since midnight into a time string in the form of HH:MM
def timeToTimeString(time):
    hours = int(time / 60)
    minutes = time % 60

    hourString = f"{hours}" if hours >= 10 else f"0{hours}"
    minuteString = f"{minutes}" if minutes >= 10 else f"0{minutes}"

    return f"{hourString}:{minuteString}"
