from controllers import Controllers



def main():
    coco = Controllers()
    print(coco.controllers[0].methods_dict)

if __name__ == '__main__':
    main()
