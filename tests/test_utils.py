from pydaoe.utils import contrast_constants_table


def test_cc_table():
    """Test contrast_constants_table for k=4."""

    n_factors = 4
    cc_table = contrast_constants_table(n_factors)

    assert cc_table.loc["ad", "ABC"] == +1
