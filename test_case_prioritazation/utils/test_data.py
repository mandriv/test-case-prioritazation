def read(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    data = []
    for line in lines:
        # csv
        bits = line.split(',')
        # first thing in csv is an identifier
        id = bits.pop(0)
        # rest are tests
        for i in range(len(bits)):
            # format each bit so it is a int
            bits[i] = int(bits[i][0])
        # create dict that holds identifier and faults detected
        piece = {
            'id': id,
            'faults': bits
        }
        data.append(piece)
    return data
