"""Initialize Flask app."""
import textwrap
import os
import os.path as path


from datetime import timedelta

from flask import Flask, session, render_template
from flask_assets import Environment

from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import datetime


# PUSH_PUSH
IoT_Enable = False

account_frame = {
    "__name__": "account_frame",
    "themes": ["Light Color", "Deep Color"],
    "types": ["积分申报个人", "积分申报成员", "积分申报战队", "积分申报管理", "Number据库管理员"],
    "status": ["Normal", "挂起", "只读", "锁定"],
    "account_tests": [{"name": "Test Database", "team_name": None, "email": "data_admin@gmail.com",
                       "password": "111111"},
                      {"name": "管理测试", "team_name": None, "email": "admin@gmail.com",
                          "password": "111111"},
                      #
                      {"name": "战队测试1", "team_name": "Team1", "email": "team1@gmail.com",
                          "password": "111111"},
                      {"name": "战队测试2", "team_name": "地之水战队", "email": "team2@gmail.com",
                          "password": "111111"},
                      #
                      {"name": "成员测试1", "team_name": None, "email": "member1@gmail.com",
                          "password": "111111"},
                      {"name": "成员测试2", "team_name": None, "email": "member2@gmail.com",
                          "password": "111111"},
                      {"name": "成员测试3", "team_name": None, "email": "member3@gmail.com",
                          "password": "111111"},
                      {"name": "成员测试4", "team_name": None, "email": "member4@gmail.com",
                          "password": "111111"},
                      {"name": "成员测试5", "team_name": None, "email": "member5@gmail.com",
                          "password": "111111"},
                      {"name": "成员测试6", "team_name": None, "email": "member6@gmail.com",
                          "password": "111111"},
                      #
                      {"name": "个人测试1", "team_name": None, "email": "personal1@gmail.com",
                       "password": "111111"},
                      {"name": "个人测试2", "team_name": None, "email": "personal2@gmail.com",
                       "password": "111111"}]
}


submit_frame = {
    "__name__": "submit_frame",
    "status": ["已提交", "待审核", "通过", "退回"],
    "submit": False,
    "submit_tests": [{"title": "Video标题1", "point": 100,
                      "link": "https://www.google.ca/",
                      "disk_link": "https://www.google.ca/", "length": 3670, "comment": "备注1"},
                     {"title": "Video标题2", "point": 200,
                      "link": "https://www.google.ca/",
                      "disk_link": "https://www.google.ca/", "length": 3500, "comment": "备注2"},
                     {"title": "Video标题3", "point": 300,
                      "link": "https://www.google.ca/",
                      "disk_link": "https://www.google.ca/", "length": 1800, "comment": "备注3"},
                     {"title": "Video标题4", "point": 400,
                      "link": "https://www.google.ca/",
                      "disk_link": "https://www.google.ca/", "length": 50, "comment": "备注4"}],
    "options": [{
        "submit": False,
        "level": 1,
        "value": 1,
        "name": "Video",
        # "point": 1000,
        "options": [{
            "submit": False,
            "level": 2,
            "value": 1,
            "name": "Tiny Video",
            "point": 500,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<Tiny Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<Tiny Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<Tiny Video>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<Tiny Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<Tiny Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<Tiny Video>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 2,
            "name": "Simplified Video",
            "point": 550,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<Simplified Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<Simplified Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<Simplified Video>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<Simplified Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<Simplified Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<Simplified Video>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 3,
            "name": "State StructuredVideo",
            "point": 600,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<State StructuredVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<State StructuredVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<State StructuredVideo>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<State StructuredVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<State StructuredVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<State StructuredVideo>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 4,
            "name": "Create StructedVideo",
            "point": 650,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<Create StructedVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<Create StructedVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<Create StructedVideo>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<Create StructedVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<Create StructedVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<Create StructedVideo>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 5,
            "name": "Documentary",
            "point": 700,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<Documentary>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<Documentary>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<Documentary>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<Documentary>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<Documentary>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<Documentary>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 6,
            "name": "EmergencyVideo",
            "point": 750,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<EmergencyVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<EmergencyVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<EmergencyVideo>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<EmergencyVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<EmergencyVideo>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<EmergencyVideo>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }, {
            "submit": False,
            "level": 2,
            "value": 7,
            "name": "Interview Video",
            "point": 800,
            "code": "",
            "v_name": "",
            "length": "",
            "link": "",
            "options": [{
                "submit": True,
                "level": 3,
                "value": 1,
                "name": "Design<Interview Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            },
                {
                "submit": True,
                "level": 3,
                "value": 2,
                "name": "文案编辑<Interview Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 3,
                "name": "文案审核<Interview Video>",
                "quality": [1, 2, 3],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 4,
                "name": "配音<Interview Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 5,
                "name": "翻译<Interview Video>",
                "quality": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "words": 0,
                "weight": 15,
            }, {
                "submit": True,
                "level": 3,
                "value": 6,
                "name": "翻译校对<Interview Video>",
                "quality": [1, 2, 3],
                "weight": 25,
            }]
        }]
    }, {
        "submit": False,
        "level": 1,
        "value": 2,
        "name": "Music",
        # "point": 1500,
        "options": [{"value": 1, "name": "MusicType1", "point": 500, "submit": False},
                    {"value": 2, "name": "MusicType2", "point": 550, "submit": False}]
    }, {
        "submit": False,
        "level": 1,
        "value": 3,
        "name": "Stream",
        # "point": 2000,
        "options": [{"value": 1, "name": "StreamType1", "point": 500, "submit": False},
                    {"value": 2, "name": "StreamType2", "point": 550, "submit": False}]
    }, {
        "submit": False,
        "level": 1,
        "value": 4,
        "name": "IT Development",
        # "point": 2500,
        "options": [{"value": 1, "name": "IT DevelopmentType1", "point": 500, "submit": False},
                    {"value": 2, "name": "IT DevelopmentType2", "point": 550, "submit": False}]
    }
    ]
}


def current_year():
    return (datetime.date.today()).strftime("%Y")


def count_number(countable):
    return len(countable)


def access_sum(records):
    sum = 0
    for record in records:
        sum += record.total
    return sum


def get_notice():
    # global notice
    # print(session["select_06"])
    file_notice = os.path.join(os.path.dirname(__file__), 'notice.txt')

    with open(file_notice, 'r', encoding='utf-8') as f:
        notice = f.readline()
        if notice.startswith('#'):
            notice = ''

    return notice


def get_count(iterables):
    return len(iterables)


def text_short(text, width, placeholder):
    return text[:width] + textwrap.shorten(text=text[width:], width=width, placeholder=placeholder)

# 	Design, 文案编辑, 文案审核, 配音, 翻译, 翻译校对


def account_operation_points(submit, keyword):
    act_opts = submit.account_operations
    if not act_opts:
        return ''

    for act_opt in act_opts:
        if keyword in act_opt.operation.name:
            # print(act_opt.operation.name)
            return act_opt.account.name + '/' + str(act_opt.point)
    return ''


def my_operation_points(submit, keyword, is_member):
    from flask_login import current_user

    act_opts = submit.account_operations
    if not act_opts:
        return ''

    if is_member:
        for act_opt in act_opts:
            if act_opt.account_id == current_user.id and keyword in act_opt.operation.name:
                return str(act_opt.point)
        return ''
    else:
        for act_opt in act_opts:
            if keyword in act_opt.operation.name:
                return str(act_opt.point)
        return ''


def account_points(submit, keyword):
    act_opts = submit.account_operations
    if not act_opts:
        return ['', '']

    for act_opt in act_opts:
        if keyword in act_opt.operation.name:
            # print(act_opt.operation.name)
            return [act_opt.account.name, str(act_opt.point)]
    return ['', '']


def team_points(team):
    submits = team.submits
    total = 0
    for submit in submits:
        if submit.submit_status.name == "通过":
            for act_opt in submit.account_operations:
                total += act_opt.point
    return total


def my_points(submits, is_member):
    from flask_login import current_user

    total_points = 0
    if submits is None:
        return 0

    if is_member:
        for submit in submits:
            if submit.submit_status.name == "通过":
                for act_opt in submit.account_operations:
                    if act_opt.account_id == current_user.id:
                        total_points += act_opt.point
        return total_points
    else:
        for submit in submits:
            if submit.submit_status.name == "通过":
                for act_opt in submit.account_operations:
                    total_points += act_opt.point
        return total_points


def member_points(member):
    from .auth.model_account import Account

    team = Account.query.get(member.team_id)
    submits = team.submits
    total = 0
    for submit in submits:
        if submit.submit_status.name == "通过":
            for act_opt in submit.account_operations:
                if act_opt.account_id == member.id:
                    total += act_opt.point
    return total


utils = {'get_count': get_count,
         'access_sum': access_sum,
         'get_notice': get_notice,
         'text_short': text_short,
         'count_number': count_number,
         'current_year': current_year,
         'team_points': team_points,
         'my_points': my_points,
         'member_points': member_points,
         'my_operation_points': my_operation_points,
         'account_operation_points': account_operation_points}

db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    global app_ref
    app_ref = app

    assets = Environment()

    # app.jinja_env.globals.update(current_year=current_year)
    # app.jinja_env.globals.update(count_number=count_number)
    app.jinja_env.globals.update(utils=utils)

    # Initialize Plugins
    assets.init_app(app)
    db.init_app(app)

    #
    login_manager.needs_refresh_message = (
        u"Call Fail Login Again")
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=5)

    sess.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .assets import compile_static_assets
        from .index import index
        # from .login import login
        from .auth import auth
        from .dashboard import dashboard, dashboard_api
        # from .home import home
        # from .products import products
        # from .profile import profile

        # Register Blueprints
        app.register_blueprint(index.index_bp)
        # app.register_blueprint(login.auth_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(dashboard.dashboard_bp)

        app.register_blueprint(dashboard_api._dashboard_bp)
        # app.register_blueprint(profile.profile_bp)
        # app.register_blueprint(home.home_bp)
        # app.register_blueprint(products.product_bp)

        # Create Database Models
        if app.config["FLASK_ENV"] == "development":
            print('😍开发模式清除，重建Number据库😍')
            db.drop_all()
        db.create_all()

        # from ..dashboard import z_page_not_found
        app.register_error_handler(404, page_not_found)

        from .index.index import table_init
        table_init()

        # Compile static assets
        compile_static_assets(assets)

        return app


# @dashboard_bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('page_not_found.html'), 404
