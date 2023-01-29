from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server import socketIO
from twibo_server.lib.blog import Blog
from twibo_server.utils import logger


@bp.route('/blogs', methods=['POST'])
@login_required
def create_blog():
    data = request.get_json()
    Blog.create(data, g.user_id)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/blogs/<blog_id>', methods=['PATCH'])
@login_required
def update_blog(blog_id):
    data = request.get_json()
    Blog(blog_id).update(data, g.user_id)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/blogs/<blog_id>', methods=['DELETE'])
@login_required
def delete_blog(blog_id):
    Blog(int(blog_id)).delete(g.user_id)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/blogs/image', methods=['POST'])
@login_required
def upload_blog_image():
    file = request.files.get('file')
    name = Blog.upload_image(file)
    return jsonify(meta={'code': 200}, data={'url': name})


@bp.route('/blogs', methods=['GET'])
@login_required
def get_blogs():
    size = request.args.get('page_size', 10)
    page = request.args.get("page", 0)
    keyword = request.args.get("keyword", '')
    blogs, total = Blog.get_blogs(g.user_id, keyword=keyword, page_size=int(size), page_num=int(page))
    res = {
        'blogs': blogs,
        'total': total
    }
    return jsonify(meta={'code': 200}, data=res)


@bp.route('/blogs/<blog_id>', methods=['GET'])
@login_required
def get_one_blog(blog_id):
    data = Blog(blog_id).get_one(g.user_id)
    return jsonify(meta={'code': 200}, data=data)


@socketIO.on('like', namespace='/twibo')
def like_blog(data):
    blog_id = data['blog_id']
    Blog(blog_id).add_comment(data)