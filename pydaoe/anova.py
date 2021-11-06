"""Module for tests based on the Analysis of Variance (ANOVA)."""
from scipy import stats
import pandas as pd

from pydaoe.utils import ALPHABET, contrast_constants_table


def _sum_y2_k(df, k, y):
    """Sum of the squared sums over the column k.
    Typically `k` is the Factor or Block column and `y` is the column of Observations.
    """
    return (df.groupby(k).sum()[y]**2).sum()


def _sum_y2_kj(df, k, j, y):
    """Sum of the squared sums over the column k and j, i.e., for each replica.
    Typically `k` and `j` are the Factors and `y` is the column of Observations.
    """
    return (df.groupby([k, j]).sum()[y]**2).sum()


def _ssyyy(df, k, j, y):
    """Double sum in Equation 5.20."""
    s = 0
    for _, row in df.iterrows():
        s += row[y] * df.groupby(k).sum().at[row[k], y] * df.groupby(j).sum().at[row[j], y]
    return s


def _y2_sum(df, y):
    """Square of the y sum."""
    return df[y].sum()**2


def _sum_y2(df, y):
    """Sum of y squared."""
    return (df[y]**2).sum()


def single_factor(df, factor_col=None, observ_col=None):
    """Single Factor experiment, also called One-Way ANOVA."""

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    n_treats = len(treats)  # a
    n_observ = len(df[df[factor_col] == treats[0]])  # n
    n_total = n_treats * n_observ  # N

    # Check if all treatements have the same number of observation
    for treat in treats:
        if len(df[df[factor_col] == treat]) != n_observ:
            raise NotImplementedError(
                "For Single-Factor test all treatments should have the same number of observations.")

    # Degree of Freedom
    dof_treat = n_treats - 1
    dof_error = n_total - n_treats
    dof_total = n_total - 1

    # Sum of Squares
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / n_observ - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 3.3
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_treat, ms_treat, f0_treat, pval_treat],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]

    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def rcbd(df, factor_col=None, block_col=None, observ_col=None):
    """Randomized Complete Block Design."""

    # Default format of the dataframe
    cols = [factor_col, block_col, observ_col]
    if None in cols:
        factor_col, block_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    blocks = list(df[block_col].unique())
    blocks = sorted(blocks)

    n_treats = len(treats)  # a
    n_blocks = len(blocks)  # b
    n_total = n_treats * n_blocks  # N

    # Check if all observations are provided
    if len(df) != n_total:
        raise NotImplementedError("Incomplete RCBD not implemented.")

    # Degree of Freedom
    dof_treat = n_treats - 1
    dof_block = n_blocks - 1
    dof_error = dof_treat * dof_block
    dof_total = n_total - 1

    # Sum of Squares
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / n_blocks - _y2_sum(df, observ_col) / n_total
    ss_block = _sum_y2_k(df, block_col, observ_col) / n_treats - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat - ss_block

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_block = ss_block / dof_block
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 4.2
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_treat, ms_treat, f0_treat, pval_treat],
        ["Blocks", ss_block, dof_block, ms_block, "", ""],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def latin_square(df, factor_col=None, block1_col=None, block2_col=None, observ_col=None):
    """Latin square design."""

    # Default format of the dataframe
    cols = [factor_col, block1_col, block2_col, observ_col]
    if None in cols:
        factor_col, block1_col, block2_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    block1, block2 = list(df[block1_col].unique()), list(df[block2_col].unique())
    block1, block2 = sorted(block1), sorted(block2)

    # Considering equal treat, rows, cols
    n_treats = len(treats)  # p
    n_block1 = len(block1)  # "Rows", p
    n_block2 = len(block2)  # "Columns", p

    if not n_treats == n_block1 == n_block2:
        raise NotImplementedError("Incomplete Latin Square not implemented.")

    p = n_treats  # == n_block1 == n_block2 in Latin Square Design
    n_total = p**2

    # Degree of Freedom
    dof_p = p - 1
    dof_error = (p - 2) * (p - 1)
    dof_total = n_total - 1

    # Sum of Squares]
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block1 = _sum_y2_k(df, block1_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block2 = _sum_y2_k(df, block2_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat - ss_block1 - ss_block2

    # Mean Squares
    ms_treat = ss_treat / dof_p
    ms_block1 = ss_block1 / dof_p
    ms_block2 = ss_block2 / dof_p
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_p, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 4.10
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_p, ms_treat, f0_treat, pval_treat],
        ["Block1", ss_block1, dof_p, ms_block1, "", ""],
        ["Block2", ss_block2, dof_p, ms_block2, "", ""],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def graeco_latin_square(df, factor_col=None, block1_col=None, block2_col=None, block3_col=None, observ_col=None):
    """Graeco-Latin square design."""

    # Default format of the dataframe
    cols = [factor_col, block1_col, block2_col, block3_col, observ_col]
    if None in cols:
        factor_col, block1_col, block2_col, block3_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    block1, block2, block3 = list(df[block1_col].unique()), list(df[block2_col].unique()), list(df[block3_col].unique())
    block1, block2, block3 = sorted(block1), sorted(block2), sorted(block3)

    # Considering equal treat, rows, cols
    n_treats = len(treats)  # "Latin Letter", p
    n_block1 = len(block1)  # "Greek Letter", p
    n_block2 = len(block2)  # "Rows", p
    n_block3 = len(block3)  # "Columns", p

    if not n_treats == n_block1 == n_block2 == n_block3:
        raise NotImplementedError("Incomplete Graeco-Latin Square not implemented.")

    p = n_treats
    n_total = p**2

    # Degree of Freedom
    dof_p = p - 1
    dof_error = (p - 3) * (p - 1)
    dof_total = n_total - 1

    # Sum of Squares
    ss_treats = _sum_y2_k(df, factor_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block1 = _sum_y2_k(df, block1_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block2 = _sum_y2_k(df, block2_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block3 = _sum_y2_k(df, block3_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treats - ss_block1 - ss_block2 - ss_block3

    # Mean Squares
    ms_treats = ss_treats / dof_p
    ms_block1 = ss_block1 / dof_p
    ms_block2 = ss_block2 / dof_p
    ms_block3 = ss_block3 / dof_p
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treats / ms_error
    rv = stats.f(dof_p, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 4.19
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treats, dof_p, ms_treats, f0_treat, pval_treat],
        ["Block1", ss_block1, dof_p, ms_block1, "", ""],
        ["Block2", ss_block2, dof_p, ms_block2, "", ""],
        ["Block3", ss_block3, dof_p, ms_block3, "", ""],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def two_factor_factorial(df, factor1_col=None, factor2_col=None, observ_col=None):
    """Two-Factor Factorial, Fixed Effects Model."""

    # Default format of the dataframe
    cols = [factor1_col, factor2_col, observ_col]
    if None in cols:
        factor1_col, factor2_col, observ_col = df.columns

    treats1 = list(df[factor1_col].unique())
    treats1 = sorted(treats1)

    treats2 = list(df[factor2_col].unique())
    treats2 = sorted(treats2)

    n_treats1 = len(treats1)  # a
    n_treats2 = len(treats2)  # b

    # Check if all combination of factor1/factor2 have the same number of replicas
    replicas = df.groupby([factor1_col, factor2_col]).count()[observ_col].unique()  # np.array
    if len(replicas) > 1:
        raise NotImplementedError("Incomplete two factorial not implemented.")

    n_replicas = replicas[0]  # n, Only one value if previous check passed
    n_total = n_treats1 * n_treats2 * n_replicas  # = len(df)

    if n_replicas > 1:
        # Degree of Freedom
        dof_treat1 = n_treats1 - 1
        dof_treat2 = n_treats2 - 1
        dof_inter = dof_treat1 * dof_treat2
        dof_error = n_treats1 * n_treats2 * (n_replicas - 1)
        dof_total = n_treats1 * n_treats2 * n_replicas - 1

        # Sum of Squares
        ss_treat1 = _sum_y2_k(df, factor1_col, observ_col) / (n_treats1 * n_replicas) - _y2_sum(df,
                                                                                                observ_col) / n_total
        ss_treat2 = _sum_y2_k(df, factor2_col, observ_col) / (n_treats2 * n_replicas) - _y2_sum(df,
                                                                                                observ_col) / n_total
        ss_inter = _sum_y2_kj(df, factor1_col, factor2_col, observ_col) / n_replicas - _y2_sum(
            df, observ_col) / n_total - ss_treat1 - ss_treat2
        ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
        ss_error = ss_total - ss_treat1 - ss_treat2 - ss_inter

        # Mean Squares
        ms_treat1 = ss_treat1 / dof_treat1
        ms_treat2 = ss_treat2 / dof_treat2
        ms_inter = ss_inter / dof_inter
        ms_error = ss_error / dof_error

        # test statistic
        f0_treat1 = ms_treat1 / ms_error
        f0_treat2 = ms_treat2 / ms_error
        f0_inter = ms_inter / ms_error

        # Print Table 5.3
        cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
        rows = [
            ["Factor-1", ss_treat1, dof_treat1, ms_treat1, f0_treat1,
             stats.f(dof_treat1, dof_error).sf(f0_treat1)],
            ["Factor-2", ss_treat2, dof_treat2, ms_treat2, f0_treat2,
             stats.f(dof_treat2, dof_error).sf(f0_treat2)],
            ["Interaction", ss_inter, dof_inter, ms_inter, f0_inter,
             stats.f(dof_inter, dof_error).sf(f0_inter)],
            ["Error", ss_error, dof_error, ms_error, "", ""],
            ["Total", ss_total, dof_total, "", "", ""],
        ]
        table = pd.DataFrame(rows, columns=cols)
        table = table.set_index("Source of Variation")
        return table

    # elif n_replicas==1

    # Degree of Freedom
    dof_treat1 = n_treats1 - 1
    dof_treat2 = n_treats2 - 1
    dof_n = 1
    dof_error = dof_treat1 * dof_treat2 - 1
    dof_total = n_treats1 * n_treats2 - 1

    # Sum of Squares
    ss_treat1 = _sum_y2_k(df, factor1_col, observ_col) / n_treats2 - _y2_sum(df, observ_col) / n_total
    ss_treat2 = _sum_y2_k(df, factor2_col, observ_col) / n_treats1 - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_residual = ss_total - ss_treat1 - ss_treat2
    ss_n = (_ssyyy(df, factor1_col, factor2_col, observ_col) - df[observ_col].sum() *
            (ss_treat1 + ss_treat2 + _y2_sum(df, observ_col) / n_total))**2
    ss_n /= n_treats1 * n_treats2 * ss_treat1 * ss_treat2
    ss_error = ss_residual - ss_n

    # Mean Squares
    ms_treat1 = ss_treat1 / dof_treat1
    ms_treat2 = ss_treat2 / dof_treat2
    ms_n = ss_n / dof_n
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat1 = ms_treat1 / ms_error
    f0_treat2 = ms_treat2 / ms_error
    f0_n = ms_n / ms_error

    # Print Table 5.9
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Factor-1", ss_treat1, dof_treat1, ms_treat1, f0_treat1,
         stats.f(dof_treat1, dof_error).sf(f0_treat1)],
        ["Factor-2", ss_treat2, dof_treat2, ms_treat2, f0_treat2,
         stats.f(dof_treat2, dof_error).sf(f0_treat2)],
        ["Nonadditivity", ss_n, dof_n, ms_n, f0_n,
         stats.f(dof_n, dof_n).sf(f0_n)],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def twoktest(df, test):
    """Get the sum of tests from a 2k factorial, given test index such as (1), a, b, abc, etc."""
    factors = list(df.columns[:-1])
    k = len(factors)
    treat_dict = {factor: sorted(df[factor].unique()) for factor in factors}
    coded_factors = ALPHABET.lower()[:k]  # e.g., abcd for k=4

    if test == "(1)":
        hilo = [0] * k
    else:
        hilo = [int(f in test) for f in coded_factors]

    for factor, hl in zip(factors, hilo):
        df = df[df[factor] == treat_dict[factor][hl]]

    return df.iloc[:, -1].sum()


def twok_factorial(df):
    """2^k Factorial Design.
    This implementation works for the General 2^k, therefore for whatever number of factors.
    """

    # Default format of the dataframe
    # NOTE: for semplicity of later calculations we impose the observations to be in the last column
    factors = list(df.columns[:-1])
    observ_col = df.columns[-1]

    treat_dict = {factor: sorted(df[factor].unique()) for factor in factors}

    # Check if all factors have 2 treatements
    for factor, treats in treat_dict.items():
        ntreats = len(treats)
        if ntreats != 2:
            raise Exception(f"Factor {factor} has {ntreats}!=2 treatements: not 2^k design.")

    # Check if all tests have the same number of replicas
    replicas = df.groupby(factors).count()[observ_col].unique()  # np.array
    if len(replicas) > 1:
        raise NotImplementedError("All tests must have the same number of replicas.")

    n_fact = len(factors)  # k
    n_repl = replicas[0]  # n, Only one value in the array

    # Load the contrast constants, store the sum of observations for each test
    cc_table = contrast_constants_table(n_fact)
    sumtests = {test: twoktest(df, test) for test in cc_table.index}
    effects = list(cc_table.columns)

    # Evaluate effects and their sum of squares
    res_dict = {}
    for effect in effects:
        contrast = sum([cc_table.loc[test, effect] * sumtests[test] for test in sumtests])
        effect_val = contrast / (n_repl * 2**n_fact)  # Equation 6.22
        ss = contrast**2 / (n_repl * 2**n_fact)  # Equation 6.23
        res_dict[effect] = {"Effect": effect_val, "Sum of Squares": ss, "Degrees of Freedom": 1}

    # Evalutate total and error
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / ((2**n_fact) * n_repl)  # Equation 6.9
    ss_error = ss_total - sum([res_dict[effect]["Sum of Squares"] for effect in effects])
    res_dict["Error"] = {"Sum of Squares": ss_error}
    res_dict["Total"] = {"Sum of Squares": ss_total, "Degrees of Freedom": ((2**n_fact) * n_repl) - 1}

    for key in effects:
        res_dict[key]['%Contribution'] = 100 * res_dict[key]['Sum of Squares'] / res_dict["Total"]['Sum of Squares']

    # Error's DoF, Mean Square, and P-Values will only make sense if n_repl>1
    if n_repl > 1:
        res_dict["Error"]["Degrees of Freedom"] = (2**n_fact) * (n_repl - 1)  # DOF will fail with only one replica!!!

        for key in effects + ['Error']:
            res_dict[key]['Mean Square'] = res_dict[key]["Sum of Squares"] / res_dict[key]["Degrees of Freedom"]

        for key in effects:
            f0 = res_dict[key]['Mean Square'] / res_dict['Error']['Mean Square']
            pval = stats.f(res_dict[key]['Degrees of Freedom'], res_dict['Error']['Degrees of Freedom']).sf(f0)
            res_dict[key].update({"F0": f0, "P-Value": pval})

    # Print Table
    table = pd.DataFrame.from_dict(res_dict, orient='index')
    table = table.fillna("")
    table.index.name = "Source of Variation"
    return table
