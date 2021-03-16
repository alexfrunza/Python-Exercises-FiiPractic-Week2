"""
    Implement a function that prints the following output from the given input:

    Input:
    my_dict = {
        'a': 1,
        'b': {'c': 2},
        'd': {
            'e': {'f': 3},
            'g': 4
        }
    }

    Output:
    a.1
    b.c.2
    d.e.f.3
    d.g.4
"""


def print_function(d, last_keys):
    for key, value in d.items():
        if isinstance(value, dict):
            print_function(value, last_keys + f"{key}.")
        else:
            print(f"{last_keys}{key}.{value}")

# --------------------------------------------------------------------
# Tests


my_dict = {
    'a': 1,
    'b': {'c': 2},
    'd': {
        'e': {
            'f': 3,
            'z': 4
        },
        'g': 4
    }
}


print_function(my_dict, "")
