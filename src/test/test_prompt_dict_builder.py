"""
Tests the history dictionary builder
"""
from collections import defaultdict
from cmdwerk.commands.prompt_cmd import build_history_data


def stringuify_rec(indent, so_far, a_dict):
    """Recursive call transform dicts of dicts into strings"""
    filler = indent * ' '
    for key in sorted(a_dict.keys()):
        value = a_dict[key]
        so_far.append(filler + key)
        if isinstance(value, dict):
            stringuify_rec(indent+1, so_far, value)
        elif isinstance(value, set):
            for elem in sorted(value):
                so_far.append(filler + ' ' + elem)


def stringuify(a_dict):
    """Transform dicts of dicts into strings"""
    so_far = []
    stringuify_rec(0, so_far, a_dict)
    return '\n'.join(so_far)


def report_comp_details(expected, current):
    """Cleaner version of comparison with large strings"""
    print('\n-- Expected --\n')
    print(expected)
    print('\n-- Current --\n')
    print(current)


def test_prompt_2_levels():
    """Tests the case with history producing two level dicts"""
    expected = defaultdict(set, {'git': {'log', 'status', 'checkout'},
                                 'git|_|checkout': {'dev', 'master'}})
    data = build_history_data(['git status', 'git log', 'git checkout master', 'git checkout dev'])
    expected_str = stringuify(expected)
    data_str = stringuify(data)
    report_comp_details(expected_str, data_str)
    assert expected_str == data_str


def test_prompt_3_levels():
    """Tests the case with history producing three level dicts"""
    init_set = {
        'git': {'commit', 'status'},
        'git|_|commit': {'src'},
        'git|_|commit|_|src': {'-m'},
        'git|_|commit|_|src|_|-m': {'This is a commit', 'This is another commit'}
    }
    expected = defaultdict(set, init_set)
    data = build_history_data(['git status',
                               "git commit src -m 'This is a commit'",
                               "git commit src -m 'This is another commit'",
                               ])
    expected_str = stringuify(expected)
    data_str = stringuify(data)
    report_comp_details(expected_str, data_str)
    assert expected_str == data_str

