from my_framework.my_http.http_constants.http_methods import HTTP_METHODS_AS_LIST
import re


class BaseController():
    def __init__(self, base_path=""):
        self.methods_list = self._get_methods_list()

        self.methods_dict = dict()
        for method in self.methods_list:
            self.methods_dict[method] = base_path
        
        self._validate_http_methods_notation()


    def _get_methods_list(self):
        pattern = re.compile("^__.*__$")
        base_controller_methods_list = list(filter(lambda x:(pattern.match(x) == None) , dir(BaseController)))
        methods_list = list(filter(lambda x:(pattern.match(x) == None and x not in base_controller_methods_list) , dir(self)))
        return methods_list


    def _validate_http_methods_notation(self):
        for method in self.methods_dict:
            if method.split("_")[0] not in HTTP_METHODS_AS_LIST:
                raise ValueError(f" \"{method}\" method from controller: \"{self.__class__.__name__}\" should have one of {HTTP_METHODS_AS_LIST} at the begging of name, delimited with an underscore.")


    def _validate_methods_dict(self):        
        for method in self.methods_list:
            try:
                self.methods_dict[method]
            except KeyError:
                raise ValueError(f"Method \"{method}\" does not have a path set in controller \"{self.__class__.__name__}\" initialization.")

        for method, path in self.methods_dict.items():
            if method not in self.methods_list:
                raise ValueError(f"Method \"{method}\" declared in controller \"{self.__class__.__name__}\" initialization, does not exist")

    def _regex_escape(string):
        regex_special_chars_map = {chr(i): '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.&~# \t\n\r\v\f'}
        aux = ""
        for ch in string:
            if ch in regex_special_chars_map:
                aux += regex_special_chars_map[ch]
            else:
                aux += ch
        return aux

    def _match_path(pattern_path, path):
        pattern_path = BaseController._regex_escape(pattern_path)  
        pattern = re.compile("\\\{[^{}]*}")
        uncompiled_pattern_string = re.sub(pattern, ".*", pattern_path)
        pattern = re.compile(f"^{uncompiled_pattern_string}$")
        return pattern.match(path)


    def _validate_paths(self, other_controllers):
        def validate_the_2_paths_for_ambiguity(method, path, other_controller, other_method, other_path):
            if BaseController._match_path(path, other_path) is not None:
                comprehensive_error_dict = {"controller" : self.__class__.__name__, "method" : method, "path" : path}
                comprehensive_error_dict_other = {"controller" : other_controller.__class__.__name__, "method" : other_method, "path" : other_path}
                raise ValueError(f"Path ambiguity detected between: {comprehensive_error_dict} and {comprehensive_error_dict_other}")

        for idx, (method, path) in enumerate(self.methods_dict.items()):
            for other_method, other_path in list(self.methods_dict.items())[:idx] + list(self.methods_dict.items())[idx + 1:]:
                if method.split("_")[0] == other_method.split("_")[0]:
                    validate_the_2_paths_for_ambiguity(method, path, self, other_method, other_path)

            for other_controller in other_controllers:
                for other_method, other_path in other_controller.methods_dict.items():
                    if method.split("_")[0] == other_method.split("_")[0]:
                        validate_the_2_paths_for_ambiguity(method, path, other_controller, other_method, other_path)



    def _reverse_string(string):
        stack = list()
        for elem in string:
            stack.append(elem)
        string = ""
        while stack:
            string += stack.pop()
        return string

    def _compute_path_without_request_param_string(path):
        if len(path.split("?")) < 2:
            return path
        path = BaseController._reverse_string(path)
        path = path.split("?", 1)[1]
        path = BaseController._reverse_string(path)
        return path


    def _compute_request_param_string(path):
        if len(path.split("?")) < 2:
            return ""
        path = BaseController._reverse_string(path)
        path = path.split("?", 1)[0]
        path = BaseController._reverse_string(path)
        return path


    def _find_implementation(self, http_request):
        path = BaseController._compute_path_without_request_param_string(http_request.path)
        for method, stored_path in self.methods_dict.items():
            if method.split("_")[0] == http_request.method:
                if BaseController._match_path(stored_path, path):
                    return method
        return None



    def _compute_ordered_list_of_keywords(path):
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


    def _compute_ordered_lists_of_keywords_starts_and_ends(path):
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



    def _compute_ordered_list_of_values(path, stored_path):
        ordered_list_of_keywords_starts, ordered_list_of_keywords_ends = BaseController._compute_ordered_lists_of_keywords_starts_and_ends(stored_path)

        idx_path = ordered_list_of_keywords_starts[0]
        ordered_list_of_values = list()
        slice = path
        for (idx_s, keyword_start), keyword_end in zip(enumerate(ordered_list_of_keywords_starts), ordered_list_of_keywords_ends):
            value = ""
            last_slice = slice
            while BaseController._match_path(stored_path[keyword_start:], slice) is not None and last_slice != "":
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


    def get_path_variables(self, http_request):
        stored_path = self.methods_dict[self._find_implementation(http_request)]   #Can be implemented more efficiently with getting caller name or passing a parameter
        path = BaseController._compute_path_without_request_param_string(http_request.path)
        ordered_list_of_keywords = BaseController._compute_ordered_list_of_keywords(stored_path)
        ordered_list_of_values = BaseController._compute_ordered_list_of_values(path, stored_path)
        path_variables = dict()
        for key, value in zip(ordered_list_of_keywords, ordered_list_of_values):
            path_variables[key] = value
        return path_variables



    def get_query_param(self, http_request):
        path = http_request.path
        path = BaseController._compute_request_param_string(path)
        path = path.split("&")
        for pair in path:
            if re.compile("^[^=]*=[^=]*$").match(pair) is None:
                raise ValueError(f"Querry parameters are not formated correctly: {pair}")
        return {elem.split("=")[0]:elem.split("=")[1] for elem in path}
