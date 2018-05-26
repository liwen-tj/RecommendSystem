import numpy as np
import math
import pandas as pd
from apriori import Apriori
from time import time


def read_raw_data(file_path):
    """
    read data from 'tianchi_fresh_comp_train_user.csv'
    return all records of all users.
    """
    raw_data = pd.read_csv(file_path)
    # data = raw_data.loc[:, ['user_id', 'behavior_type', 'item_category']]
    data = raw_data.loc[:, ['user_id', 'item_id', 'item_category']]
    data = data.values

    users_id = [data[0][0]]
    users_item_id = []
    users_item_category = []
    one_user_item_id = []
    one_user_item_category = []
    for d in data:
        # A new user
        if d[0] != users_id[-1]:
            users_id.append(d[0])
            users_item_id.append(one_user_item_id)
            users_item_category.append(one_user_item_category)
            one_user_item_id = [d[1]]
            one_user_item_category = [d[2]]
        one_user_item_id.append(d[1])
        one_user_item_category.append(d[2])
    # !!
    users_item_id.append(one_user_item_id)
    users_item_category.append(one_user_item_category)

    users_item_id = remove_repeated_data(users_item_id)
    users_item_category = remove_repeated_data(users_item_category)

    return (users_item_id, users_item_category)


def remove_repeated_data(data):
    f_data = []
    for user in data:
        items = []
        for item in user:
            if item not in items:
                items.append(item)
        f_data.append(items)
    return np.array(f_data)


def cal_two(user1, user2):
    """
    compute similarity between two users
    """
    intersects = 0.0
    for u in user1:
        if u in user2:
            intersects += 1.0
    len_1, len_2 = user1.__len__(), user2.__len__()
    result = intersects / math.sqrt(len_1*len_2)
    return result


def gen_rules(uii, support=0.2, confidence=0.1, L=5):
    t0 = time()
    # generate associated rules
    print('generate associated rules....')
    apri = Apriori(uii, support, confidence, L)
    (items_id, allRules) = apri.genRules()
    print('Time took for generating rules:', time()-t0, 's')
    return (items_id, allRules)


def cal_imp(rules):
    t0 = time()
    sum_support = 0.0
    sum_confidence = 0.0
    for r in rules:
        sum_support += r[2]
        sum_confidence += r[3]

    r_len = rules.__len__()
    imp = [r_len*(r[2]/sum_support + r[3]/sum_confidence) for r in rules]

    print('Time took for calculating importace:', time()-t0, 's')

    return imp


def cal_interest(rules, r_imp, items_id, z_id):
    """
    calculate user's interest of item z.

    rules: (list) every elmement ==> [{left, right, support, confidence}]
    r_imp: (list) correspoding to rules.
    items_id:(list)
    z_id:(integer)
    """
    sum = 0.0
    items_id = set(items_id)
    r_len = r_imp.__len__()
    for i in range(r_len):
        if z_id in rules[i][1]:
            n = items_id & rules[i][0]
            if n.__len__() > 0:
                denominator = rules[i][1].__len__()*rules[i][0].__len__()
                sum += (n.__len__() * r_imp[i]) / denominator
    return sum


if __name__ == '__main__':
    pass
