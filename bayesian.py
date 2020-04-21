""" Calculating an approximate value of e using Bayesian inference.

In this code, we will use Bayesian inference to find the posterior
probability density of e given a dataset drawn from a normal
distribution with zero mean and unit variance. We will find an
analytical solution for the unnormalized posterior distribution
which does the job as we are using the Metropolis-Hastings
algorithm. The posterior density is given by

P(x|a) = N(a) a^{-x^2/2}

where,

N(a) = sqrt[log(a)/(2*pi)]

We find N(a) by making sure that the integral of P(x|a) from -inf to
+inf is 1. We use the fact that integral of e^{-bx^2} from -inf to
+inf is equal to sqrt[pi/b].
P(x|a) is the likelihood here. To find the posterior, we also need to
know what prior to use. We use a prior such that probability of a<=1 is
0. This is because N(a) will be undefined for a<1. We choose a prior of
1 for all other values of a.
"""

import numpy as np
import matplotlib.pyplot as plt


def post_a_x(a_value, sq_sum_data, length):

    """ Calculating the posterior P(a|{x})

    The formula for posterior P(a|{x}) is

    P(a|{x}) = (N(a))^n * a^{-(x_1^2+x_2^2 + ... + x_n^2)/2}

    Parameters:

    1. a - The value of a for which the posterior is calculated.
    2. sq_sum_data - Importing the sum of the square of x values of the
       datapoints. Not importing the individual datapoints as that is
       unnecessary.
    3. length - The number of x datapoints.
    """

    return pow(np.log(a_value) / (2 * np.pi), length / 2) * pow(
        a_value, -sq_sum_data / 2
    )


def metropolis_hastings(iterations, initial_a, data):

    """ The Metropolis-Hastings Algorithm

    Parameters:

    1. iterations - The number of iterations over which the chain runs.
    2. initial_a - The starting value of a for the mcmc chain.
    3. sq_sum_data - Importing the sum of the square of x values of the
       datapoints. Not importing the individual datapoints as that is
       unnecessary.
    4. length - The number of x datapoints.
    """

    a_old = initial_a  # old data point

    e_est = []  # list of the estimates for e at each iteration

    sum_sq_data = sum(
        map(lambda x: x * x, data)
    )  # sum of the square of the x datapoints

    length = len(data)  # number of datapoints

    for _ in range(iterations):

        # Choose a new data point using the generating function
        # which is a gaussian with mean a_old and variance 1.

        a_new = np.random.randn() + a_old

        if a_new <= 1:

            pass  # Do not accept the new data point if it is < 1

        elif (
            post_a_x(a_new, sum_sq_data, length) / post_a_x(a_old, sum_sq_data, length)
            >= 1
        ):

            # accept the new data point if it P(a_new|x) > P(a_old|x)

            a_old = a_new

        elif np.random.uniform(0, 1) < post_a_x(a_new, sum_sq_data, length) / post_a_x(
            a_old, sum_sq_data, length
        ):

            # accept the new data point with a probablity
            # given by P(a_new|x)/P(a_old|x) which is less than 1

            a_old = a_new

        e_est.append(a_old)  # append the current value of a to the list

    return e_est


def plot_post_a_x(a_array, x_data):

    """ Plot the posterior probability of a given x
    """

    sum_sq_data = sum(map(lambda x: x * x, x_data))

    plt.plot(
        a_array, list(map(lambda y: post_a_x(y, sum_sq_data, len(x_data)), a_array))
    )
    plt.xlabel("a")
    plt.ylabel("posterior probability")
    plt.savefig("post_prob_analytical.jpg")
    plt.close()


def plot_trace_histogram(post_e):

    """ Plot the trace plot and histogram
    """

    # Plotting the trace plot

    plt.plot(np.arange(0, len(post_e)), post_e)
    plt.xlabel("Iteration")
    plt.ylabel("Parameter Value")
    plt.savefig("trace_plot.jpg")
    plt.close()

    # Plotting the histogram

    plt.hist(post_e, bins="auto")
    plt.xlabel("parameter")
    plt.ylabel("posterior probability distribution")
    plt.savefig("histogram.jpg")
    plt.close()


# Drawing 100 random samples of x from a gaussian of mean zero
# and unit variance

X_DATA = np.random.randn(100)  # drawing

# defining the values of a over which the analytical posterior
# probability is calculted

A_ARRAY = np.arange(1.5, 6, 0.01)

# plotting the analytical posterior probability

plot_post_a_x(A_ARRAY, X_DATA)

# Running the Metropolis-Hastings algorithm

ITER_NUM = 20000  # number of iterations

INIT_A = 10  # the initial value of a for the chain

POST_E = metropolis_hastings(ITER_NUM, INIT_A, X_DATA)

# Plotting the trace plot and the histogram

plot_trace_histogram(POST_E)
