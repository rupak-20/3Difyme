def make_mapping_list(mapping_path: str, obj_path: str, export_path: str):
    VERTICES = []
    try:
        # read .obj file to get vertices
        with open(obj_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'v' and line[1] != 't' and line[1] != 'n':
                    x, y, z = [float(x) for x in list(line[2:].split(' '))]
                    # store vertices as an numpy array
                    VERTICES.append([x, y, z])
    except(FileNotFoundError):
        print('file not found')

    # print(VERTICES)

    MAPPINGS = {}
    try:
        with open(mapping_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == '#' or line == '\n':
                    continue
                else:
                    if len(list(line[:-2].split(' '))) == 1:
                        continue
                    else:
                        a, b = [int(x) for x in list(line.split(' '))]
                        print(a, b)
                        if a not in MAPPINGS.keys():
                            MAPPINGS[a] = b
                        else:
                            print('same value found for index', a, ':', b)
    except(FileNotFoundError):
        print('file not found')

    # print(MAPPINGS)

    with open(export_path, 'w') as export:
        for i in range(1, len(VERTICES)):
            if i not in MAPPINGS.keys():
                print(i)
                export.writelines(
                    'v ' + str(VERTICES[i][0]) + ' ' + str(VERTICES[i][1]) + ' ' + str(VERTICES[i][2]) + '\n')
            # else:
            #     export.writelines(str(i) + ' ' + '\n')


if __name__ == '__main__':
    mapping = 'mapping_standard.txt'
    obj = 'Task-6/mp_face.obj'
    expo = 'not_found.obj'

    make_mapping_list(mapping, obj, expo)
