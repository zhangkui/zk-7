from django.core.management.base import BaseCommand
from archive.models import Category, Tag, HeritageProject, Exhibition, ExhibitionItem


class Command(BaseCommand):
    help = '初始化示例数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化示例数据...')

        categories_data = [
            {'name': '昆曲', 'category_type': 'traditional_theater', 'level': 1,
             'description': '昆曲是中国古老的戏曲声腔、剧种，被称为"百戏之祖"。'},
            {'name': '京剧', 'category_type': 'traditional_theater', 'level': 1,
             'description': '京剧是中国影响最大的戏曲剧种，被视为中国国粹。'},
            {'name': '古琴艺术', 'category_type': 'traditional_music', 'level': 1,
             'description': '古琴是中国最古老的弹拨乐器之一，有三千多年历史。'},
            {'name': '中国书法', 'category_type': 'traditional_art', 'level': 1,
             'description': '中国书法是汉字的书写艺术，是中华文化的瑰宝。'},
            {'name': '中国篆刻', 'category_type': 'traditional_art', 'level': 1,
             'description': '中国篆刻是以石材为主要材料，以刻刀为工具的传统艺术。'},
            {'name': '中国剪纸', 'category_type': 'traditional_art', 'level': 1,
             'description': '剪纸是用剪刀或刻刀在纸上剪刻花纹的民间艺术。'},
            {'name': '苏绣', 'category_type': 'traditional_craft', 'level': 1,
             'description': '苏绣是苏州地区刺绣产品的总称，中国四大名绣之一。'},
            {'name': '景德镇手工制瓷技艺', 'category_type': 'traditional_craft', 'level': 1,
             'description': '景德镇制瓷历史悠久，被誉为"瓷都"。'},
            {'name': '中医针灸', 'category_type': 'traditional_medicine', 'level': 1,
             'description': '针灸是中国传统医学的重要组成部分。'},
            {'name': '端午节', 'category_type': 'folk_custom', 'level': 1,
             'description': '端午节是中国传统节日，有赛龙舟、吃粽子等习俗。'},
            {'name': '春节', 'category_type': 'folk_custom', 'level': 1,
             'description': '春节是中华民族最重要的传统节日。'},
            {'name': '苗族古歌', 'category_type': 'folk_literature', 'level': 1,
             'description': '苗族古歌是苗族口头传唱的长篇叙事诗。'},
            {'name': '吴桥杂技', 'category_type': 'traditional_acrobatics', 'level': 1,
             'description': '吴桥杂技是河北省吴桥县的传统杂技艺术。'},
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'category_type': cat_data['category_type'],
                    'level': cat_data['level'],
                    'description': cat_data['description'],
                }
            )
        self.stdout.write(self.style.SUCCESS(f'已创建/更新 {len(categories_data)} 个类别'))

        tags_data = [
            ('世界级', '#E74C3C'), ('人类非遗', '#9B59B6'), ('国宝级', '#3498DB'),
            ('传统工艺', '#2ECC71'), ('传统表演', '#F39C12'), ('民间艺术', '#1ABC9C'),
            ('传统节庆', '#E67E22'), ('传统医药', '#16A085'), ('书法艺术', '#8E44AD'),
            ('戏曲', '#C0392B'), ('音乐', '#2980B9'), ('美术', '#27AE60'),
            ('技艺', '#D35400'), ('民俗', '#2C3E50'), ('传承', '#7F8C8D'),
        ]

        for tag_name, color in tags_data:
            Tag.objects.get_or_create(
                name=tag_name,
                defaults={'color': color}
            )
        self.stdout.write(self.style.SUCCESS(f'已创建/更新 {len(tags_data)} 个标签'))

        projects_data = [
            {
                'name': '昆曲《牡丹亭》',
                'category_name': '昆曲',
                'tags': ['世界级', '戏曲', '传统表演'],
                'region': '江苏苏州',
                'inheritors': '王芳、汪世瑜',
                'origin_date': '元末明初',
                'overview': '《牡丹亭》是明代剧作家汤显祖的代表作，是昆曲最经典的剧目之一。',
                'history': '昆曲发源于江苏昆山，至今已有600多年历史。《牡丹亭》写成于明万历二十六年（1598年）。',
                'content': '该剧描写了杜丽娘与柳梦梅的爱情故事，体现了青年男女对自由爱情的追求。',
                'features': '昆曲唱腔华丽婉转，念白儒雅，表演细腻，舞蹈飘逸。',
                'value': '昆曲是中国戏曲艺术的珍品，被誉为"百戏之祖，百戏之师"。',
                'status': 'published',
            },
            {
                'name': '京剧《霸王别姬》',
                'category_name': '京剧',
                'tags': ['人类非遗', '戏曲', '传统表演'],
                'region': '北京',
                'inheritors': '梅葆玖',
                'origin_date': '清代乾隆年间',
                'overview': '《霸王别姬》是京剧艺术大师梅兰芳表演的梅派经典名剧之一。',
                'history': '京剧形成于清代乾隆年间，由徽剧、汉剧等融合演变而成。',
                'content': '故事讲述了西楚霸王项羽兵败垓下，与爱妃虞姬诀别的故事。',
                'features': '京剧融合了唱、念、做、打四种艺术手法，角色分为生、旦、净、丑。',
                'value': '京剧被视为中国国粹，是传播中国传统文化的重要载体。',
                'status': 'published',
            },
            {
                'name': '古琴名曲《流水》',
                'category_name': '古琴艺术',
                'tags': ['世界级', '音乐', '传统表演'],
                'region': '全国',
                'inheritors': '吴钊、李祥霆',
                'origin_date': '春秋战国时期',
                "overview": "《流水》是中国古代最著名的古琴曲之一，与伯牙子期的故事相关。",
                'history': '古琴有三千多年的历史，是中国最早的弹拨乐器。',
                'content': '《流水》一曲描绘了水的各种形态，表现了人与自然的和谐。',
                'features': '古琴音色深沉，余音悠远，具有独特的音乐表现力。',
                'value': '古琴艺术是中国传统文化的重要象征。',
                'status': 'published',
            },
            {
                'name': '王羲之《兰亭序》书法艺术',
                'category_name': '中国书法',
                'tags': ['国宝级', '书法艺术', '传统艺术'],
                'region': '浙江绍兴',
                'inheritors': '历代书法家',
                'origin_date': '东晋永和九年',
                'overview': '《兰亭序》被誉为"天下第一行书"，是王羲之的代表作。',
                'history': '东晋永和九年（353年），王羲之与友人在兰亭雅集，写下此序。',
                'content': '文章描绘了兰亭的优美景色和聚会的欢乐情景，抒发了对人生的感慨。',
                'features': '其书法飘逸遒劲，变化万千，达到了行书艺术的巅峰。',
                'value': '《兰亭序》是中国书法史上最具影响力的作品。',
                'status': 'published',
            },
            {
                'name': '吴昌硕篆刻艺术',
                'category_name': '中国篆刻',
                'tags': ['传统艺术', '技艺', '国宝级'],
                'region': '浙江安吉',
                'inheritors': '诸乐三、沙孟海',
                'origin_date': '清代晚期',
                'overview': '吴昌硕是近代最杰出的篆刻艺术家，"海派"代表人物。',
                'history': '中国篆刻起源于商代，至今已有三千多年历史。',
                'content': '吴昌硕的篆刻作品气势磅礴，雄浑古拙，独具风格。',
                'features': '篆刻融书法、绘画、雕刻于一体，是中国特有的传统艺术形式。',
                'value': '篆刻艺术是中国传统文化的重要组成部分。',
                'status': 'published',
            },
            {
                'name': '陕北剪纸艺术',
                'category_name': '中国剪纸',
                'tags': ['世界级', '民间艺术', '传统工艺'],
                'region': '陕西延安',
                'inheritors': '高凤莲',
                'origin_date': '汉代',
                'overview': '陕北剪纸是中国北方最具代表性的剪纸艺术形式之一。',
                'history': '剪纸艺术起源于汉代，发展于唐宋，盛于明清。',
                'content': '内容多反映陕北人民的生产生活、婚丧嫁娶、节日庆典等。',
                'features': '风格粗犷豪放，造型夸张生动，色彩对比强烈。',
                'value': '剪纸是人民群众创造的艺术，具有浓郁的乡土气息。',
                'status': 'published',
            },
            {
                'name': '苏绣双面绣',
                'category_name': '苏绣',
                'tags': ['传统工艺', '技艺', '国宝级'],
                'region': '江苏苏州',
                'inheritors': '姚建萍',
                'origin_date': '宋代',
                'overview': '双面绣是苏绣中最精妙的技艺之一，两面都可观赏。',
                'history': '苏绣历史悠久，至今已有两千多年历史。',
                'content': '作品题材广泛，包括花鸟、人物、山水、书法等。',
                'features': '针法精细，色彩雅洁，图案秀丽，被誉为"东方艺术明珠"。',
                'value': '苏绣是中国四大名绣之首，具有很高的艺术价值和收藏价值。',
                'status': 'published',
            },
            {
                'name': '景德镇青花瓷',
                'category_name': '景德镇手工制瓷技艺',
                'tags': ['世界级', '传统工艺', '技艺'],
                'region': '江西景德镇',
                'inheritors': '王锡良',
                'origin_date': '元代',
                'overview': '青花瓷是景德镇最具代表性的瓷器品种。',
                'history': '景德镇制瓷始于汉代，成熟于唐宋，元代创烧青花瓷。',
                'content': '青花瓷以钴料在瓷胎上绘画，施透明釉后高温烧成。',
                'features': '青白相映，纹饰优雅，被誉为"人间瑰宝"。',
                'value': '景德镇手工制瓷技艺是人类非物质文化遗产代表作。',
                'status': 'published',
            },
            {
                'name': '中医针灸疗法',
                'category_name': '中医针灸',
                'tags': ['世界级', '传统医药'],
                'region': '全国',
                'inheritors': '贺普仁、程莘农',
                'origin_date': '新石器时代',
                'overview': '针灸是中国传统医学中独特的治疗方法。',
                'history': '针灸起源于新石器时代，战国时代已形成完整体系。',
                'content': '通过针刺或艾灸人体穴位，调节气血，治疗疾病。',
                'features': '操作简便，适应症广，疗效显著，副作用小。',
                'value': '针灸已传播到世界100多个国家和地区。',
                'status': 'published',
            },
            {
                'name': '端午节习俗',
                'category_name': '端午节',
                'tags': ['世界级', '传统节庆', '民俗'],
                'region': '全国',
                'inheritors': '集体传承',
                'origin_date': '战国时期',
                'overview': '端午节是中国最重要的传统节日之一，定于农历五月初五。',
                'history': '端午节起源于对自然天象的崇拜，后融入纪念屈原的内容。',
                'content': '主要习俗有赛龙舟、吃粽子、挂艾草、佩香囊、饮雄黄酒等。',
                'features': '端午节民俗丰富多样，具有浓郁的中华文化特色。',
                'value': '端午节是人类非物质文化遗产代表作。',
                'status': 'published',
            },
            {
                'name': '春节习俗',
                'category_name': '春节',
                'tags': ['人类非遗', '传统节庆', '民俗'],
                'region': '全国',
                'inheritors': '集体传承',
                'origin_date': '上古时代',
                'overview': '春节是中华民族最隆重的传统节日，又称新年、过年。',
                'history': '春节起源于上古时代的岁首祈年祭祀活动。',
                'content': '习俗包括贴春联、放鞭炮、守岁、拜年、发压岁钱等。',
                'features': '春节是家人团聚的日子，承载着中华民族的文化记忆。',
                'value': '春节是中华民族文化认同的重要标志。',
                'status': 'published',
            },
            {
                'name': '苗族古歌传唱',
                'category_name': '苗族古歌',
                'tags': ['传统表演', '民间艺术', '传承'],
                'region': '贵州黔东南',
                'inheritors': '王安江、田锦隆',
                'origin_date': '远古时期',
                'overview': '苗族古歌是苗族先民口头创作的长篇叙事诗。',
                'history': '苗族古歌传唱已有数千年历史，是苗族的"百科全书"。',
                'content': '内容包括开天辟地、人类起源、民族迁徙、生产生活等。',
                'features': '篇幅宏大，语言古朴，具有很高的文学和史学价值。',
                'value': '苗族古歌是研究苗族历史文化的重要资料。',
                'status': 'published',
            },
            {
                'name': '吴桥杂技艺术',
                'category_name': '吴桥杂技',
                'tags': ['传统表演', '传统杂技', '技艺'],
                'region': '河北吴桥',
                'inheritors': '边发吉',
                'origin_date': '春秋战国时期',
                'overview': '吴桥杂技是中国最著名的地方杂技品种。',
                'history': '吴桥杂技有两千多年历史，被誉为"杂技之乡"。',
                'content': '节目包括口技、魔术、马戏、驯兽、高空杂技等。',
                'features': '以惊险、奇特、巧妙著称，具有浓郁的地方特色。',
                'value': '吴桥杂技是中华民族文化艺术的瑰宝。',
                'status': 'published',
            },
        ]

        for proj_data in projects_data:
            category = Category.objects.filter(name=proj_data['category_name']).first()
            project, created = HeritageProject.objects.get_or_create(
                name=proj_data['name'],
                defaults={
                    'category': category,
                    'region': proj_data['region'],
                    'inheritors': proj_data['inheritors'],
                    'origin_date': proj_data['origin_date'],
                    'overview': proj_data['overview'],
                    'history': proj_data['history'],
                    'content': proj_data['content'],
                    'features': proj_data['features'],
                    'value': proj_data['value'],
                    'status': proj_data['status'],
                }
            )
            tag_names = proj_data['tags']
            tags = Tag.objects.filter(name__in=tag_names)
            project.tags.set(tags)
        self.stdout.write(self.style.SUCCESS(f'已创建/更新 {len(projects_data)} 个非遗项目'))

        exhibitions_data = [
            {
                'title': '百戏之祖——昆曲艺术特展',
                'subtitle': '穿越六百年时空的雅韵',
                'description': '本展览系统呈现昆曲的历史渊源、艺术特色、经典剧目和代表性传承人，让观众领略"百戏之祖"的独特魅力。',
                'curator': '戏曲研究所',
                'project_names': ['昆曲《牡丹亭》'],
                'status': 'published',
            },
            {
                'title': '国粹风华——京剧艺术大展',
                'subtitle': '生旦净丑演绎人间百态',
                'description': '展示京剧的形成发展、表演体系、经典剧目和艺术成就，弘扬国粹艺术。',
                'curator': '中国艺术研究院',
                'project_names': ['京剧《霸王别姬》'],
                'status': 'published',
            },
            {
                'title': '千年一脉——中华传统技艺展',
                'subtitle': '匠心传承 手艺中国',
                'description': '汇集苏绣、景德镇瓷器、剪纸、篆刻等传统技艺，展示中国工匠精神。',
                'curator': '国家博物馆',
                'project_names': ['苏绣双面绣', '景德镇青花瓷', '陕北剪纸艺术', '吴昌硕篆刻艺术'],
                'status': 'published',
            },
            {
                'title': '岁时节令——中华传统节日文化展',
                'subtitle': '春生夏长 秋收冬藏',
                'description': '通过春节、端午等传统节日，展示中华民族的时间观念和文化传统。',
                'curator': '民俗博物馆',
                'project_names': ['春节习俗', '端午节习俗'],
                'status': 'published',
            },
        ]

        for exh_data in exhibitions_data:
            exhibition, created = Exhibition.objects.get_or_create(
                title=exh_data['title'],
                defaults={
                    'subtitle': exh_data['subtitle'],
                    'description': exh_data['description'],
                    'curator': exh_data['curator'],
                    'status': exh_data['status'],
                }
            )
            for idx, proj_name in enumerate(exh_data['project_names']):
                project = HeritageProject.objects.filter(name=proj_name).first()
                if project:
                    ExhibitionItem.objects.get_or_create(
                        exhibition=exhibition,
                        project=project,
                        defaults={
                            'section_title': f'第{idx+1}单元',
                            'sort_order': idx,
                        }
                    )
        self.stdout.write(self.style.SUCCESS(f'已创建/更新 {len(exhibitions_data)} 个专题展陈'))
        self.stdout.write(self.style.SUCCESS('示例数据初始化完成！'))
