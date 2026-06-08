from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import HeritageProject, Category, Tag, Exhibition


project_index = Index('heritage_projects')
project_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        'analyzer': {
            'ik_max_word': {
                'type': 'ik_max_word'
            },
            'ik_smart': {
                'type': 'ik_smart'
            }
        }
    }
)

exhibition_index = Index('exhibitions')
exhibition_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@registry.register_document
@project_index.document
class HeritageProjectDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'category_type': fields.TextField(),
        'level': fields.IntegerField(),
    })
    tags = fields.NestedField(properties={
        'name': fields.TextField(),
        'color': fields.TextField(),
    })

    class Django:
        model = HeritageProject
        fields = [
            'name',
            'english_name',
            'code',
            'region',
            'inheritors',
            'origin_date',
            'overview',
            'history',
            'content',
            'features',
            'value',
            'current_situation',
            'protection_measures',
            'status',
            'view_count',
            'created_at',
            'updated_at',
        ]
        related_models = [Category, Tag]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.projects.all()
        elif isinstance(related_instance, Tag):
            return related_instance.projects.all()


@registry.register_document
@exhibition_index.document
class ExhibitionDocument(Document):
    projects = fields.NestedField(properties={
        'name': fields.TextField(),
        'code': fields.TextField(),
    })

    class Django:
        model = Exhibition
        fields = [
            'title',
            'subtitle',
            'description',
            'curator',
            'status',
            'view_count',
            'created_at',
        ]
        related_models = [HeritageProject]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, HeritageProject):
            return related_instance.exhibitions.all()
