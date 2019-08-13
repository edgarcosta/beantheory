import os

def root_path():
    # returns the root path of the git repo
    return os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    '../..'))
