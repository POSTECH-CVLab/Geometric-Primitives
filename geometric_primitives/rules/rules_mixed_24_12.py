import numpy as np


PROBS_CONTACTS = np.array([4.0, 4.0, 4.0, 4.0, 6.0])
PROBS_CONTACTS /= np.sum(PROBS_CONTACTS)

RULE_CONTACTS = [
    # [1, 1.5] -> 4
    {
        'num_contacts': 1,
        'translations': [[1, 1.5], [1, -1.5], [-1, 1.5], [-1, -1.5]],
        'direction': 1
    },
    # [1, 0.5] -> 4
    {
        'num_contacts': 1,
        'translations': [[1, 0.5], [1, -0.5], [-1, 0.5], [-1, -0.5]],
        'direction': 1
    },
    # [0, 1.5], [0, 0.5] -> 4
    {
        'num_contacts': 2,
        'translations': [[0, 1.5], [0, -1.5], [0, 0.5], [0, -0.5]],
        'direction': 1
    },
    # [0.5, 2] -> 4
    {
        'num_contacts': 1,
        'translations': [[0.5, 2], [0.5, -2], [-0.5, 2], [-0.5, -2]],
        'direction': 0
    },
    # [0.5, 1], [0.5, 0] -> 6
    {
        'num_contacts': 2,
        'translations': [[0.5, 1], [0.5, -1], [-0.5, 1], [-0.5, -1], [0.5, 0], [-0.5, 0]],
        'direction': 0
    },
]

LIST_RULES = []
ind = 1
for rule in RULE_CONTACTS:
    cur_direction = rule['direction']
    cur_num_contacts = rule['num_contacts']

    for translation in rule['translations']:
        cur_rule = [ind, [cur_direction, translation, cur_num_contacts]]
        LIST_RULES.append(cur_rule)

        ind += 1
