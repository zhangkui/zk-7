from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    LEVEL_CHOICES = [
        (1, '国家级'),
        (2, '省级'),
        (3, '市级'),
        (4, '县级'),
    ]

    CATEGORY_TYPE_CHOICES = [
        ('folk_literature', '民间文学'),
        ('traditional_music', '传统音乐'),
        ('traditional_dance', '传统舞蹈'),
        ('traditional_theater', '传统戏剧'),
        ('traditional_acrobatics', '传统体育、游艺与杂技'),
        ('traditional_art', '传统美术'),
        ('traditional_craft', '传统技艺'),
        ('traditional_medicine', '传统医药'),
        ('folk_custom', '民俗'),
        ('other', '其他'),
    ]

    name = models.CharField('类别名称', max_length=100, unique=True)
    category_type = models.CharField('大类', max_length=50, choices=CATEGORY_TYPE_CHOICES, default='other')
    level = models.IntegerField('保护级别', choices=LEVEL_CHOICES, default=2)
    description = models.TextField('描述', blank=True)
    slug = models.SlugField('URL别名', unique=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '非遗类别'
        verbose_name_plural = verbose_name
        ordering = ['category_type', 'level', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=50, unique=True)
    color = models.CharField('标签颜色', max_length=7, default='#6c757d', help_text='十六进制颜色，如 #ff5722')
    slug = models.SlugField('URL别名', unique=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class HeritageProject(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('项目名称', max_length=200)
    english_name = models.CharField('英文名称', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects', verbose_name='所属类别')
    tags = models.ManyToManyField(Tag, related_name='projects', verbose_name='标签', blank=True)
    code = models.CharField('项目编号', max_length=50, unique=True, blank=True)
    region = models.CharField('流传地区', max_length=200, blank=True)
    inheritors = models.CharField('代表性传承人', max_length=500, blank=True)
    origin_date = models.CharField('起源年代', max_length=100, blank=True)
    overview = models.TextField('项目概述', blank=True)
    history = models.TextField('历史渊源', blank=True)
    content = models.TextField('基本内容', blank=True)
    features = models.TextField('主要特征', blank=True)
    value = models.TextField('重要价值', blank=True)
    current_situation = models.TextField('存续现状', blank=True)
    protection_measures = models.TextField('保护措施', blank=True)
    cover_image = models.ImageField('封面图片', upload_to='covers/%Y/%m/', blank=True, null=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    view_count = models.IntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '非遗项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            prefix = self.category.category_type[:3].upper() if self.category else 'ICH'
            self.code = f'{prefix}-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)


class MediaResource(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', '图片'),
        ('video', '视频'),
        ('audio', '音频'),
        ('document', '文档'),
    ]

    project = models.ForeignKey(HeritageProject, on_delete=models.CASCADE, related_name='media_resources', verbose_name='所属项目')
    title = models.CharField('资源标题', max_length=200)
    media_type = models.CharField('资源类型', max_length=20, choices=MEDIA_TYPE_CHOICES, default='image')
    file = models.FileField('资源文件', upload_to='media/%Y/%m/', blank=True, null=True)
    url = models.URLField('外部链接', blank=True, help_text='如果文件为外部链接请填写此项')
    thumbnail = models.ImageField('缩略图', upload_to='thumbnails/%Y/%m/', blank=True, null=True)
    description = models.TextField('描述', blank=True)
    duration = models.CharField('时长', max_length=20, blank=True, help_text='音视频时长，如 03:25')
    is_primary = models.BooleanField('是否主展示', default=False)
    sort_order = models.IntegerField('排序', default=0)
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        verbose_name = '多媒体资源'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', '-uploaded_at']

    def __str__(self):
        return f'{self.get_media_type_display()}: {self.title}'


class Exhibition(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('专题标题', max_length=200)
    subtitle = models.CharField('副标题', max_length=300, blank=True)
    slug = models.SlugField('URL别名', unique=True, blank=True)
    description = models.TextField('专题介绍', blank=True)
    cover_image = models.ImageField('封面图片', upload_to='exhibition_covers/%Y/%m/', blank=True, null=True)
    banner_image = models.ImageField('横幅图片', upload_to='exhibition_banners/%Y/%m/', blank=True, null=True)
    curator = models.CharField('策展人', max_length=100, blank=True)
    start_date = models.DateField('开展日期', blank=True, null=True)
    end_date = models.DateField('结束日期', blank=True, null=True)
    projects = models.ManyToManyField(HeritageProject, through='ExhibitionItem', related_name='exhibitions', verbose_name='包含项目')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    view_count = models.IntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '专题展陈'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ExhibitionItem(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, verbose_name='专题展陈')
    project = models.ForeignKey(HeritageProject, on_delete=models.CASCADE, verbose_name='非遗项目')
    section_title = models.CharField('章节标题', max_length=200, blank=True)
    section_description = models.TextField('章节描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '展陈项目'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']
        unique_together = ['exhibition', 'project']

    def __str__(self):
        return f'{self.exhibition.title} - {self.project.name}'
