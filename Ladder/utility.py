import json,requests
import random
from . models import Problem, Category

maxm = 1000000

class CFQuery :
    def __init__(self):
        print("Welcome to codeforces!")

    def allProblemStat(self):
        urlAllProblems = "http://codeforces.com/api/problemset.problems"
        res = requests.get(urlAllProblems)
        data = json.loads(res.text)
        #print(data)
        N = len(data["result"]["problems"])
        print('problem count : ', N)
        for i in range(1):
            contestId = data["result"]["problems"][i]["contestId"]
            index = data["result"]["problems"][i]["index"]
            problemId = str(contestId) + str(index)
            problemName = data["result"]["problems"][i]["name"]
            solvedCount = int(data["result"]["problemStatistics"][i]["solvedCount"])
            tags = data["result"]["problems"][i]["tags"]
            category_name = self.AssignCategory(tags)
            rating = 0
            try:
                rating = int(data["result"]["problems"][i]['rating'])
            except:
                rating = 0

            if(len(Problem.objects.filter(problemId=problemId)) == 0):
                category = Category.objects.get(name=category_name)
                problem = Problem(problemId=problemId, contestId=contestId, index=index,problemName=problemName,rating=rating,solvedCount=solvedCount, category=category)
                problem.save()
                #c = Categories.objects.get(category=category)
                #c.problem.add(problem)
            else:
                problem = Problem.objects.get(problemId=problemId)
                problem.solvedCount=solvedCount
                problem.rating=rating
        print(str(N) + " Problem Processed!")

    def AssignCategory(self, tags):
        dict = {'Dynamic-Programming' : ['dp', 'fft',],
                'Graphs' : ['graphs', 'trees', 'dfs and similar', 'graph matchings', 'flows', 'shortest paths', 'graph matchings', ],
                'Greedy' : ['greedy', ],
                'Strings' : ['strings', 'string suffix structures'],
                'Bit-Manipulation' : ['bitmasks'],
                'Algorithms' : ['chinese remainder theorem', 'constructive algorithms', 'number theory'],
                'Math' : ['combinatorics', 'probabilities', 'math', 'geometry', 'matrices',],
                'Data-Structures' : ['dsu', 'data structures', 'hashing'],
                'Implementation' : ['implementation'],
                }

        for key in dict:
            for tag in tags:
                if tag in dict[key]:
                    return key

        return 'Miscellaneous'

    def UserSubmissions(self, cfHandle):

        urlUserRating = "http://codeforces.com/api/user.info?handles=" + cfHandle
        query = requests.get(urlUserRating)
        ratingdata = json.loads(query.text)

        try :
            rating = int(ratingdata['result'][0]['rating'])
        except :
            rating = 800

        urlUserStat ="http://codeforces.com/api/user.status?handle="+ cfHandle + "&from=1&count=" + str(maxm)
        res = requests.get(urlUserStat)
        data = json.loads(res.text)

        solvedProblemsByUser = []
        stats = {'Dynamic-Programming' : [0,0,0], 'Graphs' : [0,0,0], 'Greedy' : [0,0,0], 'Strings' : [0,0,0], 'Bit-Manipulation' : [0,0,0], 'Algorithms' : [0,0,0], 'Math' : [0,0,0], 'Data-Structures' : [0,0,0], 'Implementation' : [0,0,0], 'Miscellaneous' : [0,0,0],}
        #totalstats = {'Dynamic-Programming' : 0, 'Graphs' : 0, 'Greedy' : 0, 'Strings' : 0, 'Bit-Manipulation' : 0, 'Algorithms' : 0, 'Math' : 0, 'Data-Structures' : 0, 'Implementation' : 0, 'Miscellaneous' : 0,}

        Nlength = len(data['result'])
        print(Nlength)

        for submission in data['result']:
            contestId = str(submission['problem']['contestId'])
            index = str(submission['problem']['index'])
            problemId = contestId + index
            name = str(submission['problem']['name'])
            tags = submission['problem']['tags']
            category_name = self.AssignCategory(tags)
            #if rating in submission['problem']:
            #    rating = int(submission['problem']['rating'])
            #if(len(Problem.objects.filter(problemId=problemId)) == 0):
                #category = Category.objects.get(name = category_name)
                #problem = Problem(problemId=problemId, contestId=contestId, index=index,problemName=problemName,rating=rating,solvedCount=solvedCount, category=category)
                #problem.save()
                #category = AssignCategory(tags)
                #c = Categories.objects.get(category=category)
                #c.problem.add(problem)

            if(str(submission['verdict'])=='OK'):
                if (problemId not in solvedProblemsByUser):
                    solvedProblemsByUser.append(problemId)
                    stats[category_name][0] = stats[category_name][0] + 1
                    stats[category_name][1] = stats[category_name][1] + 1

            else:
                stats[category_name][1] = stats[category_name][1] + 1

        #accuracystats = dict()

        for category in stats:
            if stats[category][1] > 0 :
                stats[category][2] = round(stats[category][0]/stats[category][1], 2)    #rounding of value to 2 decimal values
            else:
                stats[category][2] = 0

        print('Utility Stats : ', stats)
        #print('Utility accuracystats : ', accuracystats)


        return solvedProblemsByUser, stats, rating


    def LadderProblem(self, cfHandle, category_name):
        urlUserRating = "http://codeforces.com/api/user.info?handles=" + cfHandle
        query = requests.get(urlUserRating)
        data = json.loads(query.text)

        try :
            rating = int(data['result'][0]['rating'])
        except :
            rating = 800

        solvedProblemsByUser, stats, rating = self.UserSubmissions(cfHandle=cfHandle)
        category = Category.objects.get(name = category_name)
        #problems = category.problem_set(rating>Rating+100).order_by('rating','solvedCount')[:5]
        problems = Problem.objects.filter(category=category, rating__gt=rating+100,).order_by('rating','solvedCount')[:5]
        print(str(len(problems)) + "Problems Fetched")
        print(problems)


        #problems = problems[:10:2]
        #print(problems)

        return problems, stats[category_name], rating
