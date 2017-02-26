import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

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

    # 만약, 질문이 없을 경우 질문이 없다는 메세지 노출 여부와 데이터 결과 테스트
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        # 리턴 상태 코드값이 200인지 체크
        self.assertEquals(response.status_code, 200)
        # 데이터가 없을 경우 선택 가능한 질문이 없습니다 노출 체크
        self.assertContains(response, "선택 가능한 질문이 없습니다.")
        # 데이터가 없을 경우 쿼리셋이 [] empty 인지 체크
        self.assertQuerysetEqual(response.context['lastest_question_list'],[])

    # 등록일자 기준으로 지난에 등록된 데이터 조회시 Index 페이지에 어떻게 노출되는지 테스트
    # 이전의 데이터 조회시 검색된 데이터가 노출 되어야 한다
    def test_index_view_with_a_past_question(self):
        create_question(question_text="과거 질문", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['last_question_list'], ['<질문: 지난 질문>']
        )

    # 등록일자 기준으로 미래의 데이터 조회시 Index 페이지에 어떻게 노출되는지 테스트
    # 미래의 데이터 조회시 노출되지 않아야 한다
    def test_index_view_with_a_future_question(self):
        create_question(question_text="미래 질문", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "선택 가능한 질문이 없습니다")
        self.assertQuerysetEqual(response.context['lastest_question_list'],[])

    # 등록일자 기준으로 미래의 데이터와 과거의 데이터 동시 조회시 Index 페이지지에 어떻게 노출되는지 테스트
    # 과거의 질문과 미래의 질문이 둘 다 존재할 때, 과거의 질문만 노출되어야 한다.
    def text_index_view_with_future_question_and_past_question(self):
        create_question(question_text="과거 질문", days=-30)
        create_question(question_text="미래 질문", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['lastest_questuon_list'], ['<질문: 지난 질문>']
        )