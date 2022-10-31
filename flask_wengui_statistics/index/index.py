"""General page routes."""

from gpiozero import LED, Buzzer, LEDBoard, RGBLED

from enum import IntEnum, unique
import json
import string
import random
from flask import Blueprint, url_for, render_template, request, redirect

from .. import db
from .. import app_ref

from ..dashboard.model_video_submit import VideoSubmit
from ..auth.model_account import Account
from ..auth.model_theme import Theme
from ..auth.model_account_type import AccountType
from ..auth.model_account_status import AccountStatus

from ..dashboard.model_category import Category
from ..dashboard.model_submit_status import VideoSubmitStatus
from ..dashboard.model_video import Video
from ..dashboard.model_operation import Operation
from ..dashboard.model_account_operation import AccountOperation

from ..dashboard.model_music import Music
from ..dashboard.model_stream import Stream
from ..dashboard.model_website import Website

from ..auth.model_white import WhiteIP
from ..auth.model_black import BlackIP


# Enable Before PUSH

from .. import IoT_Enable
if IoT_Enable:
    myLED = LED(24)
    myRelay = LED(18)
    myBuzzer = Buzzer(14)
    myLED_ARRAY = LEDBoard(5, 6, 13, 1, 12, 16, 20, 21, 19, 26)


# Blueprint Configuration
index_bp = Blueprint(
    "index_bp", __name__, template_folder="templates", static_folder="static"
)


def account_num():
    # account_type = AccountType.query.filter_by(
    #     name="积分申报战队").first()
    # team_accounts = Account.query.filter_by(account_type=account_type).all()
    accounts = Account.query.all()
    return len(accounts)


def data_init():
    from .. import account_frame, submit_frame
    from ..dashboard.model_video_submit import E_SUBMIT_TYPE

    account_themes = account_frame['themes']
    account_types = account_frame['types']
    account_status = account_frame['status']
    account_tests = account_frame['account_tests']

    # submit_types = ["视频", "音乐", "直播", "网站"]
    categories = [{'name': category['name'], 'value': category['value']}
                  for category in submit_frame['options']]

    # video_types = ["微视频", "简化视频", "引述结构视频", "创作结构视频", "纪录片", "应急视频", "访谈视频"]
    videoes = [{'name': video['name'], 'point': video['point']}
               for video in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options']]

    # video_mic_ops: 微视频,
    # 微视频<策划<微视频>, 文案编辑<微视频>, 文案审核<微视频>, 配音<微视频>, 翻译<微视频>, 翻译校对<微视频>>

    # video_sim_ops: 简化视频,
    # video_ref_ops: 引述结构视频,
    # video_crt_ops: 创作结构视频,
    # video_rcd_ops: 纪录片,
    # video_ugt_ops: 应急视频,
    # video_cht_ops: 访谈视频
    #
    # video_ops = [type['name']
    #              for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .MIC_VIDEO]['options']]+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .SIM_VIDEO]['options']])+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .REF_VIDEO]['options']])+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .CRT_VIDEO]['options']])+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .RCD_VIDEO]['options']])+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .UGT_VIDEO]['options']])+([type['name'] for type in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .CHT_VIDEO]['options']])
    #
    # # #
    musics = [{'name': music['name'], 'point': music['point']}
              for music in submit_frame['options'][E_SUBMIT_TYPE.MUSIC]['options']]

    streams = [{'name': stream['name'], 'point': stream['point']}
               for stream in submit_frame['options'][E_SUBMIT_TYPE.STREAM]['options']]

    websites = [{'name': website['name'], 'point': website['point']}
                for website in submit_frame['options'][E_SUBMIT_TYPE.WEBSITE]['options']]

    submit_status = submit_frame['status']

    submit_tests = submit_frame['submit_tests']

    return [account_themes, account_status, account_types, account_tests, categories, videoes, musics, streams, websites, submit_status, submit_tests]


def ip_init():
    from ..index.model_ip import IP
    from urllib.request import urlopen

    ips = IP.query.all()
    if not ips:
        request_url = 'https://ipapi.co/{}/json'.format(
            '8.8.8.8')+'/?key=QCM5ry3Xw1kC1xrNrXZKzaZRXhhxywi67F8eSTgVDnnSMn64Lu'

        # store the response of URL
        response = urlopen(request_url)

        # storing the JSON response
        # from url in data
        data_json = json.loads(response.read())

        ip = IP(
            page='Google',

            ip=data_json['ip'],
            city=data_json['city'],
            region=data_json['region'],
            country_name=data_json['country_name'],
            country_capital=data_json['country_capital'],
            timezone=data_json['timezone'],
            latitude=data_json['latitude'],
            longitude=data_json['longitude'],
            org=data_json['org'],

            browser='N'
        )
        db.session.add(ip)
    db.session.commit()


def ip_white_init():
    '''IP白名单'''
    results = WhiteIP.query.all()
    if not results:
        ips_white = ['50.72.43.125']
        for ip in ips_white:
            _ip = WhiteIP(ip=ip, note=u'开发人员')
            db.session.add(_ip)
        db.session.commit()


def ip_black_init():
    '''IP黑名单'''
    results = BlackIP.query.all()
    if not results:
        ips_white = ['39.156.66.10']
        for ip in ips_white:
            _ip = BlackIP(ip=ip, note=u'百度')
            db.session.add(_ip)
        db.session.commit()


def account_theme_init(themes):
    '''账号主题初始化'''
    results = Theme.query.all()
    if not results:
        for theme in themes:
            theme = Theme(name=theme)
            db.session.add(theme)
        db.session.commit()


def account_status_init(status):
    '''账号状态初始化'''
    results = AccountStatus.query.all()
    if not results:
        for status in status:
            status = AccountStatus(name=status)
            db.session.add(status)
        db.session.commit()


def account_type_init(types):
    '''账号类型初始化'''
    results = AccountType.query.all()
    if not results:
        for type in types:
            type = AccountType(name=type)
            db.session.add(type)
        db.session.commit()


def account_init(account_tests):
    '''账号初始化'''
    results = Account.query.all()
    if not results:
        # for account in accounts:
        # for idx, account in enumerate(accounts):
        for account in account_tests:
            if "个人" in account['name']:
                account_type = AccountType.query.filter_by(
                    name="积分申报个人").first()
                member = None
            elif "成员" in account['name']:
                account_type = AccountType.query.filter_by(
                    name="积分申报成员").first()
                member = Account.query.filter_by(name="战队测试1").first()
            elif "战队" in account['name']:
                account_type = AccountType.query.filter_by(
                    name="积分申报战队").first()
                member = None
            elif "管理" in account['name']:
                account_type = AccountType.query.filter_by(
                    name="积分申报管理").first()
                member = None
            else:
                account_type = AccountType.query.filter_by(
                    name="数据库管理员").first()
                member = None
            new_account = Account(name=account['name'],
                                  team_name=account['team_name'],
                                  email=account['email'],
                                  theme=Theme.query.filter_by(
                                      name='浅色').first(),
                                  account_status=AccountStatus.query.filter_by(
                                      name='正常').first(),
                                  member=member,
                                  account_type=account_type)

            new_account.set_password(account['password'])
            db.session.add(new_account)
            # if account['team_name'] != None:
            #     new_account.team_id = new_account.id
        db.session.commit()

        # account_type = AccountType.query.filter(
        #     AccountType.name.like('%战队%')).first()
        # teams = Account.query.filter_by(account_type=account_type).all()
        # for team in teams:
        #     db.session.query(Account).filter_by(id=team.id).update(
        #         {"team_id": team.id}, synchronize_session=False)

        account_type = AccountType.query.filter(
            AccountType.name.like('%成员%')).first()
        members = Account.query.filter_by(account_type=account_type).all()
        for member in members:
            if not not member.team_id:
                team = Account.query.get(member.team_id)
                db.session.query(Account).filter_by(id=member.id).update(
                    {"team_name": team.team_name}, synchronize_session=False)

        db.session.commit()


def category_init(categories):
    '''作品类别初始化'''
    results = Category.query.all()
    if not results:
        for category in categories:
            new_category = Category(
                name=category['name'])
            db.session.add(new_category)
        db.session.commit()


def submit_status_init(status):
    '''提交状态初始化'''
    results = VideoSubmitStatus.query.all()
    if not results:
        for status in status:
            new_status = VideoSubmitStatus(name=status)
            db.session.add(new_status)
        db.session.commit()


def video_init(videoes):
    '''视频类型初始化'''
    results = Video.query.all()
    if not results:
        from .. import submit_frame
        from ..dashboard.model_video_submit import E_SUBMIT_TYPE
        category = Category.query.filter(Category.name.like(
            submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['name'])).first()
        for video in videoes:
            new_video = Video(name=video['name'],
                              point=video['point'], category=category)
            db.session.add(new_video)
        db.session.commit()


def music_init(musics):
    '''音乐类型初始化'''
    results = Music.query.all()
    if not results:
        from .. import submit_frame
        from ..dashboard.model_video_submit import E_SUBMIT_TYPE
        category = Category.query.filter(Category.name.like(
            submit_frame['options'][E_SUBMIT_TYPE.MUSIC]['name'])).first()
        for music in musics:
            new_music = Music(name=music['name'],
                              point=music['point'], category=category)
            db.session.add(new_music)
        db.session.commit()


def stream_init(streams):
    '''直播类型初始化'''
    results = Stream.query.all()
    if not results:
        from .. import submit_frame
        from ..dashboard.model_video_submit import E_SUBMIT_TYPE
        category = Category.query.filter(Category.name.like(
            submit_frame['options'][E_SUBMIT_TYPE.STREAM]['name'])).first()
        for stream in streams:
            new_stream = Stream(name=stream['name'],
                                point=stream['point'], category=category)
            db.session.add(new_stream)
        db.session.commit()


def website_init(websites):
    '''网站类型初始化'''
    results = Website.query.all()
    if not results:
        from .. import submit_frame
        from ..dashboard.model_video_submit import E_SUBMIT_TYPE
        category = Category.query.filter(Category.name.like(
            submit_frame['options'][E_SUBMIT_TYPE.WEBSITE]['name'])).first()
        for website in websites:
            new_website = Website(name=website['name'],
                                  point=website['point'], category=category)
            db.session.add(new_website)
        db.session.commit()


def video_ops_init():
    '''视频操作初始化'''
    results = Operation.query.all()
    if not results:
        from .. import submit_frame
        from ..dashboard.model_video_submit import E_SUBMIT_TYPE
        from ..dashboard.model_video import E_VIDEO_TYPE

        video = Video.query.filter(
            Video.name.like('微视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .MIC_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('简化视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .SIM_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('引述结构视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .REF_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('创作结构视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .CRT_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('纪录片')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .RCD_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('应急视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .UGT_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
            # db.session.commit()
        #
        video = Video.query.filter(
            Video.name.like('访谈视频')).first()
        video_ops = [{'name': op['name'], 'weight': op['weight']}
                     for op in submit_frame['options'][E_SUBMIT_TYPE.VIDEO]['options'][E_VIDEO_TYPE .CHT_VIDEO]['options']]
        for op in video_ops:
            op_type = Operation(
                name=op['name'], weight=op['weight'], video=video)
            db.session.add(op_type)
        db.session.commit()


def submit_init(submit_tests):
    results = VideoSubmit.query.all()
    if not results:
        # for account in accounts:
        # categories = Category.query.all()
        category = Category.query.filter(
            Category.name.like('视频')).first()
        submit_status = VideoSubmitStatus.query.filter(
            VideoSubmitStatus.name.like('%待审核%')).first()
        # search = "%{}%".format('成员')
        account = Account.query.filter(Account.name.like('%战队%')).first()

        from pypinyin import pinyin, lazy_pinyin, Style
        team_initials = pinyin(account.team_name, style=Style.FIRST_LETTER)

        for idx, submit in enumerate(submit_tests):
            new_submit = VideoSubmit(
                title=submit['title'],
                global_code='NFSC-'+str(idx).zfill(6),
                # team_code=''.join(random.choices(
                #     string.ascii_uppercase, k=3)) + '-' + ''.join(random.choices(string.digits, k=5)),
                team_code=(''.join(i[0].upper() for i in team_initials))[
                    0:3:1]+'-'+(str(len(results)+idx).zfill(4)),
                category=category,
                length=submit['length'],
                link=submit['link'],
                disk_link=submit['disk_link'],
                comment=submit['comment'],
                submit_status=submit_status,
                account=account)
            db.session.add(new_submit)
        db.session.commit()


def table_init():
    [account_themes, account_status, account_types, account_tests, categories, videoes,
     musics, streams, websites, submit_status, submit_tests] = data_init()

    account_theme_init(account_themes)
    account_status_init(account_status)
    account_type_init(account_types)
    #
    account_init(account_tests)
    #
    category_init(categories)
    submit_status_init(submit_status)
    #
    video_init(videoes)
    music_init(musics)
    stream_init(streams)
    website_init(websites)

    video_ops_init()

    ip_init()

    ip_white_init()
    ip_black_init()
    #
    submit_init(submit_tests)


@unique
class E_IP_TYPE (IntEnum):
    WHITE = 0
    BLACK = 1
    NORMAL = 2


def record_notice(request):
    from netaddr import IPAddress
    from ..index.model_ip import IP
    from .record_notice import record_save

    # return E_IP_TYPE .BLACK

    # Enable Before PUSH

    ip = request.remote_addr
    # ip = '8.8.8.8'

    if IPAddress(ip).is_private() or IPAddress(ip).is_loopback():
        return

    if bool(WhiteIP.query.filter_by(ip=ip).first()):
        return E_IP_TYPE .WHITE

    if bool(BlackIP.query.filter_by(ip=ip).first()):
        return E_IP_TYPE .BLACK

    record_save(ip)
    return E_IP_TYPE .NORMAL


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    # Enable Before PUSH
    from .. import IoT_Enable
    if IoT_Enable:
        myLED.toggle()
        myRelay.toggle()
        myLED_ARRAY.toggle()
    """Homepage."""
    # trusted_hosts: t.Optional[t.List[str]] = None
    # iii = request.remote_addr

    if (record_notice(request) == E_IP_TYPE .BLACK):
        return redirect("https://www.google.com/")

    return render_template(
        "index.jinja2",
        title="战友(战队)灭共任务统计网页应用",
        template="main-template",
        team="新中国联邦灭共技术支持小组",
        login=url_for('auth_bp.login'),
    )
