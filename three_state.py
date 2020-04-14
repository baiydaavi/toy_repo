import random
import numpy as np
from matplotlib import pyplot as plt

def random_string(length):

    '''Returns a random bit string of the given length. 
    
    Parameters
    ----------
    length: int
        Posivite integer that specifies the desired length of 
        the bit string.
        
    Returns
    -------
    out: list
        The random bit string given as a list, with int elements.
    '''
    
    if not isinstance(length, int) or length < 0:
        raise ValueError("input length must be a positive ingeter")
    return [random.randint(0,2) for _ in range(length)]

def lookup_table(rule_number):

    '''Returns a dictionary that maps neighbourhood to output.
    
    Returns a dictionary which maps three state CA neighborhoods to 
    output values according to the rule number.
    Parameters
    ----------
    rule_number: int
        Integer value between 0 and 3**9-1, inclusive.
        
    Returns
    -------
    lookup_table: dict
        Lookup table dictionary that maps neighborhood tuples to their
        output according to the three state CA local evolution rule 
        (i.e. the lookup table), as specified by the rule number. 
    '''
    
    if not isinstance(rule_number, int) 
		or rule_number < 0 or rule_number > 3**9-1:
		
        raise ValueError("rule_number must be an int "
        				 "between 0 and 3**9-1, inclusive")
    
    # define the neighborhood
        
    neighborhoods = [
        (0,0), (0,1), (0,2), 
    	(1,0), (1,1), (1,2), 
    	(2,0), (2,1), (2,2)
    	] 							
    
    # using numpy (for fun) to return base 3 representation of the rule  
    # number with 0 padding as necessary.
    
    rule_ternary = np.base_repr(
    	rule_number, 3,
    	padding=9-len(np.base_repr(rule_number,3))) 
    
    # we will use the dict function to create the lookup table 
    # dictionary. The zip function just takes two lists and combine
    # them together to give you the dictionary. We use map so that 
    # outputs are ints, not strings
    
    return dict(zip(neighborhoods, map(int,reversed(rule_ternary)))) 


class ThreeStateCA(object):

    '''Three state cellular automata simulator.
    
    '''
    
    #__init__ is known as the constructor which simply allows you to
    # define the attributes of the instantiated object from a given 
    # class that you want to pass as parameters. Here we want that
    # Three_state_CA class have attributes rule number and an initial
    # condition to be passed as parameters as that is all you need to 
    #know for the evolution of the cellular automata
    
    def __init__(self, rule_number, initial_condition):
    
        '''Initializing the simulator.
        
        Initializes the simulator for the given rule number and
        initial condition.
        
        Parameters: These are as attributes too. We just desire for 
        these attributes to be passed as parameters.
        ----------
        rule_number: int
            Integer value between 0 and 3**9-1, inclusive. The total 
            number of possible rules are 3**9 for the three state CA 
            case.
            
        initial_condition: list
            String used as the initial condition for the three state 
            CA. Elements of the list should be 0s,1s and 2s. 
        
        Attributes
        ----------
        lookup_table: dict
            Lookup table for the three state CA given as a dictionary,
            with neighborhood tuple keys. 
        initial: array_like
            Copy of the initial conditions used to instantiate the 
            simulator.
        spacetime: array_like
            2D array (list of lists) of the spacetime field created by
            the simulator.
        current_configuration: array_like
            List of the spatial configuration of the three state CA at 
            the current time.
        '''
        
        for i in initial_condition:
            if i not in [0,1,2]:
                raise ValueError("initial condition must be a list of "
                				 "0s, 1s and 2s")
                
        self.lookup_table = lookup_table(rule_number)
        self.initial = initial_condition
        self.spacetime = [initial_condition]
        self.current_configuration = initial_condition.copy()
        self._length = len(initial_condition) 
        
        # the underscore before _length defines a private variable
	
	# functions within a class is known as methods. Evolve is a method 
	# of this class
	
    def evolve(self, time_steps):
      
        '''
        Evolves the current configuration of the three state CA for the
        given number of time steps.
        
        Parameters
        ----------
        time_steps: int
            Positive integer specifying the number of time steps for
            evolving the ECA.  
        '''
        
        if time_steps < 0:
            raise ValueError("time_steps must be a non-negative " 
            				 "integer")
            
        # try converting time_steps to int and raise a custom error
        # if this can't be done.
        
        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("time_steps must be a non-negative "
            				 "integer")
		
        for _ in range(time_steps): 
        	# use underscore if the index will not be used
        	
            new_configuration = []
            for i in range(self._length):

                neighborhood = (self.current_configuration[(i-1)], 
                                self.current_configuration[i])

                new_configuration.append(
                	self.lookup_table[neighborhood])

            self.current_configuration = new_configuration
            self.spacetime.append(new_configuration)
