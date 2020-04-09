import random
import numpy as np
from matplotlib import pyplot as plt

def random_string(length):
    '''
    Returns a random bit string of the given length. 
    
    Parameters
    ----------
    length: int
        Posivite integer that specifies the desired length of the bit string.
        
    Returns
    -------
    out: list
        The random bit string given as a list, with int elements.
    '''
    if not isinstance(length, int) or length < 0:
        raise ValueError("input length must be a positive ingeter")
    return [random.randint(0,2) for _ in range(length)]

def lookup_table(rule_number):
    '''
    Returns a dictionary which maps three state CA neighborhoods to output values.
    
    Parameters
    ----------
    rule_number: int
        Integer value between 0 and 3**9-1, inclusive.
        
    Returns
    -------
    lookup_table: dict
        Lookup table dictionary that maps neighborhood tuples to their output according to the 
        three state CA local evolution rule (i.e. the lookup table), as specified by the rule number. 
    '''
    
    if not isinstance(rule_number, int) or rule_number < 0 or rule_number > 3**9-1:
        raise ValueError("rule_number must be an int between 0 and 3**9-1, inclusive")
        
    neighborhoods = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)] #define the neighbourhood
    
    #using numpy (for fun) to return base 3 representation of the rule number with 0 padding as necessary
    rule_ternary = np.base_repr(rule_number,3,padding=9-len(np.base_repr(rule_number,3))) 
    
    #we will use the dict function to create the lookup table dictionary. The zip function just takes two lists and combine them together to give you the dictionary
    return dict(zip(neighborhoods, map(int,reversed(rule_ternary)))) # use map so that outputs are ints, not strings


