# 非遗数字档案展示与检索系统

基于 Django + Elasticsearch + MySQL + Bootstrap 的非物质文化遗产数字档案管理系统。

## 功能特性

- **非遗项目资料录入**: 通过 Django Admin 后台录入项目基础信息、历史渊源、传承内容等
- **多媒体展示**: 支持图片、视频、音频、文档等多种多媒体资源的管理与展示
- **标签分类**: 非遗类别与标签双重分类体系，灵活组织内容
- **全文检索**: 基于 Elasticsearch 的全文检索系统，支持模糊搜索和关键词高亮
- **专题展陈**: 创建专题展览，按策展逻辑组织非遗项目
- **响应式界面**: 基于 Bootstrap 5 的响应式设计，适配多端设备

## 技术栈

- **后端框架**: Django 4.2
- **数据库**: MySQL 8.0+
- **搜索引擎**: Elasticsearch 7.x
- **前端框架**: Bootstrap 5.3
- **Python 版本**: Python 3.9+

## 目录结构

```
.
├── archive/                    # 核心应用
│   ├── management/
│   │   └── commands/
│   │       └── init_sample_data.py  # 初始化示例数据
│   ├── migrations/             # 数据库迁移文件
│   ├── admin.py                # 后台管理配置
│   ├── apps.py                 # 应用配置
│   ├── documents.py            # Elasticsearch 文档定义
│   ├── models.py               # 数据模型
│   ├── search.py               # 搜索服务
│   ├── signals.py              # 信号处理
│   ├── urls.py                 # URL 路由
│   └── views.py                # 视图函数
├── cultural_heritage/          # 项目配置
│   ├── settings.py             # 项目配置
│   ├── urls.py                 # 根 URL 路由
│   ├── asgi.py                 # ASGI 配置
│   └── wsgi.py                 # WSGI 配置
├── media/                      # 媒体文件上传目录
├── static/                     # 静态资源
│   ├── css/
│   └── js/
├── templates/archive/          # 模板文件
│   ├── base.html               # 基础模板
│   ├── home.html               # 首页
│   ├── project_list.html       # 项目列表
│   ├── project_detail.html     # 项目详情
│   ├── exhibition_list.html    # 专题展陈列表
│   ├── exhibition_detail.html  # 专题展陈详情
│   ├── category_list.html      # 分类浏览
│   ├── tag_list.html           # 标签云
│   └── search.html             # 搜索结果页
├── manage.py                   # Django 管理脚本
└── requirements.txt            # Python 依赖
```

## 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.9+
- MySQL 8.0+
- Elasticsearch 7.x
- Redis（可选，用于缓存）

### 2. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# macOS/Linux 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE cultural_heritage CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `cultural_heritage/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cultural_heritage',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 配置 Elasticsearch

确保 Elasticsearch 服务已启动，默认地址为 `localhost:9200`。
如需修改，编辑 `cultural_heritage/settings.py`：

```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',
    },
}
```

> **注意**: 如果 Elasticsearch 未启动，系统会自动降级使用数据库的模糊搜索功能。

### 5. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 7. 导入示例数据（可选）

```bash
python manage.py init_sample_data
```

### 8. 重建 Elasticsearch 索引（可选）

```bash
python manage.py search_index --rebuild
```

### 9. 启动开发服务器

```bash
python manage.py runserver
```

访问地址：
- 前台首页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/

## 数据模型说明

| 模型 | 说明 |
|------|------|
| `Category` | 非遗类别（含保护级别、大类等） |
| `Tag` | 标签（自定义颜色） |
| `HeritageProject` | 非遗项目（核心模型） |
| `MediaResource` | 多媒体资源（图片/视频/音频/文档） |
| `Exhibition` | 专题展陈 |
| `ExhibitionItem` | 展陈项目关联表 |

## 主要功能模块

### 1. 资料录入
登录管理后台后，可以录入：
- 非遗项目的完整信息
- 项目相关的多媒体资源
- 标签和分类信息
- 专题展陈内容

### 2. 多媒体展示
- 图片画廊：支持点击放大查看
- 视频播放：支持 MP4 等常见格式
- 音频播放：支持 MP3 等格式
- 文档下载：支持 PDF、Word 等文档

### 3. 全文检索
- 支持项目名称、内容、传承人等多字段搜索
- 支持按类别、标签筛选
- 自动补全提示
- Elasticsearch 不可用时自动降级为数据库搜索

### 4. 专题展陈
- 创建专题展览
- 自定义展陈章节
- 按策展逻辑排序项目

## 常见问题

### Q: 没有安装 MySQL，可以使用 SQLite 吗？
A: 可以。修改 `settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Q: Elasticsearch 启动报错怎么办？
A: 系统已内置降级方案，Elasticsearch 不可用时会自动使用数据库的 LIKE 查询，不影响核心功能。

## 许可证

本项目仅供学习和研究使用。
