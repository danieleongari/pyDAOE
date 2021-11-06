from pydaoe.generate_design import which_design


def test_which():
    """Test the function which design."""
    design = which_design(
        ntreats1=5,
        ntreats2=1,
        nblock1=5,
        nblock2=5,
        nblock3=5,
    )
    assert design == "graeco_latin_square"
