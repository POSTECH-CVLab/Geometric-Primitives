from geometric_primitives.rules import rules_2_4 as rules_2_4
from geometric_primitives.rules import rules_2_2 as rules_2_2
from geometric_primitives.rules import rules_1_2 as rules_1_2
from geometric_primitives.rules import rules_mixed_24_12 as rules_mixed_24_12


PROBS_CONTACTS_2_4 = rules_2_4.PROBS_CONTACTS_2_4
RULE_CONTACTS_2_4 = rules_2_4.RULE_CONTACTS_2_4
LIST_RULES_2_4 = rules_2_4.LIST_RULES_2_4

PROBS_CONTACTS_2_2 = rules_2_2.PROBS_CONTACTS_2_2
RULE_CONTACTS_2_2 = rules_2_2.RULE_CONTACTS_2_2
LIST_RULES_2_2 = rules_2_2.LIST_RULES_2_2

PROBS_CONTACTS_1_2 = rules_1_2.PROBS_CONTACTS_1_2
RULE_CONTACTS_1_2 = rules_1_2.RULE_CONTACTS_1_2
LIST_RULES_1_2 = rules_1_2.LIST_RULES_1_2

PROBS_CONTACTS_24_12 = rules_mixed_24_12.PROBS_CONTACTS_24_12
RULE_CONTACTS_24_12 = rules_mixed_24_12.RULE_CONTACTS_24_12
LIST_RULES_24_12 = rules_mixed_24_12.LIST_RULES_24_12

ALL_TYPES = [
    '0',
    '1',
    '2',
    '3',
]

ALL_PROBS = [
    PROBS_CONTACTS_2_4, # 0
    PROBS_CONTACTS_2_2, # 1
    PROBS_CONTACTS_1_2, # 2
    PROBS_CONTACTS_24_12, # 3
]
ALL_RULES = [
    RULE_CONTACTS_2_4,
    RULE_CONTACTS_2_2,
    RULE_CONTACTS_1_2,
    RULE_CONTACTS_24_12,
]
ALL_LISTS = [
    LIST_RULES_2_4,
    LIST_RULES_2_2,
    LIST_RULES_1_2,
    LIST_RULES_24_12,
]
