import cluster
import helper
from time import time


def main(user_path, item_path, user_num=None, K=None, supp=0.5, conf=0.2, L=4):
    # --- 1 --- read data.
    print('reading data.This might take a few minutes...')
    t0 = time()
    # (uii, uic) ==> (users_item_id, users_item_category)
    (uii, uic) = helper.read_raw_data(user_path)
    t1 = time()
    print(t1-t0, 's')

    # --- 2 --- cluster users into different groups.
    print('clustering data...')
    cu = cluster.ClusterUsers(uic, user_num, K, max_iterations=5)
    (centroids, groups) = cu.cluster()
    t2 = time()
    print(t2-t1, 's')

    # --- 3 ---  generate associated rules & calculate importance of each rule
    for i in range(K):
        print(i, '--------------------------------------------------------')
        print('groups[i].__len__() =', groups[i].__len__())
        t3 = time()
        uii_group = [uii[g] for g in groups[i]]
        (items_id, rules) = helper.gen_rules(uii_group, supp, conf, L)
        r_imp = helper.cal_imp(rules)
        interest_scores = []
        for z in items_id:
            c = centroids[i]
            interest = helper.cal_interest(rules, r_imp, uii[c], z[0])
            if interest > 0.0:
                interest_scores.append(interest)
            print(interest)
        t4 = time()
        print(t4-t3, 's\n')


if __name__ == '__main__':
    main('4239users.csv', 'train_item.csv', 4239, 50)
