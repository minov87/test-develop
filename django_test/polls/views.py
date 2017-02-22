# 404 Error 페이지 렌더링
from django.http import Http404
# 템플릿 렌더링
from django.shortcuts import get_object_or_404, render
# HttpResponse 처리
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# models 에 있는 질문항목 임폴트
from .models import Question, Choice

# generic View 활용시
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		# 최근에 등록된 5개의 질문 노출
		#return Question.objects.order_by('-pub_date')[:5]
		# 최근 등록 5개를 노출하되, 미래의 질문은 비노출 처리
		# Questions whose pub_date is less than or equal to -
		# that is, earlier than or equal to - timezone.now
		return Question.objects.filter()
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

# 일반 방식 활용시
def index(request):
	#return HttpResponse("Test Index page")

	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('poll/index.html')
	#context = {
	#	'latest_question_list':latest_question_list,
	#}

	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)

	#return HttpResponse(template.render(context, request))

	context = {'latest_question_list' : latest_question_list}
	return render(request, 'polls/index.html', context)

# index 에서 선택한 질문의 상세 페이지 렌더링
def detail(request, question_id):
	# exception 처리
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("해당 질문은 존재하지 않습니다.")
	#return HttpResponse("당신이 선택한 질문은 '%s'번 질문 입니다." %question_id)

	return render(request, 'polls/detail.html', {'question' : question})

# 투표 처리
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	# exception 처리
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# 투표 선택 페이지로 재 렌더링
		return render(request,
			'polls/detail.html', {
				'question' : question,
				'error_message' : "선택된 투표 값이 없습니다.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# POST 데이터가 정상적으로 완료 되었을 때는 항상 HttpResponseRedirect를 통해
		# 리턴을 해야 하며, 이는 사용자가 뒤로가기버튼을 눌렀을 경우 두번 전송되는 것을 방지.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
	#return HttpResponse("'%s' 질문에 대한 당신의 투표는" %question_id)

# 결과 페이지 렌더링
def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question' : question})
#	return HttpResponse(response %question_id)
