from haystack import indexes
from qbdb.models import Tossup, Bonus

class TossupIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    tossup_text = indexes.CharField(model_attr='tossup_text_sanitized')
    answer = indexes.NgramField(model_attr='answer_sanitized')


    def get_model(self):
        return Tossup

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        

class BonusIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    leadin_text = indexes.CharField(model_attr='leadin_sanitized')
    part1_text = indexes.CharField(model_attr='part1_text_sanitized')
    part1_answer = indexes.NgramField(model_attr='part1_answer_sanitized')
    part2_text = indexes.CharField(model_attr='part2_text_sanitized')
    part2_answer = indexes.NgramField(model_attr='part2_answer_sanitized')
    part3_text = indexes.CharField(model_attr='part3_text_sanitized')
    part3_answer = indexes.NgramField(model_attr='part3_answer_sanitized')
    part4_text = indexes.CharField(model_attr='part4_text_sanitized')
    part4_answer = indexes.NgramField(model_attr='part4_answer_sanitized')
    part5_text = indexes.CharField(model_attr='part5_text_sanitized')
    part5_answer = indexes.NgramField(model_attr='part5_answer_sanitized')
    part6_text = indexes.CharField(model_attr='part6_text_sanitized')
    part6_answer = indexes.NgramField(model_attr='part6_answer_sanitized')


    def get_model(self):
        return Bonus

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
