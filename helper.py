import math
from apriori import Apriori
from time import time


def read_data(file_path):
    uid_last = None
    uic_lists = []
    with open(file_path) as lines:
        uic = []
        for line in lines:
            [user_id, item_category] = line[:-1].split(',')
            item_category = int(item_category)
            if uid_last is not None:  # 从文件第二行开始
                if user_id == uid_last:  # 同一个用户
                    uic.append(item_category)
                else:  # 换新的用户了
                    uid_last = user_id
                    a = sorted(uic)
                    uic_lists.append(a)
                    uic = [item_category]
            else:  # 文件第一行
                uid_last = user_id
                uic = [item_category]

        a = sorted(uic)
        uic_lists.append(a)

    return uic_lists


def read_test(file_path1, file_path2):
    data1 = read_data(file_path1)
    data2 = read_data(file_path2)
    return (data1, data2)


def assign_test(data1, uic_lists, centroids):
    classes = []
    for d in data1:
        sims = [cal_two(d, uic_lists[c]) for c in centroids]
        classes.append(sims.index(max(sims)))
    return classes


def cal_two(user1, user2):
    """
    compute similarity between two users
    """
    intersects = 0.0
    len_1, len_2 = user1.__len__(), user2.__len__()
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if user1[i] > user2[j]:
            j += 1
        elif user1[i] < user2[j]:
            i += 1
        else:
            intersects += 1.0
            i += 1
            j += 1

    result = intersects / math.sqrt(len_1*len_2)
    return result


def gen_rules(uii, support, confidence):
    t0 = time()
    # generate associated rules
    print('generate associated rules....')
    apri = Apriori(uii, support, confidence)
    (items_id, allRules) = apri.genRules()
    print('Time took for generating rules:', time()-t0, 's')
    # items_id 频繁一项集
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

    rules: (list) every elmement ==> [{left}, {right}, support, confidence]
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
                denominator = rules[i][1].__len__() * rules[i][0].__len__()
                sum += (n.__len__() * r_imp[i]) / denominator
    return sum


def recommend_item(classes, data1, rules):
    importance = [cal_imp(x[1]) for x in rules]

    likes = []
    i = 0
    for user in classes:
        interest_item_cate = set()
        (L1s, s_rules) = rules[user]
        for ci in L1s:
            score = cal_interest(s_rules, importance[user], data1[i], ci)
            if score > 0.0:
                interest_item_cate.add(ci)
        i += 1
        print('user', user, 'interested item num =', len(interest_item_cate))
        likes.append(interest_item_cate)
    return likes


def scoring(data2, guess_likes):
    l_inter, l_reference, l_prediction = 0.0, 0.0, 0.0
    i = 0
    for d_ in data2:
        d = set(d_)
        len_inter = len(d & guess_likes[i])
        len_reference = len(d)
        len_prediction = len(guess_likes[i])
        i += 1
        l_inter += len_inter
        l_reference += len_reference
        l_prediction += len_prediction

        print('for this user....')
        print('len_inter =', len_inter)
        print('len_reference =', len_reference)
        print('len_prediction =', len_prediction)
        print('\n\n\n')

    precision = l_inter / l_prediction
    recall = l_inter / l_reference
    fscore = 2 * precision * recall / (precision + recall)
    return (precision, recall, fscore)


if __name__ == '__main__':
    uic_train = read_data('./others/5000-100.csv')
    print(len(uic_train))
