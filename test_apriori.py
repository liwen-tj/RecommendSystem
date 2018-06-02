from apriori import Apriori


transactions = [
    [1, 2, 5],
    [2, 4],
    [2, 3],
    [1, 2, 4],
    [1, 3],
    [2, 3],
    [1, 3],
    [1, 2, 3, 5],
    [1, 2, 3]
]

support = 0.2
confidence = 0.4
a = Apriori(transactions, support, confidence)
rules = a.genRules()
print('--------------------')
print(rules[0])
for r in rules[1]:
    print(r)
