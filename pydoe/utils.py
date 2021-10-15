import pandas as pd
import itertools

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def contrast_constants_table(k):
    """Generate the table of contrast constants for the 2^k factorial design.
    The table is returned as a DataFrame, to be compared, e.g., with Tables 6.3 (k=3), 6.11 (k=4), 6.17 (k=5).
    """

    if k > len(ALPHABET):
        raise NotImplementedError(f"The number of factor is bigger than the implemented limit of {len(ALPHABET)}")

    main_effects = ALPHABET[:k]
    cc_dict = {}
    cc_dict['(1)'] = {effect: -1 for effect in main_effects}

    for comb in itertools.combinations_with_replacement(main_effects.lower(), k):
        comb = sorted(set(comb))
        k_comb = "".join(comb)
        cc_dict[k_comb] = {effect: [-1, +1][int(effect.lower() in comb)] for effect in main_effects}

    cc = pd.DataFrame.from_dict(cc_dict, orient='index')

    for effect in itertools.combinations_with_replacement(main_effects, k):
        effect = sorted(set(effect))
        if len(effect) == 1:  # Already in table
            continue
        k_effect = "".join(effect)
        cc[k_effect] = cc[effect].prod(axis=1)

    # Sort indexes/columns like the convention of the book: Tables 6.3 (k=3), 6.11 (k=4), 6.17 (k=5)
    cc = cc.sort_values(list(main_effects)[::-1])
    indexes = list(cc.index)[1:]
    cc = cc.reindex(columns=[x.upper() for x in indexes])

    return cc
