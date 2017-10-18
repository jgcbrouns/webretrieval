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


# Create your views here.
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html')

def page_view(request):
	if request.method == 'GET':
		documentId = request.GET.get('id')

		topicsList = []

		db = get_db()
		cursor = get_topics_for_document(db, documentId)
		for topic in cursor:
			if topic != 'documentId' and topic != '_id' and topic != 'main topic' and topic != 'second topic' and topic != 'third topic':
				topicName = topic
				topicValue = cursor[topic]

				topicDict = {'topic': topicName, 'value': topicValue}

				topicsList.append(topicDict)

		topicsList.sort(key=lambda item: (item['value']),reverse=True)

		return render(request, 'page.html', {'topics': topicsList})

def getContent(request, **kwargs):
    if request.method == 'POST':
		query = request.POST.get('query')
		response_data = {}

		# post = Post(text=post_text, author=request.user)
		# post.save()
		# Do query
		db = get_db()
		if query:
			try:
				query = int(query)
			except ValueError:
				query = None
				papers = None


				#return empty data
				response_data['papers'] = json.dumps([])
			
			if query:
				try:
					papers = Papers.objects.filter(year=query).only("year", "title", "id")

					items=[]
					items_with_pagerank=[]
    
					for paper in papers:
						year = paper.year
						title = paper.title
						id = paper.id
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