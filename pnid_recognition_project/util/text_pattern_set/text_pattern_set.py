import re
import json

class TextPatternsSet:
    def __init__(self, special_chars, max_window):
        self.max_window = max_window
        self.patterns = {}
        for char in special_chars:
            self.patterns[char] = set()

    def update(self, char, line, ignore_newline=True, strip=True):
        if ignore_newline and '\n' in line:
            return

        char_index = line.find(char)
        start_ind = max(char_index-self.max_window, 0)
        end_ind = min(char_index+self.max_window, len(line))

        line_window = line[start_ind:end_ind]
        line_window = re.sub(r'[a-z]', 'c', line_window)
        line_window = re.sub(r'[A-Z]', 'C', line_window)
        line_window = re.sub(r'[0-9]', 'n', line_window)
        if strip:
            line_window = line_window.strip()

        self.patterns[char].update([line_window])

    def dump_json(self, path):
        dump_obj = {}
        for char in self.patterns:
            dump_obj[char] = list(self.patterns[char])

        with open(path, 'w') as f:
            json.dump(dump_obj, f, indent=4)