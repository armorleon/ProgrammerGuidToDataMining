import codecs
from math import sqrt
import pprint


class movie:

    def __init__(self, filename, k=2, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.users = []
        self.data = {}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson

        self.loadMovieDB(filename)

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def loadMovieDB(self, path):
        self.data = {}
        i = 0
        f = codecs.open("./Movie_Ratings.csv", 'r', 'utf8')
        for line in f:
            i += 1
            if i == 1:
                self.users = line.split(",")
                for u in self.users[1:]:
                    user = u.strip('"')
                    self.data[user] = {}

            else:
                fields = line.split(",")
                movie = fields[0].strip('"')
                for j in range(1, len(fields)):
                    field = fields[j].strip()
                    if field:
                        rating = int(field)
                        user = self.users[j].strip('"')
                        self.data[user][movie] = rating
        pprint.pprint(self.data)

    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to username"""
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances


    def recommend(self, user):
       """Give list of recommendations"""
       recommendations = {}
       # first get list of users  ordered by nearness
       nearest = self.computeNearestNeighbor(user)
       #
       # now get the ratings for the user
       #
       userRatings = self.data[user]
       #
       # determine the total distance
       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          # compute slice of pie
          weight = nearest[i][1] / totalDistance
          # get the name of the person
          name = nearest[i][0]
          # get the ratings for this person
          neighborRatings = self.data[name]

          # get the name of the person
          # now find bands neighbor rated that user didn't
          for movie in neighborRatings:
             if not movie in userRatings:
                if movie not in recommendations:
                   recommendations[movie] = (neighborRatings[movie]
                                              * weight)
                else:
                   recommendations[movie] = (recommendations[movie]
                                              + neighborRatings[movie]
                                              * weight)
       # now make list from dictionary
       recommendations = list(recommendations.items())
       # finally sort and return
       recommendations.sort(key=lambda movieTuple: movieTuple[1],
                            reverse = True)
       # Return the first n items
       return recommendations[:self.n]

r = movie("./")

print "recommened movies are %s", r.recommend('vanessa')
print "recommened movies are %s", r.recommend('brian')
print "recommened movies are %s", r.recommend('Katherine')