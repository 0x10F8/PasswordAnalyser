def clean_input(input_text):
    return input_text.replace("\n", "").replace("\r", "")

def count_lines(input_file):
    with open(input_file, 'r', 1024, encoding="utf8", errors="ignore") as open_file:
        count = 0
        while True:
            if open_file.readline():
                count += 1
            else:
                break
        return count