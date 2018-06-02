import copy


def powerSetsBinary(items):
    """ calculate subset (items should be list) """
    results = []
    # generate all combination of N items
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(1, 2**N-1):
        left_items = set()
        right_items = set()
        for j in range(N):
            # test jth bit of integer i
            if(i >> j) % 2 == 1:
                left_items.add(items[j])
            else:
                right_items.add(items[j])
        results.append([left_items, right_items])
    return results


class Apriori:
    def __init__(self, transactions, support, confidence, L=2):
        """
        transactions: all item_ids of all users in single group.(list of list)
        support: minimal support value(0~1)
        confidence: minimal confidence value(0~1)
        L: maximal number
        """
        self.transactions = transactions
        self.t_len = self.transactions.__len__()
        self.support = int(support * self.t_len + 0.5)
        self.support_for_L1 = (int(0.15 * self.t_len + 0.5))
        self.confidence = confidence
        self.L = L

    def _getL1(self):
        """ get L1 frequent set. """
        freq_items = []
        L1_candidates = {}
        for t in self.transactions:
            for item in t:
                if item in L1_candidates:
                    L1_candidates[item] += 1
                else:
                    L1_candidates[item] = 1
        L1 = []
        for c in L1_candidates:
            if L1_candidates[c] >= self.support_for_L1:
                L1.append([{c}, L1_candidates[c]])
                freq_items.append(c)
        return (freq_items, L1)

    def _getLn1(self, Ln):
        """ get L(n+1) frequent sets from L(n) """
        def intersects(set1, set2):
            diff = 0
            diff_element = None
            for s in set1:
                if s not in set2:
                    diff_element = s
                    diff += 1
                if diff >= 2:
                    return None
            assert diff == 1
            set_new = copy.deepcopy(set2)
            set_new.add(diff_element)
            return set_new

        def checkRepeat(L, inse):
            for t in L:
                if inse == t[0]:
                    return True
            return False

        def countNum(inse):
            n = 0
            for t in self.transactions:
                flag = 1
                for i in inse:
                    if i not in t:
                        flag = 0
                        break
                n += flag
            return n

        Ln1 = []
        len = Ln.__len__()
        for i in range(len-1):
            for j in range(i+1, len):
                inse = intersects(Ln[i][0], Ln[j][0])
                if inse is not None:
                    repeated = checkRepeat(Ln1, inse)
                    if not repeated:
                        counter = countNum(inse)
                        if counter >= self.support:
                            Ln1.append([inse, counter])

        return Ln1

    def getFrequentSubset(self):
        (freq_items, Ln) = self._getL1()
        print('L - 1 number =', Ln.__len__())
        frequent_sets = Ln
        for i in range(1, self.L):
            Ln = self._getLn1(Ln)
            if Ln.__len__() == 0:
                break
            frequent_sets += Ln
            print('L -', i+1, 'number =', Ln.__len__())
        return (freq_items, frequent_sets)

    def genRules(self):
        """ generate association rules """
        (freq_items, frequent_sets) = self.getFrequentSubset()

        def gen_rules(fs):
            # generate association rules for single frequent set
            rules = []
            fs0 = list(fs[0])
            sets = powerSetsBinary(fs0)
            for s in sets:
                left_num = 0
                for fss in frequent_sets:
                    if fss[0] == s[0]:
                        left_num = fss[1]
                if left_num > 0:
                    confidence = fs[1] / left_num
                else:
                    confidence = 0.0
                if confidence > self.confidence:
                    rules.append([s[0], s[1], fs[1]/self.t_len, confidence])

            return rules

        allRules = []
        for fs in frequent_sets:
            if fs[0].__len__() > 1:
                rules = gen_rules(fs)
                allRules += rules

        return (freq_items, allRules)
