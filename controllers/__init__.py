import os
import re
from io import StringIO

from my_framework.my_http.http_data_types import HttpResponse
from my_framework.my_http.http_constants.response_codes import INTERNAL_SERVER_ERROR
from config import CONTROOLERS_FOLDER_PATH, PRODUCTION
from my_framework.my_http.dtos import ErrorMessage

class ControllerManager():
    def __init__(self, controllers_folder_path):
        pattern = re.compile("^__.*__.*$")
        files_in_controller_folder = os.listdir(controllers_folder_path)
        files_in_controller_folder = list(filter(lambda x:(pattern.match(x) == None) , files_in_controller_folder))

        ControllerManager._validate_controller_files(controllers_folder_path, files_in_controller_folder)

        self.controllers = []
        for file in files_in_controller_folder:
            class_name = file.split(".")[0]
            class_name_actual_name_part = class_name.split("_")[0]
            class_name_actual_name_part = class_name_actual_name_part[0].upper() + class_name_actual_name_part[1:]
            class_name_controller_part = class_name.split("_")[1]
            class_name_controller_part = class_name_controller_part[0].upper() + class_name_controller_part[1:]
            class_name = class_name_actual_name_part + class_name_controller_part

            module_name = file.split(".")[0]
            module = __import__(f"{controllers_folder_path}.{module_name}", {}, {}, [f"{controllers_folder_path}"])
            self.controllers.append(getattr(module, class_name)())

        self._validate_controllers_methods_dict()
        self._validate_paths()



    def _find_error_in_controller_files_name(files):
        for file in files:
            file_does_not_comply_string = f"File \"{file}\" does not comply."

            if len(file.split(".")) != 2:
                return f"The only \".\" in filename should be the type delimiter. {file_does_not_comply_string}"
            if file.split(".")[1] != "py":
                return f"Not a \".py\" file.{file_does_not_comply_string}"

            file = file.split(".")[0]
            if len(file.split("_")) != 2:
                return f"File must contain exactly one \"_\". {file_does_not_comply_string}"
            if file.split("_")[0] == "":
                return f"The part before \"_\" cannot be blank. {file_does_not_comply_string}"
            if file.split("_")[1] != "controller":
                return f"The part after \"_\" must be named \"controller\". {file_does_not_comply_string}"
        return None





    def _validate_controller_files(controllers_folder_path, files):
        if len(files) == 0:
            raise Exception(f"Controller folder \"{controllers_folder_path}\" must have at least one controller file")

        error = ControllerManager._find_error_in_controller_files_name(files)
        if error is not None:
            raise ValueError(error)


    def _validate_controllers_methods_dict(self):
        for controller in self.controllers:
            controller._validate_methods_dict()


    def _validate_paths(self):
        for idx, controller in enumerate(self.controllers):
            controller._validate_paths(self.controllers[:idx] + self.controllers[idx + 1:])



    def find_implementation_and_execute(self, http_request):
        for controller in self.controllers:
            method = controller._find_implementation(http_request)
            if method is not None:
                method_address = getattr(controller, method)
                try:
                    result = method_address(http_request)
                    if not isinstance(result, HttpResponse):
                        raise ValueError(f"Method \"{method}\" from controller \"{controller.__class__.__name__}\" doesn't return an \"{HttpResponse.__name__}\" object. It returns \"{result.__class__.__name__}\".")
                except Exception as e:
                    stacktrace_error_message = StringIO()
                    import sys
                    if sys.implementation.name == "micropython":
                        sys.print_exception(e, stacktrace_error_message)
                    else:
                        import traceback
                        traceback.print_exception(e, file=stacktrace_error_message)
                    print(stacktrace_error_message.getvalue())

                    body = ""
                    if not PRODUCTION:
                        body = ErrorMessage(stacktrace_error_message.getvalue())
                    result = HttpResponse(INTERNAL_SERVER_ERROR, {}, body)
                return result

CONTROLLER_MANAGER_INSTANCE = ControllerManager(CONTROOLERS_FOLDER_PATH)
