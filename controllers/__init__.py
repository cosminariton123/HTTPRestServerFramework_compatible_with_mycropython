import os
import re

class Controllers():
    def __init__(self, controllers_folder="controllers"):
        pattern = re.compile("^__.*__.*$")
        files_in_controller_folder = os.listdir(controllers_folder)
        files_in_controller_folder = list(filter(lambda x:(pattern.match(x) == None) , files_in_controller_folder))

        Controllers._validate_controller_files(files_in_controller_folder)

        self.controllers = []
        for file in files_in_controller_folder:
            class_name = file.split(".")[0]
            class_name_actual_name_part = class_name.split("_")[0]
            class_name_actual_name_part = class_name_actual_name_part[0].upper() + class_name_actual_name_part[1:]
            class_name_controller_part = class_name.split("_")[1]
            class_name_controller_part = class_name_controller_part[0].upper() + class_name_controller_part[1:]
            class_name = class_name_actual_name_part + class_name_controller_part

            module_name = file.split(".")[0]
            module = __import__(f"{controllers_folder}.{module_name}", {}, {}, [f"{controllers_folder}"])
            self.controllers.append(getattr(module, class_name)())
            self._validate_paths()



    def _validate_controller_file_name(file):
        if len(file.split(".")) != 2:
            return "The only \".\" in filename should be the delimiter"
        if file.split(".")[1] != "py":
            return "Not a \".py\" file"

        file = file.split(".")[0]

        if len(file.split("_")) != 2:
            return "File must contain exactly one \"_\""
        if file.split("_")[0] == "":
            return "The part before _ cannot be blank"
        if file.split("_")[1] != "controller":
            return "The part after _ must be named controller"




    def _validate_controller_files_name(files):
        errors = dict()
        for file in files:
            error = Controllers._validate_controller_file_name(file)
            if error:
                errors[file] = error
        return errors




    def _validate_controller_files(files):
        if len(files) == 0:
            raise Exception("Controller folder must have at least one controller")

        errors = Controllers._validate_controller_files_name(files)
        
        if errors:
            raise ValueError(f"Following errors were found: {errors}")

    def _validate_paths(self):
        pass
