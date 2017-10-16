 # howdy/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Papers
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core import serializers

# Create your views here.
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html')


def getContent(request, **kwargs):
    if request.method == 'POST':
		query = request.POST.get('query')
		response_data = {}

		# post = Post(text=post_text, author=request.user)
		# post.save()
		# Do query

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
					papers = Papers.objects.filter(year=query).only("year", "title")

					line_items=[]
					for paper in papers:
					    year = paper.year
					    title = paper.title

					    jsonInstance = {
					                'year': year,
					                'title': title
					            	}
					    line_items.append(jsonInstance)

					jsonOutput = json.dumps(line_items)
					#data = serializers.serialize("json", papers)
					response_data['papers'] = jsonOutput
				except ObjectDoesNotExist:
					null

		response_data['result'] = 'Create post successful!'
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