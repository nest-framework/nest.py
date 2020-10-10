"""
Created by Epic at 10/10/20
"""


class NoProjectFound(BaseException):
    def __init__(self):
        super().__init__("No project was found. Create one with nest init.")


class ProjectAlreadyExists(BaseException):
    def __init__(self):
        super().__init__("There already exists a project in this directory")


class ModuleAlreadyAdded(BaseException):
    def __init__(self):
        super().__init__("This module is already added?")


class IncorrectModuleFormat(BaseException):
    def __init__(self):
        super().__init__("The module name is not formatted correctly")
