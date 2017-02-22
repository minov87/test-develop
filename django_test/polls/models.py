import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# 파이선2 에서도 사용하려고 할 때 아래와 같이 추가함. (3으로 작성해도 2에서 인식 가능)
@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # 질문에 대한 메시지 리턴 처리
    def __str__(self):
        return self.question_text

    # 최근 게시글 여부 (신규글) 체크
    def was_published_recently(self):
        now = timezone.now()

        # 기존 방식의 문제는 현재시간에서 -1 days (결국 1일전) 가 등록일자보다 크거나 같다는
        # 조건 설정시 미래의 일자 ex) +30 days 설정시 테스트 케이스를 통과하지 못함.
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        #print(now - datetime.timedelta(days=1) <= self.pub_date)
        #print(now - datetime.timedelta(days=1) <= self.pub_date <= now)
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# 파이선2 에서도 사용하려고 할 때 아래와 같이 추가함. (3으로 작성해도 2에서 인식 가능)
@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # 선택에 대한 메시지 리턴 처리
    def __str__(self):
        return self.choice_text
