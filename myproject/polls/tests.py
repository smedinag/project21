import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.

class QuestionModelTests(TestCase):

    def test_fue_publicado_reciente_preg_futura(self):
        """
        fue_publicado_reciente() debe devolver Falso para preguntas donde pub_date es una fecha futura
        """

        time = timezone.now() + datetime.timedelta(days=30)
        preg_futura= Question(pub_date=time)
        self.assertIs(preg_futura.fue_publicado_reciente(), False)
