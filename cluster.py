import random
import helper


class ClusterUsers:
    def __init__(self, data, user_num, K=50, max_iterations=10, verbose=True):
        """
        data: all raw records of all users
        """
        self.data = data
        self.user_num = user_num
        assert self.user_num == self.data.__len__()  # # # # # # # # # # # #
        self.K = K
        self.max_iterations = max_iterations
        self.verbose = verbose

    def init_centroid(self):
        first_centroid = random.randint(0, self.user_num - 1)
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
            for g in groups:
                print('points_num =', g.__len__())
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
        if self.verbose is True:
            print('init centroids...')
        (centroids, groups) = self.init_centroid()
        for i in range(self.max_iterations):
            sims = self.cal_performace(centroids, groups)
            print("centroids = ", centroids)
            centroids = self.new_centroids(groups)
            if self.verbose is True:
                print('iteration', i, ', sims_before =', sims)
            sims = self.cal_performace(centroids, groups)
            groups = self.group_users(centroids)
            if self.verbose is True:
                print('iteration', i, ', sims_after =', sims)
            print('\n')
        return (centroids, groups)
