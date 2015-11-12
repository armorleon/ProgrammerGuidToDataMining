__author__ = 'duoduo'

from math import sqrt
from math import pow

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

def manhattan(rating1, rating2):
    #calculate manhattan distance

    commonRating = False
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            commonRating = True
    if commonRating:
        return distance
    else:
        return -1

def computeNearestNeighbor(username, users):
    """creates a sorted list of users based on their distance to username"""
    distances = []
    for u in users:
        if u != username:
            distance = manhattan(users[username], users[u])
            distances.append((distance, u))
    distances.sort()
    return distances

def recommend(username, users):
    """Give list of recommendations"""
    nearest = computeNearestNeighbor(username, users)[0][1]
    #return nearest

    recommendations = []

     # now find bands neighbor rated that user didn't
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if artist not in userRatings:
            recommendations.append((artist, neighborRatings[artist]))

    return sorted(recommendations, key = lambda x : x[1], reverse = True)






def minkowski(rating1, rating2, r):
    """Computes the Minkowski distan"""
    commonRating = False
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += pow(abs(rating1[key] - rating2[key]), r)
            commonRating = True
    if commonRating:
        print "distance %d\n" % distance
        return pow(distance, 1/r)
    else:
        return 0


print manhattan(users["Chan"], users["Jordyn"])

print computeNearestNeighbor("Sam", users)

print recommend("Sam", users)
print( recommend('Hailey', users))


print minkowski(users["Hailey"], users["Sam"], 2)


def pearson(rating1, rating2):
    sumX = 0
    sumY = 0
    sumXY = 0
    sumX_sq = 0
    sumY_sq = 0
    common = False

    n = 0
    for x in rating1:
        if x in rating2:
            n += 1
            sumX += rating1[x]
            sumY += rating2[x]
            sumXY += rating1[x] * rating2[x]
            sumX_sq += rating1[x]**2
            sumY_sq += rating2[x]**2
            common = True

    if n == 0:
        return 0

    r = 0
    if common:
        a = sumXY - (sumX * sumY/n)
        b = sqrt(sumX_sq - (sumX**2)/n) * sqrt(sumY_sq - (sumY**2)/n)
        r = a/b

    return r

print pearson(users["Angelica"], users["Bill"])
print pearson(users["Angelica"], users["Hailey"])
print pearson(users["Angelica"], users["Jordyn"])