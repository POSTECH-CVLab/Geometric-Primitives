import numpy as np


PROBS_CONTACTS_1_2 = np.array([4.0, 2.0, 1.0])
PROBS_CONTACTS_1_2 /= np.sum(PROBS_CONTACTS_1_2)

RULE_CONTACTS_1_2 = [
    # [0.5, 0.5] -> 4
    {
        'num_contacts': 1,
        'translations': [[0.5, 0.5], [-0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]],
        'direction': 1
    },
    # [0, 1] -> 2
    {
        'num_contacts': 1,
        'translations': [[0, 1], [0, -1]],
        'direction': 0
    },
    # [0, 0] -> 1
    {
        'num_contacts': 2,
        'translations': [[0, 0]],
        'direction': 0
    }
]

LIST_RULES_1_2 = []
ind = 1
for rule in RULE_CONTACTS_1_2:
    cur_direction = rule['direction']
    cur_num_contacts = rule['num_contacts']

    for translation in rule['translations']:
        cur_rule = [ind, [cur_direction, translation, cur_num_contacts]]
        LIST_RULES_1_2.append(cur_rule)

        ind += 1
