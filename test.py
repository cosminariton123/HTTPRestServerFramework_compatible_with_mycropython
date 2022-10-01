import re

def sub():
    path = "/Coco/{cate}/mere/{cate}/porno"
    pattern = re.compile("{[^{}]*}")
    path = re.sub(pattern, "GIGI", path)

    print(path)


def regex_escape(string):
    regex_special_chars_map = {chr(i): '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}
    aux = ""
    for ch in string:
        if ch in regex_special_chars_map:
            aux += regex_special_chars_map[ch]
        else:
            aux += ch
    return aux

def match_path(pattern_path, path):
    pattern_path = regex_escape(pattern_path)  
    pattern = re.compile("\\\{[^{}]*}")
    uncompiled_pattern_string = re.sub(pattern, ".*", pattern_path)
    pattern = re.compile(uncompiled_pattern_string)

    return pattern.match(path)


def compute_ordered_list_of_keywords(path):
    pattern = re.compile("{[^{}]*}")
    ordered_list_of_keywords = list()
    current_key = pattern.search(path)
    if current_key is not None:
        ordered_list_of_keywords.append(current_key.group(0)[1:-1])
    slice = path
    while current_key is not None:
        slice = slice[current_key.end():]
        current_key = pattern.search(slice)
        if current_key is not None:
            ordered_list_of_keywords.append(current_key.group(0)[1:-1])
    return ordered_list_of_keywords


def compute_ordered_lists_of_keywords_starts_and_ends(path):
    pattern = re.compile("{[^{}]*}")
    offset = 0
    ordered_list_of_keywords_starts = list()
    ordered_list_of_keywords_ends = list()
    current_key = pattern.search(path)
    if current_key is not None:
        ordered_list_of_keywords_starts.append(current_key.start())
        ordered_list_of_keywords_ends.append(current_key.end())
        offset = current_key.end()
    while current_key is not None:
        slice = path[offset:]
        current_key = pattern.search(slice)
        if current_key is not None:
            ordered_list_of_keywords_starts.append(current_key.start() + offset)
            ordered_list_of_keywords_ends.append(current_key.end() + offset)
            offset+= current_key.end()
    return ordered_list_of_keywords_starts, ordered_list_of_keywords_ends



def compute_ordered_list_of_values(path, stored_path):
    ordered_list_of_keywords_starts, ordered_list_of_keywords_ends = compute_ordered_lists_of_keywords_starts_and_ends(stored_path)

    idx_path = ordered_list_of_keywords_starts[0]
    ordered_list_of_values = list()
    slice = path
    for (idx_s, keyword_start), keyword_end in zip(enumerate(ordered_list_of_keywords_starts), ordered_list_of_keywords_ends):
        value = ""
        last_slice = slice
        while match_path(stored_path[keyword_start:], slice) is not None and last_slice != "":
            if idx_path < len(path):
                value += path[idx_path]
            idx_path += 1
            last_slice = slice
            slice = path[idx_path:]
        if idx_path < len(path):
            value = value[:-1]
        ordered_list_of_values.append(value)
        
        if idx_s + 1 < len(ordered_list_of_keywords_starts):
            if len(value) > 0:
                idx_path += ordered_list_of_keywords_starts[idx_s + 1] - keyword_end - 1
            else:
                idx_path += ordered_list_of_keywords_starts[idx_s + 1] - keyword_end
    return ordered_list_of_values


def compute_path_variables(path, stored_path):
    ordered_list_of_keywords = compute_ordered_list_of_keywords(stored_path)
    ordered_list_of_values = compute_ordered_list_of_values(path, stored_path)
    path_variables = dict()
    for key, value in zip(ordered_list_of_keywords, ordered_list_of_values):
        path_variables[key] = value
    return path_variables


def _reverse_string(string):
    stack = list()
    for elem in string:
        stack.append(elem)
    string = ""
    while stack:
        string += stack.pop()
    return string

def _compute_path_without_request_param_string(path):
        path = _reverse_string(path)
        path = path.split("?", 1)[0]
        path = _reverse_string(path)
        return path


def _compute_request_param_string(path):
        path = _reverse_string(path)
        path = path.split("?", 1)[1]
        path = _reverse_string(path)
        return path




def main():
    import sys
    if sys.implementation.name == "micropython":
	    print("Coco")

if __name__ == "__main__":
    
    main()