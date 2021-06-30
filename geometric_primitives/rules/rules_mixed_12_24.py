import numpy as np


PROBS_CONTACTS = np.array([4.0, 4.0, 2.0, 4.0, 4.0, 2.0, 2.0])
PROBS_CONTACTS /= np.sum(PROBS_CONTACTS)

RULE_CONTACTS = [
    # [0.5, 2.0] -> 4
    {
        'num_contacts': 1,
        'translations': [[0.5, 2.0], [-0.5, 2.0], [0.5, -2.0], [-0.5, -2.0]],
        'direction': 0
    },
    # [0.5, 1.0] -> 4
    {
        'num_contacts': 2,
        'translations': [[0.5, 1.0], [-0.5, 1.0], [0.5, -1.0], [-0.5, -1.0]],
        'direction': 0
    },
    # [0.5, 0.0] -> 2
    {
        'num_contacts': 2,
        'translations': [[0.5, 0.0], [-0.5, 0.0]],
        'direction': 0
    },
    # [1.5, 1.0] -> 4
    {
        'num_contacts': 1,
        'translations': [[1.5, 1.0], [-1.5, 1.0], [1.5, -1.0], [-1.5, -1.0]],
        'direction': 1
    },
    # [0.5, 1.0] -> 4
    {
        'num_contacts': 1,
        'translations': [[0.5, 1.0], [-0.5, 1.0], [0.5, -1.0], [-0.5, -1.0]],
        'direction': 1
    },
    # [1.5, 0.0] -> 2
    {
        'num_contacts': 2,
        'translations': [[1.5, 0.0], [-1.5, 0.0]],
        'direction': 1
    },
    # [0.5, 0.0] -> 2
    {
        'num_contacts': 2,
        'translations': [[0.5, 0.0], [-0.5, 0.0]],
        'direction': 1
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
