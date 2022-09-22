import re
from my_http.http_handler import BaseController
from controllers.coco_controller import CocoController

class A():
    def __init__(self):
        super().__init__()
    
    def racaciunga(self):
        return True

class B(A, CocoController):
    def __init__(self):
        super().__init__()

def main():

    a = "COCO/Are/{AAAA}gunoi/mere"

    b = re.sub("{.*}", "{.*}", a)

    print(a)
    print(b)

    a= "coco"
    b= "coco"

    print(a is b)


    a = {"coco" : 5}

    for elem in a.keys():
        print(elem)
    print(a.keys())

if __name__ == "__main__":
    main()