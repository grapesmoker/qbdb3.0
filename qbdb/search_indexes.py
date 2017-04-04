from haystack import indexes
from qbdb.models import Tossup, Bonus, BonusPart


class TossupIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    tossup_text = indexes.CharField(model_attr='tossup_text_sanitized')
    tossup_answer = indexes.CharField(model_attr='answer_sanitized')

    def get_model(self):
        return Tossup

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        

class BonusIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    leadin_text = indexes.CharField(model_attr='leadin_sanitized')

    def get_model(self):
        return Bonus

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class BonusPartTextIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    part_text = indexes.CharField(model_attr='text_sanitized')
    bonus_answer = indexes.CharField(model_attr='answer_sanitized')

    def get_model(self):
        return BonusPart

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

