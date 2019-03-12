import scipy.io as spio
'''
By Jose

To read flightdata.mat file to python follow step by step to call each dictionary


'''
# ==========Definitions===============
def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

# ===========HOW TO CALL EACH DATA================
'''
first open the .mat file using loadmat
call using the following sequences and it will give you an array of the data
example below is for angle of attack
'''
data = loadmat('FTISxprt-20190307_124723.mat')
AoA = data['flightdata']['vane_AOA']['data']
print(AoA)
