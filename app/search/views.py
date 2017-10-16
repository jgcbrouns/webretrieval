 # howdy/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Papers
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class HomePageView(TemplateView):
    # def get(self, request, **kwargs):
    # 	papers = Papers.objects.all()
    # 	return render(request, 'index.html', {'papers': papers})

	def get(self, request, **kwargs):
		query = request.GET.get('q')
		if query:
			try:
				query = int(query)
			except ValueError:
				query = None
				papers = None
			if query:
				try:
					papers = Papers.objects.filter(year=query)
					return render(request, 'index.html', {"papers": papers})
				except ObjectDoesNotExist:
					null
			#return HttpResponse(papers)
			#context = RequestContext(request)
		#return render_to_response('index.html')
		return render(request, 'index.html')

	# def get(self, request, **kwargs):
	#     if request.method == 'POST':
	#         post_text = request.POST.get('the_post')
	#         response_data = {}

	#         post = Post(text=post_text, author=request.user)
	#         post.save()

	#         response_data['result'] = 'Create post successful!'
	#         response_data['postpk'] = post.pk
	#         response_data['text'] = post.text
	#         response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
	#         response_data['author'] = post.author.username

	#         return HttpResponse(
	#             json.dumps(response_data),
	#             content_type="application/json"
	#         )
	#     else:
	#         return HttpResponse(
	#             json.dumps({"nothing to see": "this isn't happening"}),
	#             content_type="application/json"
	#         )