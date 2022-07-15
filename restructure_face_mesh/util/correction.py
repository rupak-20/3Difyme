def read_spike(read_path: str):
    spikes = []
    try:
        with open(read_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                spikes.append(int(line))
    except FileNotFoundError:
        print('file not found')
    
    return spikes

def correct(obj_path: str, ver_path: str):
    spikes = set(read_spike(ver_path))
    print(spikes)
    try:
        with open(obj_path, 'r') as file:
            lines = file.readlines()
            spikelines = ''
            for i, line in enumerate(lines):
                if i>3 and i in spikes:
                    spikelines += line
            with open('not_found.obj', 'w') as expo:
                expo.writelines(spikelines)
    except(FileNotFoundError):
        print('file not found')


if __name__ == '__main__':
    correct('Task-6/face.obj', 'Task-6/spikes.txt')


    
