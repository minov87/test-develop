import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

# Create your tests here.

# 질문 등록 테스트
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# 질문 메소드 테스트 케이스
class QuestionMethodTests(TestCase):

    # 미래일자로 등록된 질문의 최근표시 테스트 (+30일후 등록 테스트)
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    # 이전 일자로 등록시 최근표시 테스트 (-30일전 등록 테스트)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    # 최근표시 정상동작 테스트 (-1시간전 등록된 것으로 테스트)
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionViewTests(TestCase):

    # 질문이 없을 경우, 메세지 노출 과 데이터 노출에 대한 체크
    def test_index_view_with_now_questions(self):
        response = self.client.get(reverse('polls:index'))
        # 리턴 상태 코드값이 200인지 체크
        self.assertEquals(response.status_code, 200)
        # 데이터가 없을 경우 선택 가능한 질문이 없습니다 노출 체크
        self.assertContains(response, "선택 가능한 질문이 없습니다.")
        # 데이터가 없을 경우 쿼리셋이 [] empty 인지 체크
        self.assertQuerysetEqual(reponse.context['lastest_question_list'],[])
