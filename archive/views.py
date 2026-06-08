from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Q
from .models import HeritageProject, Category, Tag, Exhibition, ExhibitionItem, MediaResource
from .search import search_service


def home(request):
    featured_projects = HeritageProject.objects.filter(
        status='published'
    ).select_related('category').prefetch_related('tags')[:6]

    featured_exhibitions = Exhibition.objects.filter(
        status='published'
    )[:4]

    categories = Category.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    ).filter(project_count__gt=0)[:10]

    popular_tags = Tag.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    ).filter(project_count__gt=0).order_by('-project_count')[:15]

    recent_projects = HeritageProject.objects.filter(
        status='published'
    ).select_related('category').order_by('-created_at')[:8]

    context = {
        'featured_projects': featured_projects,
        'featured_exhibitions': featured_exhibitions,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_projects': recent_projects,
    }
    return render(request, 'archive/home.html', context)


def project_list(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    tag_slug = request.GET.get('tag', '')
    page = int(request.GET.get('page', 1))

    if query:
        search_result = search_service.search_projects(
            query=query,
            category_slug=category_slug,
            tag_slug=tag_slug,
            page=page,
            per_page=12
        )
        projects = search_result['results']
        total = search_result['total']
        total_pages = search_result['total_pages']
    else:
        queryset = HeritageProject.objects.filter(status='published').select_related('category').prefetch_related('tags')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        queryset = queryset.distinct().order_by('-created_at')

        paginator = Paginator(queryset, 12)
        page_obj = paginator.get_page(page)
        projects = list(page_obj)
        total = paginator.count
        total_pages = paginator.num_pages

    categories = Category.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    )
    tags = Tag.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    ).order_by('-project_count')

    current_category = None
    if category_slug:
        current_category = Category.objects.filter(slug=category_slug).first()

    current_tag = None
    if tag_slug:
        current_tag = Tag.objects.filter(slug=tag_slug).first()

    max_pages = 5
    start_page = max(1, page - max_pages // 2)
    end_page = min(total_pages, start_page + max_pages - 1)
    if end_page - start_page < max_pages - 1:
        start_page = max(1, end_page - max_pages + 1)
    page_range = range(start_page, end_page + 1)

    context = {
        'projects': projects,
        'query': query,
        'categories': categories,
        'tags': tags,
        'current_category': current_category,
        'current_tag': current_tag,
        'total': total,
        'page': page,
        'total_pages': total_pages,
        'page_range': page_range,
        'has_next': page < total_pages,
        'has_previous': page > 1,
    }
    return render(request, 'archive/project_list.html', context)


def project_detail(request, pk):
    project = get_object_or_404(HeritageProject, pk=pk, status='published')

    project.view_count += 1
    project.save(update_fields=['view_count'])

    media_images = project.media_resources.filter(media_type='image').order_by('sort_order')
    media_videos = project.media_resources.filter(media_type='video').order_by('sort_order')
    media_audios = project.media_resources.filter(media_type='audio').order_by('sort_order')
    media_documents = project.media_resources.filter(media_type='document').order_by('sort_order')

    related_projects = HeritageProject.objects.filter(
        status='published',
        category=project.category
    ).exclude(pk=project.pk).select_related('category')[:4]

    context = {
        'project': project,
        'media_images': media_images,
        'media_videos': media_videos,
        'media_audios': media_audios,
        'media_documents': media_documents,
        'related_projects': related_projects,
    }
    return render(request, 'archive/project_detail.html', context)


def exhibition_list(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))

    if query:
        search_result = search_service.search_exhibitions(query=query, page=page, per_page=9)
        exhibitions = search_result['results']
        total = search_result['total']
        total_pages = search_result['total_pages']
    else:
        queryset = Exhibition.objects.filter(status='published').order_by('-created_at')
        paginator = Paginator(queryset, 9)
        page_obj = paginator.get_page(page)
        exhibitions = list(page_obj)
        total = paginator.count
        total_pages = paginator.num_pages

    context = {
        'exhibitions': exhibitions,
        'query': query,
        'total': total,
        'page': page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': page > 1,
    }
    return render(request, 'archive/exhibition_list.html', context)


def exhibition_detail(request, pk):
    exhibition = get_object_or_404(Exhibition, pk=pk, status='published')

    exhibition.view_count += 1
    exhibition.save(update_fields=['view_count'])

    items = ExhibitionItem.objects.filter(
        exhibition=exhibition
    ).select_related('project').prefetch_related('project__category', 'project__tags').order_by('sort_order')

    context = {
        'exhibition': exhibition,
        'items': items,
    }
    return render(request, 'archive/exhibition_detail.html', context)


def category_list(request):
    categories = Category.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    ).order_by('category_type', 'level', 'name')

    grouped_categories = {}
    for cat in categories:
        ctype = cat.get_category_type_display()
        if ctype not in grouped_categories:
            grouped_categories[ctype] = []
        grouped_categories[ctype].append(cat)

    context = {
        'grouped_categories': grouped_categories,
        'categories': categories,
    }
    return render(request, 'archive/category_list.html', context)


def tag_list(request):
    tags = Tag.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status='published'))
    ).order_by('-project_count', 'name')

    context = {
        'tags': tags,
    }
    return render(request, 'archive/tag_list.html', context)


def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    search_type = request.GET.get('type', 'all')

    context = {
        'query': query,
        'search_type': search_type,
    }

    if query:
        if search_type == 'project':
            result = search_service.search_projects(query=query, page=page, per_page=10)
            context.update({
                'projects': result['results'],
                'project_total': result['total'],
                'project_total_pages': result['total_pages'],
                'page': page,
                'total_pages': result['total_pages'],
                'has_next': page < result['total_pages'],
                'has_previous': page > 1,
            })
        elif search_type == 'exhibition':
            result = search_service.search_exhibitions(query=query, page=page, per_page=10)
            context.update({
                'exhibitions': result['results'],
                'exhibition_total': result['total'],
                'exhibition_total_pages': result['total_pages'],
                'page': page,
                'total_pages': result['total_pages'],
                'has_next': page < result['total_pages'],
                'has_previous': page > 1,
            })
        else:
            result = search_service.search_all(query=query)
            context.update({
                'projects': result['projects']['results'],
                'project_total': result['projects']['total'],
                'exhibitions': result['exhibitions']['results'],
                'exhibition_total': result['exhibitions']['total'],
            })

    return render(request, 'archive/search.html', context)


@require_GET
def autocomplete(request):
    query = request.GET.get('q', '')
    suggestions = []

    if len(query) >= 2:
        if search_service.available:
            try:
                body = {
                    'suggest': {
                        'project-suggest': {
                            'prefix': query,
                            'completion': {
                                'field': 'name',
                                'size': 5
                            }
                        }
                    }
                }
            except Exception:
                pass

        projects = HeritageProject.objects.filter(
            status='published',
            name__icontains=query
        ).values_list('name', flat=True)[:8]

        exhibitions = Exhibition.objects.filter(
            status='published',
            title__icontains=query
        ).values_list('title', flat=True)[:4]

        suggestions = list(projects) + list(exhibitions)
        suggestions = suggestions[:10]

    return JsonResponse({'suggestions': suggestions})
