from cluster import ClusterUsers
import helper


def prepareData(file_path, n, K):
    uic_lists = helper.read_data(file_path)
    print('read 5000 users done...')
    print('clustering users...This might take a minute...')
    cu = ClusterUsers(uic_lists, n, K)
    (centroids, groups) = cu.cluster()
    return (uic_lists, centroids, groups)


def generateRules(uic_lists, groups, K, support, confidence):
    results = []
    for i in range(K):
        uic_group = [uic_lists[g] for g in groups[i]]
        print('--------------------- begin ---------------------- groups', i)
        print('number of group elements =', len(uic_group))
        (items_id, rules) = helper.gen_rules(uic_group, support, confidence)
        print('rules num =', len(rules))
        print('----------------------- end ----------------------\n\n\n')
        results.append((items_id, rules))
    return results


def evaluate(fp21, fp22, uic_lists, centroids, groups, rules):
    (data1, data2) = helper.read_test(fp21, fp22)
    classes = helper.assign_test(data1, uic_lists, centroids)   # 分发
    guess_likes = helper.recommend_item(classes, data1, rules)
    (precision, recall, fscore) = helper.scoring(data2, guess_likes)
    print('\n\n---------------------------------------------------')
    print('precision =', precision)
    print('recall =', recall)
    print('fscore =', fscore)


def main(fp1, fp21, fp22, n1, n2, K, support, confidence):
    (uic_lists, centroids, groups) = prepareData(fp1, n1, K)
    rules = generateRules(uic_lists, groups, K, support, confidence)
    evaluate(fp21, fp22, uic_lists, centroids, groups, rules)


if __name__ == '__main__':
    fp1 = './others/5000-100.csv'
    fp21 = './others/1427-1118-1208.csv'  # 21 days
    fp22 = './others/1427-1209-1218.csv'  # 10 days
    n1 = 5000
    n2 = 1427
    K = 50
    support = 0.3
    confidence = 0.45
    main(fp1, fp21, fp22, n1, n2, K, support, confidence)
