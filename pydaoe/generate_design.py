"""Module for generating desing matrices."""


def which_design(ntreats1, ntreats2=1, nblock1=1, nblock2=1, nblock3=1):
    """Return the name of the design one should run, given the specifics."""
    if ntreats2 == 1:
        if nblock1 == nblock2 == nblock3 == 1:
            if ntreats1 == 2:
                return "t_test"
            return "single_factor"
        if nblock1 > 1 and nblock2 == nblock3 == 1:
            return "rcbd"
        if ntreats1 == nblock1 == nblock2 and nblock3 == 1:
            return "latin_square"
        if ntreats1 == nblock1 == nblock2 == nblock3:
            return "graeco_latin_square"
    if ntreats1 == ntreats2 == 2 and nblock1 == nblock2 == nblock3 == 1:
        return "twok_factorial"
    if ntreats1 == ntreats2 == 3 and nblock1 == nblock2 == nblock3 == 1:
        return "threek_factorial"
    if ntreats1 > 1 and ntreats2 > 1 and nblock1 == nblock2 == nblock3 == 1:
        return "two_factor_factorial"
    raise NotImplementedError("Not able to recognize the proper design for this problem.")
