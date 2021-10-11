import pandas as pd
from pydoe.simple_comparative import t_test


def test_example_2_0():
    """Example in the text."""
    data = {
        'Mortar': [
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'mod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
            'unmod',
        ],
        'Tension Bond Strength': [
            16.85, 16.40, 17.21, 16.35, 16.52, 17.04, 16.96, 17.15, 16.59, 16.57, 16.62, 16.75, 17.37, 17.12, 16.98,
            16.87, 17.34, 17.02, 17.08, 17.27
        ]
    }
    df = pd.DataFrame(data)

    res = t_test(df, treat_col='Mortar', measure_col='Tension Bond Strength')

    assert res['P-Value'] == 0.0421967159248899
