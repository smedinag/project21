import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
# Create your tests here.

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles.")

    def test_past_question(self):
        """
                Questions with a pub_date in the past are displayed on the
                index page.
                """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
                Questions with a pub_date in the future aren't displayed on
                the index page.
                """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
              Even if both past and future questions exist, only past questions
              are displayed.
              """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
                The questions index page may display multiple questions.
                """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )



class QuestionModelTests(TestCase):

    def test_fue_publicado_reciente_preg_futura(self):
        """
        fue_publicado_reciente() debe devolver Falso para preguntas donde pub_date es una fecha futura
        """

        time = timezone.now() + datetime.timedelta(days=30)
        preg_futura= Question(pub_date=time)
        self.assertIs(preg_futura.fue_publicado_reciente(), False)

    def test_fue_publicado_reciente_preg_pasada(self):
        """
               fue_publicado_reciente() retorna False para preguntas donde pub_date tiene mas de 1 dia de publicacion
        """

        time= timezone.now() - datetime.timedelta(hours=24, seconds=1) ## timedelta(days=1, seconds=1)
        preg_pasada= Question(pub_date=time)
        self.assertIs(preg_pasada.fue_publicado_reciente(), False)

    def test_fue_publicado_reciente_preg_reciente(self):
        """
               fue_publicado_reciente() retorna True para preguntas donde pub_date fue publicado en el ultimo dia (ultimas 24 horas)
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        preg_reciente= Question(pub_date=time)
        self.assertIs(preg_reciente.fue_publicado_reciente(), True)


