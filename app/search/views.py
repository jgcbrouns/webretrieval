 # howdy/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Papers
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core import serializers
import sys
from repository import *
from authentication import *
from vsr import *
import ast

# Create your views here.
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html')

def topics_view(request):
	return render(request, 'vis.html')


def author_view(request):
	if request.method == 'GET':
		authorId = request.GET.get('id')
		db = get_db()
		topicInfo = get_author_topic_information(db, int(authorId))
		coauthors = topicInfo['workingtimes_with_coauthor']
		coauthors = coauthors[1:-1]
		coauthorsDict = ast.literal_eval(coauthors)

		coauthorsListWithNames = []
		for coAuthor in coauthorsDict:
			coAuthorId = int(coAuthor)
			coAuthorCOOPTimes = int(coauthorsDict[coAuthor])

			coauthorQuery = get_author(db, int(coAuthorId))
			coauthorName = coauthorQuery['name']

			coauthorDict = {'name': coauthorName, 'times': coAuthorCOOPTimes}

			coauthorsListWithNames.append(coauthorDict)

		authorQuery = get_author(db, int(authorId))
	else:
		authorId = null
	
	return render(request, 'author.html', {'author': authorQuery, 'topicInfo': topicInfo, 'id': authorId, 'coauthors': coauthorsListWithNames})

def page_view(request):
	if request.method == 'GET':
		documentId = request.GET.get('id')

		topicsList = []
		metadataList = []

		db = get_db()

		keywords = get_keywords_for_paper(db, documentId)
		keywords = keywords['keywords']


		cursor = get_topics_for_document(db, documentId)
		for topic in cursor:
			if topic != 'documentId' and topic != '_id' and topic != 'main topic' and topic != 'second topic' and topic != 'third topic':
				topicName = topic
				topicValue = cursor[topic]

				topicDict = {'topic': topicName, 'value': topicValue}

				topicsList.append(topicDict)

		paper = get_paper(db, int(documentId))
		# get_authors_for_paper(db, int(documentId))
		authors = get_authors_for_paper(db, int(documentId))

		topicsList.sort(key=lambda item: (item['value']),reverse=True)

		return render(request, 'page.html', {'topics': topicsList, 'metadata': paper, 'authors': authors, 'keywords' : keywords},)

def get_papers_from_list(db, ids):
	cursor = db.pages.find({'documentId': {'$in': ids}});
	return cursor


def getContent(request, **kwargs):
    if request.method == 'POST':
		query = request.POST.get('query')
		response_data = {}

		# post = Post(text=post_text, author=request.user)
		# post.save()
		# Do query
		db = get_db()
		print >>sys.stderr, 'hi:'

		if query:
			try:
				query = str(query)
				print >>sys.stderr, 'asdf:'
			except ValueError:
				query = None
				papers = None

				#return empty data
				response_data['papers'] = json.dumps([])
			
			if query:
				try:
					# papers = Papers.objects.filter(year=query).only("year", "title", "id")

					ids = final(query, 100)
					papers = get_papers_from_list(db, ids)

					items=[]
					items_with_pagerank=[]

					for paper in papers:						
						year = paper['year']
						title = paper['title']
						id = paper['documentId']
						# authors = get_authors_for_paper(db, int(id))
						try:
							cursor = get_pagerank(db, id)
							if cursor:
								pagerank = cursor['PageRank']
								jsonInstance = {'year': year,'title': title,'pagerank': pagerank, 'id': id}
								items_with_pagerank.append(jsonInstance)
							else:
								jsonInstance = {'year': year,'title': title, 'id': id}
								items.append(jsonInstance)
						except ObjectDoesNotExist:
							null

					#sort on pagerank
					#items.sort(key=lambda item: (item['points'], item['time']))
					items_with_pagerank.sort(key=lambda item: (item['pagerank']),reverse=True)

					final_list = items_with_pagerank + items
					jsonOutput = json.dumps(final_list)

					response_data['papers'] = jsonOutput
				except ObjectDoesNotExist:
					null

		response_data['result'] = 'data retrieval successful!'
		response_data['query'] = query

		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
        )
    else:
        return HttpResponse(
			json.dumps({"nothing to see": "this isn't happening"}),
			content_type="application/json"
        )

# def getContent(request, **kwargs):
#     if request.method == 'POST':
# 		query = request.POST.get('query')
# 		response_data = {}

# 		# post = Post(text=post_text, author=request.user)
# 		# post.save()
# 		# Do query
# 		db = get_db()
# 		if query:
# 			try:
# 				query = int(query)
# 			except ValueError:
# 				query = None
# 				papers = None

# 				#return empty data
# 				response_data['papers'] = json.dumps([])
			
# 			if query:
# 				try:
# 					# papers = Papers.objects.filter(year=query).only("year", "title", "id")

# 					ids = final(query, 10)
# 					papers = get_papers_from_list(db, ids)

# 					# for id in ids:
# 					# 	paper = get_paper(db, id)

# 					items=[]
# 					items_with_pagerank=[]

    
# 					for paper in papers:
# 						year = paper.year
# 						title = paper.title
# 						id = paper.id
# 						try:
# 							cursor = get_pagerank(db, id)
# 							if cursor:
# 								pagerank = cursor['PageRank']
# 								jsonInstance = {'year': year,'title': title,'pagerank': pagerank, 'id': id}
# 								items_with_pagerank.append(jsonInstance)
# 							else:
# 								jsonInstance = {'year': year,'title': title, 'id': id}
# 								items.append(jsonInstance)
# 						except ObjectDoesNotExist:
# 							null

# 					#sort on pagerank
# 					#items.sort(key=lambda item: (item['points'], item['time']))
# 					items_with_pagerank.sort(key=lambda item: (item['pagerank']),reverse=True)

# 					final_list = items_with_pagerank + items
# 					jsonOutput = json.dumps(final_list)

# 					response_data['papers'] = jsonOutput
# 				except ObjectDoesNotExist:
# 					null

# 		response_data['result'] = 'data retrieval successful!'
# 		response_data['query'] = query

# 		return HttpResponse(
# 			json.dumps(response_data),
# 			content_type="application/json"
#         )
#     else:
#         return HttpResponse(
# 			json.dumps({"nothing to see": "this isn't happening"}),
# 			content_type="application/json"
#         )