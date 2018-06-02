import helper


class ClusterUsers:
    def __init__(self, data, user_num, K=50, max_iterations=3, verbose=True):
        self.data = data
        self.user_num = user_num
        self.K = K
        self.max_iterations = max_iterations
        self.verbose = verbose

    def init_centroid(self):
        # first_centroid = random.randint(0, self.user_num - 1)
        first_centroid = 10
        centroids = [first_centroid]
        max_sims_with_centroids = [[0.0, 0] for _ in range(self.user_num)]
        while centroids.__len__() < self.K:
            candidate = -1
            min_similar = 1.0
            centroid_1_value = self.data[centroids[-1]]
            for i in range(self.user_num):
                s = helper.cal_two(self.data[i], centroid_1_value)
                if s > max_sims_with_centroids[i][0]:
                    max_sims_with_centroids[i][0] = s
                    max_sims_with_centroids[i][1] = centroids.__len__() - 1
                if max_sims_with_centroids[i][0] < min_similar:
                    min_similar = max_sims_with_centroids[i][0]
                    candidate = i
            centroids.append(candidate)
        # init centroids done!!
        # calculate init groups
        groups = [[] for _ in range(self.K)]
        centroid_1_value = self.data[centroids[-1]]
        for i in range(self.user_num):
            s = helper.cal_two(self.data[i], centroid_1_value)
            if s > max_sims_with_centroids[i][0]:
                groups[self.K-1].append(i)
            else:
                groups[max_sims_with_centroids[i][1]].append(i)

        return (centroids, groups)

    def group_users(self, centroids):
        # group all users into different centroids
        groups = [[] for _ in range(self.K)]
        for i in range(self.user_num):
            di = self.data[i]
            sims = [helper.cal_two(di, self.data[c]) for c in centroids]
            groups[sims.index(max(sims))].append(i)
        if self.verbose is True:
            for x in range(self.K):
                print('centroid =', centroids[x], ' points_num =', groups[x].__len__())
        return groups

    def cal_performace(self, centroids, groups):
        sims = 0.0
        for i in range(self.K):
            one_class_points = groups[i]
            for j in one_class_points:
                sims += helper.cal_two(self.data[centroids[i]], self.data[j])
        return sims

    def new_centroids(self, groups):
        # define new centroids
        centroids = []
        for g in groups:
            all_users_items = {}  # items of all users in single group
            # add up user_items
            for user in g:
                one_user_items = self.data[user]
                for oui in one_user_items:
                    if oui in all_users_items:
                        all_users_items[oui] += 1
                    else:
                        all_users_items[oui] = 1
            score = 0.0
            candidate_user = -1
            for user in g:
                curr_score = 0.0
                one_user_items = self.data[user]
                for oui in one_user_items:
                    curr_score += all_users_items[oui]
                curr_score = curr_score / (one_user_items.__len__()+1.0)
                if curr_score > score:
                    score = curr_score
                    candidate_user = user
            centroids.append(candidate_user)

        return centroids

    def cluster(self):
        # centroids = [1924, 3205, 2821, 4229, 4240, 3859, 404, 2815, 410, 284, 1566, 3744, 4890, 807, 3113, 1452, 4270, 1663, 2094, 947, 1973, 1206, 2233, 2745, 2235, 2748, 1341, 189, 1339, 833, 3012, 1605, 836, 1095, 455, 2764, 1997, 2648, 100, 3546, 2527, 3297, 4581, 3052, 622, 3055, 2552, 2170, 2684, 3581]
        centroids = [3878, 3205, 4924, 4229, 4240, 3859, 404, 2815, 410, 284, 1566, 3744, 4890, 807, 3113, 1452, 4270, 1663, 2094, 947, 1973, 1206, 2233, 2745, 2235, 2748, 1341, 189, 1339, 833, 3012, 1605, 836, 1095, 455, 2764, 1997, 2648, 1410, 3546, 2527, 3297, 4581, 3052, 622, 3055, 2552, 2170, 1924, 999]
        for _ in range(self.max_iterations):
            groups = self.group_users(centroids)
            sims = self.cal_performace(centroids, groups)
            print('sims = ', sims)
            print('----------------------------------------------\n\n')
            centroids = self.new_centroids(groups)
        groups = self.group_users(centroids)
        return (centroids, groups)


if __name__ == '__main__':
    pass
