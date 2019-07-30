def print_progress(current, maximum, length):
    completed = int(float(current)/float(maximum) * float(length))
    completed_string = "#" * completed
    uncompleted_string = "." * (length - completed)
    clear_progress(length+2)
    print("[{0}{1}]".format(completed_string, uncompleted_string), end='')


def clear_progress(length):
    print("\b" * length, end='')
