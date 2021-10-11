"""Module for generating desing matrices."""


def which_design(ntreats1, ntreats2=0, nblock1=0, nblock2=0, nblock3=0):
    """Return the name of the design one should run, given the specifics."""
    if ntreats2 == 0:
        if nblock1 == nblock2 == nblock3 == 0:
            if ntreats1 == 2:
                return "t_test"
            return "single_factor"
        if nblock1 > 0 and nblock2 == nblock3 == 0:
            return "rcbd"
        if ntreats1 == nblock1 == nblock2 and nblock3 == 0:
            return "latin_square"
        if ntreats1 == nblock1 == nblock2 == nblock3:
            return "graeco_latin_square"
    raise NotImplementedError("Not able to recognize the proper design for this problem.")
