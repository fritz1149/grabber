def unique(name):
    s = set()
    with open(f'raw_{name}.txt', 'r') as file:
        for line in file.readlines():
            s.add(line.strip() + '\n')
    with open(f'{name}.txt', 'w') as file:
        file.writelines(s)

unique('1-3')
unique('4')