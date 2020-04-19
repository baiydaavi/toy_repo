""" Three State Cellular Automata

This is a python code to create a 3-state cellular
automaton. A given cell can take a value of
0,1 and 2. The neighbourhood is defined by the two
cells above and to the left of the cell above. This
code follows the PEP-8 guidance.
"""
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


def random_string(length):

    """Returns a random bit string of the given length.

    Parameters
    ----------
    length: int
        Posivite integer that specifies the desired length of
        the bit string.

    Returns
    -------
    out: list
        The random bit string given as a list, with int elements.
    """

    if not isinstance(length, int) or length < 0:
        raise ValueError("input length must be a positive ingeter")
    return [random.randint(0, 2) for _ in range(length)]


class ThreeStateCA:

    """Three state cellular automata simulator.

    """

    # __init__ is known as the constructor which simply allows you to
    # define the attributes of the instantiated object from a given
    # class that you want to pass as parameters. Here we want that
    # Three_state_CA class have attributes rule number and an initial
    # condition to be passed as parameters as that is all you need to
    # know for the evolution of the cellular automata

    def __init__(self, rule_number, initial_condition):

        """Initializing the simulator.

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
        """

        for i in initial_condition:
            if i not in [0, 1, 2]:
                raise ValueError("initial condition must be a list of 0s, 1s and 2s")

        self.initial = initial_condition
        self.spacetime = [initial_condition]
        self.current_configuration = initial_condition.copy()
        self._length = len(initial_condition)
        self._rulen = rule_number

        # the underscore before _length defines a private variable

    # functions within a class is known as methods. Evolve is a method
    # of this class

    def lookup_table(self):

        """Returns a dictionary that maps neighbourhood to output.

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
        """

        if (
            not isinstance(self._rulen, int)
            or self._rulen < 0
            or self._rulen > 3 ** 9 - 1
        ):

            raise ValueError(
                "rule_number must be an int between 0 and 3**9-1, inclusive"
            )

        # define the neighborhood

        neighborhoods = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]

        # using numpy (for fun) to return base 3 representation of the rule
        # number with 0 padding as necessary.

        rule_ternary = np.base_repr(
            self._rulen, 3, padding=9 - len(np.base_repr(self._rulen, 3))
        )

        # we will use the dict function to create the lookup table
        # dictionary. The zip function just takes two lists and combine
        # them together to give you the dictionary. We use map so that
        # outputs are ints, not strings

        return dict(zip(neighborhoods, map(int, reversed(rule_ternary))))

    def evolve(self, time_steps):

        """
        Evolves the current configuration of the three state CA for the
        given number of time steps.

        Parameters
        ----------
        time_steps: int
            Positive integer specifying the number of time steps for
            evolving the ECA.
        """

        if time_steps < 0:
            raise ValueError("time_steps must be a non-negative integer")

        # try converting time_steps to int and raise a custom error
        # if this can't be done.

        try:
            time_steps = int(time_steps)
        except ValueError:
            raise ValueError("time_steps must be a non-negative integer")

        for _ in range(time_steps):
            # use underscore if the index will not be used

            new_configuration = []
            for i in range(self._length):

                neighborhood = (
                    self.current_configuration[(i - 1)],
                    self.current_configuration[i],
                )

                new_configuration.append(self.lookup_table()[neighborhood])

            self.current_configuration = new_configuration
            self.spacetime.append(new_configuration)


def spacetime_diagram(spacetime_field, size=12, colors=cm.get_cmap("Greys")):
    """
    Produces a simple spacetime diagram image using matplotlib
    imshow with 'nearest' interpolation.

   Parameters
    ---------
    spacetime_field: array-like (2D)
        1+1 dimensional spacetime field, given as a 2D array or
        list of lists. Time should be dimension 0; so that
        spacetime_field[t] is the spatial configuration at time t.

    size: int, optional (default=12)
        Sets the size of the figure: figsize=(size,size)
    colors: matplotlib colormap, optional (default=cm.get_cmap("Greys"))
    """
    plt.figure(figsize=(size, size))
    plt.imshow(spacetime_field, cmap=colors, interpolation="nearest")
    plt.show()


def run_three_state_ca(rule_num, init_condition, time):
    """ This function runs the 3 state CA code.

    This function takes three parameters:
    1. rule_num -> This is the rule number.
    2. init_condition -> This is the initial condition.
    3. time -> This tells the number of timesteps.
    """

    # Initiating the three state CA class

    rule_user = ThreeStateCA(rule_num, init_condition)

    # Evolving the spacetime using evolve method

    rule_user.evolve(time)

    # Plotting the spacetime field

    spacetime_diagram(rule_user.spacetime)


# We will have the user choose a rule number

RULE_NUM = int(input("Choose a number between 0 and 3**9-1 as the rule number:"))

# Choose the length for the initial condition

LEN_INIT = int(input("Input the length of the initial condition:"))

# We will have the user decide if they want to put in a random initial
# condition or the one they want

RANDOM_INIT = input("Enter Y if you want a random initial condition else enter N:")

if RANDOM_INIT in ("Y", "y"):
    INIT_COND = random_string(LEN_INIT)
else:
    INIT_COND = []
    print("Choose between 0,1 or 2 as each element of the initial condition one by one")
    for _ in range(0, LEN_INIT):
        INIT_COND.append(int(input()))

print("The initial conditions chosen by you is", INIT_COND)

# Choose the number of timesteps for evolution

TIME = int(input("Choose the number of timesteps for evolution:"))

# We will call the function run_three_state_CA to run the evolution

run_three_state_ca(RULE_NUM, INIT_COND, TIME)
