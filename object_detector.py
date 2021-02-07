def read_classes(filename: str) -> list:
    ''' read class names from a text file
    and return a list
    '''
    
    with open(filename, 'r') as f:
        classes = f.readlines()
        
    return [x.strip('\n') for x in classes]