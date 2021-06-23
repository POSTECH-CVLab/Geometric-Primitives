import numpy as np


PROBS_CONTACTS_24_12 = np.array([4.0, 4.0, 4.0, 4.0, 6.0])
PROBS_CONTACTS_24_12 /= np.sum(PROBS_CONTACTS_24_12)

RULE_CONTACTS_24_12 = [
    # [1, 1.5] -> 4
    {
        'num_contacts': 1,
        'translations': [[1, 1.5], [1, -1.5], [-1, 1.5], [-1, -1.5]],
        'direction': 0
    },
    # [1, 0.5] -> 4
    {
        'num_contacts': 1,
        'translations': [[1, 0.5], [1, -0.5], [-1, 0.5], [-1, -0.5]],
        'direction': 0
    },
    # [0, 1.5], [0, 0.5] -> 4
    {
        'num_contacts': 2,
        'translations': [[0, 1.5], [0, -1.5], [0, 0.5], [0, -0.5]],
        'direction': 0
    },
    # [0.5, 2] -> 4
    {
        'num_contacts': 1,
        'translations': [[0.5, 2], [0.5, -2], [-0.5, 2], [-0.5, -2]],
        'direction': 1
    },
    # [0.5, 1], [0.5, 0] -> 6
    {
        'num_contacts': 2,
        'translations': [[0.5, 1], [0.5, -1], [-0.5, 1], [-0.5, -1], [0.5, 0], [-0.5, 0]],
        'direction': 1
    },
]

LIST_RULES_24_12 = []
ind = 0
for rule in RULE_CONTACTS_24_12:
    cur_direction = rule['direction']
    cur_num_contacts = rule['num_contacts']

    for translation in rule['translations']:
        cur_rule = [ind, [cur_direction, translation, cur_num_contacts]]
        LIST_RULES_24_12.append(cur_rule)

        ind += 1
