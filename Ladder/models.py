from django.db import models

class Category(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.name)

class Problem(models.Model):
	problemId = models.CharField(max_length = 200, primary_key = True)
	contestId = models.CharField(max_length = 100)
	index = models.CharField(max_length = 100)
	problemName = models.CharField(max_length = 200)
	rating = models.IntegerField(default = 0)
	solvedCount = models.IntegerField(default = 0)

	category = models.ForeignKey(Category, on_delete=models.CASCADE)


	def __str__(self):
		return str(self.problemId)
