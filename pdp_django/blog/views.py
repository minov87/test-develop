from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList

# Create your views here.
class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'

class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'

class PostDV(DetailView):
    model = Post

class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'

class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True

class PostMAV(MonthArchiveView):
    model = Post
    month_format = '%m' # %b 형태가 한글인 문제로 월 형태를 숫자로 변경
    date_field = 'modify_date'

class PostDAV(DayArchiveView):
    model = Post
    month_format = '%m' # %b 형태가 한글인 문제로 월 형태를 숫자로 변경
    date_field = 'modify_date'

class PostTAV(TodayArchiveView):
    model = Post
    month_format = '%m' # %b 형태가 한글인 문제로 월 형태를 숫자로 변경
    date_field = 'modify_date'