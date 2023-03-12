from twibo_server.model.blog import BlogModel, CommentModel
from twibo_server.lib.exception import ParameterError
from twibo_server.lib.user import User
from twibo_server.config import config
from twibo_server.utils import logger
from twibo_server.utils import generate_id
from twibo_server import socketIO

import os


class Blog:
    def __init__(self, blog_id):
        self.blog_id = blog_id
        self._model = None

    @property
    def model(self):
        if not self._model:
            model = BlogModel.get(self.blog_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'blog not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    @property
    def author(self):
        return User(self.model.author)

    @classmethod
    def create(cls, data, user_id):
        if user_id != data['author']:
            raise ParameterError(400, 'Access denied!')
        BlogModel(**data).save()
        return

    def update(self, data, user_id):
        if user_id != self.model.author:
            raise ParameterError(400, 'Access denied!')

        title = data.get('title')
        content = data.get('content')
        abstract = data.get('abstract')
        if title:
            self.model.title = title
        if content:
            self.model.content = content
        if abstract:
            self.model.abstract = abstract

        self.model.save()

    def delete(self, user_id):
        if user_id != self.model.author:
            raise ParameterError(400, 'Access denied!')
        CommentModel.delete_all(self.blog_id)
        self.model.delete()

    @classmethod
    def upload_image(cls, file):
        base_path = config.blog_img_url
        suffix = file.filename.split('.')[-1]
        if suffix not in config.img_type:
            raise ParameterError(400, f'不支持文件格式 .{suffix}')

        name = generate_id('blog-img')

        file_name = name + '.' + suffix
        file_path = os.path.join(base_path, file_name)
        file.save(file_path)
        return file_name

    def get_one(self, user_id):
        user = User(user_id)
        blog_info = self.model.to_json()
        blog_info['comments'] = self.get_comments(user)
        blog_info['author'] = self.author.to_json()
        return blog_info

    @classmethod
    def get_blogs(cls, user_id, keyword='', page_size=10, page_num=0):
        total = BlogModel.get_total_cnt(keyword)
        blogs = BlogModel.get_blogs(keyword, page_size, page_num)
        friends = User(user_id).friends

        abstracts = []
        for blog in blogs:
            b = blog.to_json()
            info = {
                'title': b['title'],
                'blog_id': b['blog_id'],
                'time': b['time'],
                'abstract': b['abstract'],
                'author': friends.get(b['author']) or User.get_user(b['author']),
                'stats': BlogModel.get_stats(b['blog_id'])
            }
            abstracts.append(info)
        return abstracts, total

    def get_comments(self, user):
        comments_list = []
        comments = CommentModel.get_all(self.blog_id)
        for comment in comments:
            com = comment.to_json()
            comments_list.append(com)
        return comments_list

    def add_comment(self, data):
        comment_type = data.get('type', CommentModel.PLAIN)
        comment = {
            'blog_id': self.blog_id,
            'author': data['user_id'],
            'content': data.get('content', ''),
            'comment_type': comment_type
        }
        CommentModel(**comment).save()

        # socketIO.emit('like', data, namespace='/twibo')
