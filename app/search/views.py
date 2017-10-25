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
from youtube import *
import urllib
import wikipedia

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



def queryAndRetrieveWiki(query):
	# url = "https://en.wikipedia.org/wiki/" + query
	# f = urllib.urlopen(url)
	# result =  f.read()
	# print >>sys.stderr, result
	try:
		result =  wikipedia.summary(query, sentences=3)
	except:
		result = ''
	return result


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
				topicRetrievedDefinition = queryAndRetrieveWiki(topicName)

				topicDict = {'topic': topicName, 'value': topicValue, 'definition': topicRetrievedDefinition}

				topicsList.append(topicDict)

		paper = get_paper(db, int(documentId))
		# get_authors_for_paper(db, int(documentId))
		authors = get_authors_for_paper(db, int(documentId))

		######### 5th COMPONENT #######
		youtubeIds = youtube_search(str(paper['title']), 3)
		print >>sys.stderr, youtubeIds
		##############################

		topicsList.sort(key=lambda item: (item['value']),reverse=True)

		return render(request, 'page.html', {'topics': topicsList, 'metadata': paper, 'authors': authors, 'keywords' : keywords, 'youtubeIds' : youtubeIds},)

def get_papers_from_list(db, ids, year):
	if year != 0:
		cursor = db.pages.find({'documentId': {'$in': ids}, 'year': year});
	else:
		cursor = db.pages.find({'documentId': {'$in': ids}});
	return cursor

def clusters_view(request):
	return render(request, 'clusters.html')

def cluster1_view(request):
	return render(request, 'cluster1.html')

def cluster2_view(request):
	return render(request, 'cluster2.html')

def cluster3_view(request):
	return render(request, 'cluster3.html')

def cluster4_view(request):
	return render(request, 'cluster4.html')

def cluster5_view(request):
	return render(request, 'cluster5.html')


def doParseOptionBooleans(value):
	if value == 'true':
		value = True
	else:
		value = False
	return value

def queryIsInt(query):
	try:
		query = int(query)
		return True
	except ValueError:
		return False

def doIntegerProcedure(query, usepagerank, reindex):
	db = get_db()
	response_data = {}
	
	if query:
		try:
			papers = get_papers_for_intquery(db, query)
			if papers:
				response_data['status'] = 'done'

			final_list = processPapers(papers, db)
			jsonOutput = json.dumps(final_list)

			response_data = setFieldExitParameters(response_data, usepagerank)

			response_data['papers'] = jsonOutput

		except ObjectDoesNotExist:
			null

	else:
		response_data['papers'] = json.dumps([])

	response_data['result'] = 'data retrieval successful!'
	response_data['query'] = query

	return response_data

def hasPagerankValue(db, id):
	try:
		cursor = get_pagerank(db, id)
		if cursor:
			pagerank = cursor['PageRank']
			return pagerank
		else:
			return ''
	except ObjectDoesNotExist:
		return 'ERROR'

def appendItemWithPageRank(paper, items_with_pagerank, pagerank):
	year = paper['year']
	title = paper['title']
	id = paper['documentId']
	jsonInstance = {'year': year,'title': title,'pagerank': pagerank, 'id': id}
	items_with_pagerank.append(jsonInstance)
	return items_with_pagerank

#Item without pagerank
def appendItem(paper, items):
	year = paper['year']
	title = paper['title']
	id = paper['documentId']
	jsonInstance = {'year': year,'title': title, 'id': id}
	items.append(jsonInstance)
	return items

def setFieldExitParameters(response_data, usepagerank):
	if usepagerank:
		response_data['usepagerank'] = 'true'
	else:
		response_data['usepagerank'] = 'false'
	return response_data

def processPapers(papers, db):
	items=[]
	items_with_pagerank=[]

	for paper in papers:						
		id = paper['documentId']

		#check if pagerank exist and that there was no error
		if(hasPagerankValue(db, id) != "ERROR" and hasPagerankValue(db, id) != ""):
			pagerank = hasPagerankValue(db, id)
			items_with_pagerank = appendItemWithPageRank(paper, items_with_pagerank, pagerank)
		else:
			items = appendItem(paper, items)

	if items_with_pagerank != []:
		#sort on pagerank
		items_with_pagerank.sort(key=lambda item: (item['pagerank']),reverse=True)
		final_list = items_with_pagerank + items
	else:
		final_list = items

	return final_list

def doStringProcedure(query, usepagerank, reindex, field, pagerank_threshold, year):
	db = get_db()
	response_data = {}
	
	if query:
		try:
			#papers = Papers.objects.filter(year=query).only("year", "title", "id")
			print query
			ids = final(query, field, 100, False, pagerank_threshold)
			papers = get_papers_from_list(db, ids, year)

			final_list = processPapers(papers, db)
			jsonOutput = json.dumps(final_list)

			response_data = setFieldExitParameters(response_data, usepagerank)

			response_data['papers'] = jsonOutput

		except ObjectDoesNotExist:
			null

	else:
		response_data['papers'] = json.dumps([])

	response_data['query'] = query
	response_data['status'] = 'done'

	return response_data


def getContent(request, **kwargs):
    if request.method == 'POST':

    	##########get post parameters#########
		query = request.POST.get('query')
		field = request.POST.get('field')
		reindexString = request.POST.get('reindex')
		usepagerankString = request.POST.get('usepagerank')
		pagerank_threshold = float(request.POST.get('threshold'))
		year = int(request.POST.get('year'))

		######################################

		########Do some boolean parsing#######
		reindex = doParseOptionBooleans(reindexString)
		# usepagerank = doParseOptionBooleans(usepagerankString)
		usepagerank = True;
		######################################

		if query:
			if(queryIsInt(query)):
				response_data = doIntegerProcedure(query, usepagerank, reindex)
			else:
				response_data = doStringProcedure(query, usepagerank, reindex, field, pagerank_threshold, year)

		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
        )
   #  else:
   #      return HttpResponse(
			# json.dumps({"nothing to see": "this isn't happening"}),
			# content_type="application/json"
   #      )
