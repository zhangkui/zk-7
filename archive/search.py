from elasticsearch import Elasticsearch
from django.conf import settings
from .models import HeritageProject, Exhibition


class SearchService:
    def __init__(self):
        try:
            self.client = Elasticsearch(
                settings.ELASTICSEARCH_DSL['default']['hosts'],
                timeout=30
            )
            self.available = self.client.ping()
        except Exception:
            self.available = False

    def search_projects(self, query, category_slug=None, tag_slug=None, page=1, per_page=12):
        if not self.available:
            return self._fallback_search_projects(query, category_slug, tag_slug, page, per_page)

        try:
            from_ = (page - 1) * per_page
            body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': query,
                                    'fields': [
                                        'name^3',
                                        'english_name^2',
                                        'code^2',
                                        'region^1.5',
                                        'inheritors^1.5',
                                        'overview',
                                        'content',
                                        'features',
                                        'history',
                                        'value'
                                    ],
                                    'type': 'best_fields',
                                    'fuzziness': 'AUTO'
                                }
                            }
                        ],
                        'filter': []
                    }
                },
                'highlight': {
                    'fields': {
                        'name': {},
                        'overview': {},
                        'content': {}
                    }
                },
                'from': from_,
                'size': per_page,
                'sort': [{'_score': {'order': 'desc'}}]
            }

            if category_slug:
                body['query']['bool']['filter'].append({
                    'term': {'category.name.keyword': category_slug}
                })

            if tag_slug:
                body['query']['bool']['filter'].append({
                    'nested': {
                        'path': 'tags',
                        'query': {
                            'term': {'tags.name.keyword': tag_slug}
                        }
                    }
                })

            result = self.client.search(index='heritage_projects', body=body)
            hits = result['hits']['hits']
            total_info = result['hits']['total']
            total = total_info['value'] if total_info.get('relation') == 'eq' else 10000

            project_ids = [hit['_id'] for hit in hits]
            projects = list(HeritageProject.objects.filter(id__in=project_ids, status='published'))
            project_dict = {str(p.id): p for p in projects}
            ordered_projects = [project_dict[pid] for pid in project_ids if pid in project_dict]

            return {
                'results': ordered_projects,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page,
                'highlights': {hit['_id']: hit.get('highlight', {}) for hit in hits}
            }
        except Exception:
            return self._fallback_search_projects(query, category_slug, tag_slug, page, per_page)

    def _fallback_search_projects(self, query, category_slug=None, tag_slug=None, page=1, per_page=12):
        from django.db.models import Q
        queryset = HeritageProject.objects.filter(status='published')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(english_name__icontains=query) |
                Q(code__icontains=query) |
                Q(region__icontains=query) |
                Q(inheritors__icontains=query) |
                Q(overview__icontains=query) |
                Q(content__icontains=query) |
                Q(history__icontains=query) |
                Q(features__icontains=query) |
                Q(value__icontains=query)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        queryset = queryset.distinct()
        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page
        projects = list(queryset[start:end])

        return {
            'results': projects,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'highlights': {}
        }

    def search_exhibitions(self, query, page=1, per_page=12):
        if not self.available:
            return self._fallback_search_exhibitions(query, page, per_page)

        try:
            from_ = (page - 1) * per_page
            body = {
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': [
                            'title^3',
                            'subtitle^2',
                            'description',
                            'curator'
                        ],
                        'type': 'best_fields',
                        'fuzziness': 'AUTO'
                    }
                },
                'from': from_,
                'size': per_page,
                'sort': [{'_score': {'order': 'desc'}}]
            }

            result = self.client.search(index='exhibitions', body=body)
            hits = result['hits']['hits']
            total_info = result['hits']['total']
            total = total_info['value'] if total_info.get('relation') == 'eq' else 10000

            exhibition_ids = [hit['_id'] for hit in hits]
            exhibitions = list(Exhibition.objects.filter(id__in=exhibition_ids, status='published'))
            exhibition_dict = {str(e.id): e for e in exhibitions}
            ordered_exhibitions = [exhibition_dict[eid] for eid in exhibition_ids if eid in exhibition_dict]

            return {
                'results': ordered_exhibitions,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
        except Exception:
            return self._fallback_search_exhibitions(query, page, per_page)

    def _fallback_search_exhibitions(self, query, page=1, per_page=12):
        from django.db.models import Q
        queryset = Exhibition.objects.filter(status='published')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(subtitle__icontains=query) |
                Q(description__icontains=query) |
                Q(curator__icontains=query)
            )

        total = queryset.count()
        start = (page - 1) * per_page
        end = start + per_page
        exhibitions = list(queryset[start:end])

        return {
            'results': exhibitions,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    def search_all(self, query):
        project_results = self.search_projects(query, page=1, per_page=6)
        exhibition_results = self.search_exhibitions(query, page=1, per_page=6)
        return {
            'projects': project_results,
            'exhibitions': exhibition_results,
            'total': project_results['total'] + exhibition_results['total']
        }


search_service = SearchService()
