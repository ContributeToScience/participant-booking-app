from haystack import indexes
from .models import Research


class ResearchIndex(indexes.ModelSearchIndex, indexes.Indexable):
    #text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Research
        fields = ['name', 'description', 'location', 'url']

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_publish=True)
