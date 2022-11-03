"""Routes for user authentication."""


from flask import jsonify
from operator import truediv
import re
from tokenize import Name
from ..dashboard.model_operation import Operation
from ..dashboard.model_video import Video
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..dashboard.model_submit_status import VideoSubmitStatus
# from flask_wengui_statistics.index.index import account_status_init, account_type_init
from ..auth.model_account import Account
from ..auth.model_account_type import AccountType
from ..auth.model_account_status import AccountStatus

from ..auth.model_theme import Theme
from ..index.index import record_notice

from .model_category import Category
from .model_video import Video
from .model_video_submit import VideoSubmit
from .model_account_operation import AccountOperation
from ..index.model_ip import IP

from .form import TypeForm, SettingForm, VideoSubmitForm, StatusForm, AuditForm, WeightForm, PointForm, BackupForm, BWListForm, CreateForm
from .. import db
# from flask_wengui_statistics.index.index import submit_types
from pypinyin import pinyin, Style
import shutil
import datetime

from sqlalchemy import func, desc

from .. import submit_frame

from ..index.index import account_num
from enum import IntEnum, unique


@unique
class E_ACCOUNT_TYPE(IntEnum):
    TEAM = 0
    MEMBER = 1
    PERSONAL = 2
    ADMIN = 3
    DATA_ADMIN = 4

# ["Tiny Video", "Simplified Video", "State StructuredVideo", "Create StructedVideo", "Documentary", "EmergencyVideo", "Interview Video"]


# Blueprint Configuration
dashboard_bp = Blueprint(
    "dashboard_bp", __name__, template_folder="templates", static_folder="static")

_submit_v1v2, _submit_v3, g_submit_list, g_vars_list, _g_account_type = None, None, None, None, None


@login_required
def dashboard_init():
    global _g_account_type

    # Enable Before PUSH
    from .. import IoT_Enable
    if IoT_Enable:
        from ..index.index import myLED, myRelay, myLED_ARRAY
        myLED.toggle()
        myRelay.toggle()
        myLED_ARRAY.toggle()

    # theme = "dark" if current_user.theme.name == "Deep Color" else "white?"
    # back = "dashboard_bp.dashboard"
    # g_variables["theme"] = "dark" if current_user.theme.name == "Deep Color" else "white?"

    # global submit_idx
    # g_vars_list[submit_idx]["theme"] = "dark" if current_user.theme.name == "Deep Color" else "white?"
    if current_user.account_type.name == "积分申报个人":
        _g_account_type = E_ACCOUNT_TYPE.PERSONAL
        menu = [{"icon": "bx bx-cloud-upload icon", "isize": '28px',
                 "url": "dashboard_bp.submit_v1v2", "text": "积分申报v1", "active": True},
                {"icon": "bx bx-credit-card-front icon", "isize": '28px',
                 "url": "dashboard_bp.point", "text": "My Point", "active": True},
                {"icon": "bx bxs-cog icon", "isize": '28px',
                 "url": "dashboard_bp.setting", "text": "My Setting", "active": True},
                {"icon": "bx bx-run bx-flip-horizontal icon", "isize": '28px',
                 "url": "auth_bp.logout", "text": "Logout", "active": True}]
    elif current_user.account_type.name == "积分申报成员":
        _g_account_type = E_ACCOUNT_TYPE.MEMBER
        menu = [  # {"icon": "bx bx-cloud-upload icon", "isize": '28px',
            #  "url": "dashboard_bp.submit_v1v2", "text": "积分申报v1", "active": True},
            {"icon": "bx bx-credit-card-front icon", "isize": '28px',
             "url": "dashboard_bp.point", "text": "My Point", "active": True},
            {"icon": "bx bxs-cog icon", "isize": '28px',
             "url": "dashboard_bp.setting", "text": "My Setting", "active": True},
            {"icon": "bx bx-run bx-flip-horizontal icon", "isize": '28px',
             "url": "auth_bp.logout", "text": "Logout", "active": True}]
    elif current_user.account_type.name == "积分申报战队":
        _g_account_type = E_ACCOUNT_TYPE.TEAM
        menu = [{"icon": "bx bx-cloud-upload icon", "isize": '28px',
                 "url": "dashboard_bp.submit_v1v2", "text": "Point Reportv2", "active": True},
                {"icon": "bx bxs-user-detail icon", "isize": '28px',
                 "url": "dashboard_bp.member", "text": "Team Member", "active": True},
                {"icon": "bx bxs-cog icon", "isize": '28px',
                 "url": "dashboard_bp.setting", "text": "My Setting", "active": True},
                {"icon": "bx bx-run bx-flip-horizontal icon", "isize": '28px',
                 "url": "auth_bp.logout", "text": "Logout", "active": True}]

    elif current_user.account_type.name == "积分申报管理":
        _g_account_type = E_ACCOUNT_TYPE.ADMIN
        menu = [{"icon": "bx bx-cloud-upload icon", "isize": '28px',
                 "url": "dashboard_bp.submit_v3", "text": "Point Reportv3", "active": True},
                {"icon": "bx bxs-user-check icon", "isize": '28px',
                 "url": "dashboard_bp.audit", "text": "In Review", "active": True},
                {"icon": "bx bx-credit-card-front icon", "isize": '28px',
                 "url": "dashboard_bp.summary", "text": "Submit Application", "active": True},
                {"icon": "bx bxs-group icon", "isize": '28px',
                 "url": "dashboard_bp.account", "text": "Account(Type)", "active": True},
                {"icon": "bx bxs-lock-open-alt icon", "isize": '28px',
                 "url": "dashboard_bp.status", "text": "Account(Type)", "active": True},
                {"icon": "bx bxs-circle-three-quarter icon", "isize": '28px',
                 "url": "dashboard_bp.weight", "text": "Weight of Position", "active": True},
                {"icon": "bx bx-code-curly icon", "isize": '28px',
                 "url": "dashboard_bp.pparameter", "text": "Point Weight", "active": True},
                {"icon": "bx bxs-cog icon", "isize": '28px',
                 "url": "dashboard_bp.setting", "text": "My Setting", "active": True},
                {"icon": "bx bx-run bx-flip-horizontal icon", "isize": '28px',
                 "url": "auth_bp.logout", "text": "Logout", "active": True}]
    else:
        _g_account_type = E_ACCOUNT_TYPE.DATA_ADMIN
        menu = [{"icon": "bx bxs-user-rectangle icon", "isize": '28px',
                "url": "dashboard_bp.dashboard", "text": "Manager Dashboard", "active": True},
                # {"icon": "bx bxs-group icon", "isize": '28px',
                #  "url": "dashboard_bp.account", "text": "账号管理(Type)", "active": True},
                # {"icon": "bx bxs-lock-open-alt icon", "isize": '28px',
                #  "url": "dashboard_bp.status", "text": "账号管理(状态)", "active": True},
                {"icon": "bx bxs-folder-plus icon", "isize": '28px',
                 "url": "dashboard_bp.create", "text": "Account Create", "active": True},
                {"icon": "bx bx-transfer icon", "isize": '28px',
                 "url": "dashboard_bp.record", "text": "Login History", "active": True},
                {"icon": "bx bxs-pointer icon", "isize": '28px',
                 "url": "dashboard_bp.auth_list", "text": "List of Invited", "active": True},
                {"icon": "bx bxs-data icon", "isize": '28px',
                 "url": "dashboard_bp.backup", "text": "Backup Database", "active": True},
                {"icon": "bx bxs-cog icon", "isize": '28px',
                 "url": "dashboard_bp.setting", "text": "My Setting", "active": True},
                {"icon": "bx bx-run bx-flip-horizontal icon", "isize": '28px',
                 "url": "auth_bp.logout", "text": "Logout", "active": True}]

    from .. import app_ref
    if app_ref.config["FLASK_ENV"] == "development":
        key_vairbles()

    _vars = g_vars_list[current_user.id-1]
    _vars["theme"] = "dark" if current_user.theme.name == "Deep Color" else "white?"

    # print('🤣', current_user.id)
    return [menu, _vars]


@dashboard_bp.route('/menu_toggle', methods=['GET', 'POST'])
def menu_toggle():
    # session["select_06"] = "😥😥😥😥😥"

    [_, _vars] = dashboard_init()

    if (_vars["menu"] == 'close'):
        _vars["menu"] = 'open'
    else:
        _vars["menu"] = 'close'

    # print('😥😥😥😥😥', _vars["menu"])

    return redirect(request.referrer)


@dashboard_bp.route('/dashboard/create', methods=['GET', 'POST'])
@login_required
def create():
    if not account_type_check(E_ACCOUNT_TYPE.DATA_ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    types = AccountType.query.filter(AccountType.name.like(
        '%申报个人%') | AccountType.name.like('%申报成员%') | AccountType.name.like('%申报战队%') | AccountType.name.like('%申报管理%')).all()
    teams = Account.query.join(AccountType).filter(
        AccountType.name.like('%战队%')).all()

    form = CreateForm()

    form.type.choices = [(0, '-- Account Type --')] + [(type.id, type.name)
                                               for type in types]

    form.team.choices = [(0, '-- Belong Team --')] + [(team.id, team.name)
                                               for team in teams]

    if request.method == 'POST':
        name = form.data['name']
        email = form.data['email']
        password = form.data['password']
        type_id = form.data['type']
        team_id = form.data['team']

        if form.validate_on_submit():
            existing_user = Account.query.filter_by(
                email=email).first()
            if existing_user != None:
                flash(category='error', message=u'Account Exists!')
            else:
                new_account = Account(
                    name=name,
                    # team_name=account['team_name'],
                    email=email,
                    theme=Theme.query.filter_by(
                        name='Light Color').first(),
                    account_status=AccountStatus.query.filter_by(
                        name='Normal').first(),
                    # member=member,
                    account_type_id=type_id,
                    team_id=team_id,
                    team_name=Account.query.get(team_id).team_name)

                new_account.set_password(password)
                db.session.add(new_account)
                db.session.commit()

                key_vairbles_add()
                flash(category='success', message=u'Account{}Created Successfully!'.format(name))
        else:
            flash(category='error', message='Input Error!')
        return redirect(url_for("dashboard_bp.create"))
    return render_template(
        "create.jinja2",

        title="Background Management",
        sub_title="Account Create",

        form=form,
        #
        menu=menu,
        _vars=_vars,

        _height_display='vh'
    )


@dashboard_bp.route('/dashboard/record', methods=['GET'])
@login_required
def record():
    if not account_type_check(E_ACCOUNT_TYPE.DATA_ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    # from ..index.model_ip import IP
    # 1, 所有的
    # records = IP.query.all()

    # 2, ip不一样的
    # records = db.session.query(IP.ip).distinct().all()

    # from sqlalchemy import func, desc
    # # 3, 统计每个IP地址访问的次Number，降序结果， func.count, group_by，desc
    # records = records = IP.query.with_entities(
    #     IP.page,
    #     IP.ip,
    #     IP.city,
    #     IP.city,
    #     IP.region,
    #     IP.country_name,
    #     IP.timezone,
    #     IP.latitude,
    #     IP.longitude,
    #     IP.org,
    #     IP.browser,
    #     IP.time,
    #     func.count(IP.ip).label('total'))\
    #     .group_by(IP.ip)\
    #     .order_by(desc(func.count(IP.ip)))

    # ('35.227.62.178', 'North Charleston', 1)
    # ('50.72.43.125', 'Winnipeg', 2)
    # ('70.80.220.62', 'Montreal', 1)

    # 4, 统计每个IP地址访问的次Number和最近一次访问的时间， func.count, group_by，
    records = IP.query.with_entities(
        IP.page,
        IP.ip,
        IP.city,
        IP.region,
        IP.country_name,
        IP.timezone,
        IP.latitude,
        IP.longitude,
        IP.org,
        IP.browser,
        IP.time,
        func.max(IP.time).label('latest'),
        func.count(IP.ip).label('total'))\
        .group_by(IP.ip, IP.page)\
        .order_by(desc(func.count(IP.ip)))

    # from sqlalchemy.orm import defer
    # from sqlalchemy.orm import undefer

    # # 5, 统计每个IP地址访问的次Number和最近一次访问的时间（undefer('*')），， func.count, group_by，undefer
    # # records = IP.query.options(undefer('*'))
    # records = IP.query.options(undefer('*'))\
    #     .with_entities(func.max(IP.time).label('latest'),
    #                    func.count(IP.ip).label('total'))\
    #     .group_by(IP.ip)\
    #     .order_by(desc(func.count(IP.ip)))

    [menu, _vars] = dashboard_init()

    record_num = records.count() if records != None else 0
    return render_template(
        "record.jinja2",

        title="Login History",
        sub_title="Login History",

        records=records,
        #
        menu=menu,
        _vars=_vars,

        _height_display=('vh' if record_num < 3 else 'auto')
    )


@dashboard_bp.route('/dashboard/*', methods=['GET', 'POST'])
@login_required
def dashboard_theme():
    [menu, _vars] = dashboard_init()

    return render_template(
        "dashboard.jinja2",
        title="后台管理",

        menu=menu,
        _vars=_vars,
        #
        user=current_user,
    )


def key_vairbles():
    global g_submit_list, _submit_v1v2, _submit_v3
    # g_submit_list = [dict() for x in range(account_num())]

    if g_submit_list is None:
        g_submit_list = [list() for x in range(account_num())]

    if _submit_v1v2 is None:
        # _submit_v1v2 = [list() for x in range(account_num())]
        # for i in range(account_num()):
        #     _submit_v1v2[i] = g_submit_list[i]
        _submit_v1v2 = g_submit_list[current_user.id-1]

    if _submit_v3 is None:
        # _submit_v3 = [list() for x in range(account_num())]
        # for i in range(account_num()):
        #     _submit_v3[i] = g_submit_list[i]
        _submit_v3 = g_submit_list[current_user.id-1]

    # g_variables = {'menu': 'open',
    #                'theme': 'white',
    #                'back': 'dashboard_bp.dashboard'}

    global g_vars_list
    if g_vars_list is None:
        g_vars_list = [{'menu': 'open',
                        'theme': 'white',
                        'back': 'dashboard_bp.dashboard'} for x in range(account_num())]


def key_vairbles_add():
    # g_submit_list = [list() for x in range(account_num())]
    g_vars_list.append({'menu': 'open',
                        'theme': 'white',
                        'back': 'dashboard_bp.dashboard'})
    g_submit_list.append(list())


@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
# @dashboard_bp.route("/dashboard/index", methods=["GET"])
@login_required
def dashboard():
    key_vairbles()

    record_notice(request)

    # if _vars is None:
    #     # _vars = [{} for i in range(account_num())]
    #     # for i in range(account_num()):
    #     #     _vars[i] = g_vars_list[i]
    #     _vars = g_vars_list[current_user.id-1]

    # _vars["theme"] = "dark" if current_user.theme.name == "Deep Color" else "white?"

    [menu, _vars] = dashboard_init()

    return render_template(
        "dashboard.jinja2",
        title="后台管理",
        fkccp="Background Management",

        menu=menu,
        _vars=_vars,

        # template="dashboard-template"
        _ccp_display=True,
        _height_display='vh'
    )


@dashboard_bp.route('/dashboard/status', methods=['GET', 'POST'])
@login_required
def status():
    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    """
    状态更改，
    """
    [menu, _vars] = dashboard_init()

    form = StatusForm()
    # # #
    accounts_normal = Account.query.join(AccountStatus).filter(
        AccountStatus.name.like('Normal')).join(AccountType).filter(
        AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报战队')).all()

    accounts_pending = Account.query.join(AccountStatus).filter(
        AccountStatus.name.like('挂起')).join(AccountType).filter(
        AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报战队')).all()

    accounts_read = Account.query.join(AccountStatus).filter(
        AccountStatus.name.like('只读')).join(AccountType).filter(
        AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报战队')).all()

    accounts_locked = Account.query.join(AccountStatus).filter(
        AccountStatus.name.like('锁定')).join(AccountType).filter(
        AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报战队')).all()
    #
    status_normal = AccountStatus.query.filter(
        AccountStatus.name.notlike('Normal')).all()
    status_pending = AccountStatus.query.filter(
        AccountStatus.name.notlike('挂起')).all()
    status_read = AccountStatus.query.filter(
        AccountStatus.name.notlike('只读')).all()
    status_locked = AccountStatus.query.filter(
        AccountStatus.name.notlike('锁定')).all()

    if current_user.account_type.name == "Number据库管理员" or current_user.account_type.name == "积分申报管理":
        #[(1, 'C++'), (2, 'Python'), (3, 'Plain Text')]
        form.normal.choices = [(normal.id, normal.name + ' <' + normal.email + '>')
                               for normal in accounts_normal]
        form.pending.choices = [(pending.id, pending.name + ' <' + pending.email + '>')
                                for pending in accounts_pending]
        form.read.choices = [(read.id, read.name + ' <' + read.email + '>')
                             for read in accounts_read]
        form.locked.choices = [(locked.id, locked.name + ' <' + locked.email + '>')
                               for locked in accounts_locked]

        form.status_normal.choices = [(status.id, status.name)
                                      for status in status_normal]
        form.status_pending.choices = [(status.id, status.name)
                                       for status in status_pending]
        form.status_read.choices = [(status.id, status.name)
                                    for status in status_read]
        form.status_locked.choices = [(status.id, status.name)
                                      for status in status_locked]
    else:
        return redirect(url_for("dashboard_bp.dashboard"))

    # session["select_06"] = "😡😡😡😡😡😡"

    if request.method == 'POST':
        account_normal_id = form.data['normal']
        account_pending_id = form.data['pending']
        account_read_id = form.data['read']
        account_locked_id = form.data['locked']

        status_normal_id = form.data['status_normal']
        status_pending_id = form.data['status_pending']
        status_read_id = form.data['status_read']
        status_locked_id = form.data['status_locked']

        if account_normal_id != None:
            account = Account.query.get(account_normal_id)
            account.account_status_id = status_normal_id
            #
            # personal.account_type = AccountType.query.filter(
            #     AccountType.name.like('积分申报战队')).first()
            db.session.commit()
        elif account_pending_id != None:
            account = Account.query.get(account_pending_id)
            account.account_status_id = status_pending_id
            db.session.commit()
        elif account_read_id != None:
            account = Account.query.get(account_read_id)
            account.account_status_id = status_read_id
            db.session.commit()
        else:
            account = Account.query.get(account_locked_id)
            account.account_status_id = status_locked_id
            db.session.commit()

        return redirect(url_for("dashboard_bp.status"))
    return render_template(
        "status.jinja2",
        title="账号状态管理 | 后台管理",
        sub_title="账号状态编辑",

        menu=menu,
        form=form,
        _vars=_vars,

        # template="dashboard-template"

        _height_display='vh'
    )


def account_type_check(type):
    global _g_account_type
    if _g_account_type == type:
        return True
    else:
        return False


_g_AuditSelected = None


@dashboard_bp.route('/dashboard/audit', methods=['GET', 'POST'])
@login_required
# @account_type_check(E_ACCOUNT_TYPE.ADMIN)
def audit():
    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    def seconds_to_time(seconds):
        hour, minute, second, left = 0, 0, 0, 0
        if seconds >= 3600:
            hour = seconds // 3600
            left = seconds % 3600
        else:
            left = seconds
        if left >= 60:
            minute = left // 60
            left = left % 60
        if left != 0:
            second = left
        return ((str(hour) + u'小时') if hour != 0 else '') + ((str(minute) + u'分') if minute != 0 else '') + ((str(second) + u'秒') if second != 0 else '')

    [menu, _vars] = dashboard_init()

    global _g_AuditSelected

    submits = VideoSubmit.query.join(VideoSubmitStatus).filter(
        VideoSubmitStatus.name.like('待审核')).all()

    form = AuditForm()
    form.auditing.choices = [('0', '-- 请选择待审核作品 --')] \
        + [(submit.id, submit.title + "-" + (submit.account.team_name if submit.account.team_name != None else u'个人提交'))
           for submit in submits]

    if _g_AuditSelected != None:
        submit = VideoSubmit.query.get(_g_AuditSelected)
        form.auditing.data = _g_AuditSelected
        form.title.data = submit.title
        form.global_code.data = submit.global_code
        form.team_code.data = submit.team_code
        form.length.data = seconds_to_time(submit.length)

        form.link.data = submit.link
        form.disk_link.data = submit.disk_link

        from flask_wengui_statistics import account_points

        form.plan.data, form.plan_point.data = account_points(submit, 'Design<')
        form.edit.data, form.edit_point.data = account_points(submit, '编辑<')
        form.audit.data, form.audit_point.data = account_points(submit, '审核<')
        form.dubb.data, form.dubb_point.data = account_points(submit, '配音<')
        form.trans.data, form.trans_point.data = account_points(submit, '翻译<')
        form.check.data, form.check_point.data = account_points(submit, '校对<')

        form.comment.data = submit.comment

        _g_AuditSelected = None

    if request.method == 'POST':
        if form.apply.data == True:
            if form.auditing.data == 0:
                _g_AuditSelected = None
            else:
                _g_AuditSelected = form.auditing.data
        elif form.approve.data == True:
            if form.auditing.data != 0:
                status = VideoSubmitStatus.query.filter(
                    VideoSubmitStatus.name.like('%通过%')).first()
                db.session.query(VideoSubmit).filter_by(id=form.auditing.data).update(
                    {"submit_status_id": status.id}, synchronize_session=False)

                db.session.commit()
        else:
            pass

        return redirect(url_for("dashboard_bp.audit"))
    return render_template(
        "audit.jinja2",
        title="账号Type修改 | 后台管理",
        sub_title="作品提交审核",

        menu=menu,
        _vars=_vars,
        #
        form=form,
        # template="dashboard-template"

        adjust4last=True,
    )


@dashboard_bp.route('/dashboard/summary', methods=['GET', 'POST'])
@login_required
def summary():
    [menu, _vars] = dashboard_init()

    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    teams = Account.query.join(AccountType).filter(
        AccountType.name.like('%战队%')).all()

    record_num = 0
    for team in teams:
        submits = team.submits
        if submits != None:
            record_num += len(submits)
    record_num = record_num if teams != None else 0

    return render_template(
        "summary.jinja2",
        title="作品统计 | 后台管理",
        sub_title="作品统计",

        menu=menu,
        _vars=_vars,

        teams=teams,
        # template="dashboard-template"
        _height_display=('vh' if record_num < 4 else 'auto')
    )


@dashboard_bp.route('/dashboard/account', methods=['GET', 'POST'])
@login_required
def account():
    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    personal_account = AccountType.query.filter(
        AccountType.name.like('积分申报成员')).first()
    team_account = AccountType.query.filter(
        AccountType.name.like('积分申报战队')).first()
    admin_account = AccountType.query.filter(
        AccountType.name.like('积分申报管理')).first()

    personals = Account.query.filter_by(account_type=personal_account).all()
    teams = Account.query.filter_by(account_type=team_account).all()
    admins = Account.query.filter_by(account_type=admin_account).all()

    # types = AccountType.query.filter(AccountType.name.like(
    #     '积分申报战队') | AccountType.name.like('积分申报成员')).all()
    form = TypeForm()

    if current_user.account_type.name == "Number据库管理员":
        personal_type = AccountType.query.filter(
            AccountType.name.like('积分申报战队') | AccountType.name.like('积分申报管理')).all()
        team_type = AccountType.query.filter(
            AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报管理')).all()
        admin_type = AccountType.query.filter(
            AccountType.name.like('积分申报成员') | AccountType.name.like('积分申报战队')).all()

        #[(1, 'C++'), (2, 'Python'), (3, 'Plain Text')]
        form.personal.choices = [(personal.id, personal.name)
                                 for personal in personals]
        form.team.choices = [(team.id, team.name)
                             for team in teams]
        form.admin.choices = [(admin.id, admin.name)
                              for admin in admins]

        form.personal_type.choices = [(type.id, type.name)
                                      for type in personal_type]
        form.team_type.choices = [(type.id, type.name)
                                  for type in team_type]
        form.admin_type.choices = [(type.id, type.name)
                                   for type in admin_type]
    elif current_user.account_type.name == "积分申报管理":
        personal_type = AccountType.query.filter(
            AccountType.name.like('积分申报战队')).all()
        team_type = AccountType.query.filter(
            AccountType.name.like('积分申报成员')).all()
        #[(1, 'C++'), (2, 'Python'), (3, 'Plain Text')]
        form.personal.choices = [(personal.id, personal.name)
                                 for personal in personals]
        form.team.choices = [(team.id, team.name)
                             for team in teams]

        form.personal_type.choices = [(type.id, type.name)
                                      for type in personal_type]
        form.team_type.choices = [(type.id, type.name)
                                  for type in team_type]
    else:
        return redirect(url_for("dashboard_bp.dashboard"))

    # session["select_06"] = "😡😡😡😡😡😡"

    if request.method == 'POST':
        # print(g.account_dft)
        # form.user.default = 4
        # form.process()
        # g.account_user_dft = form.user.data
        # g.account_user_type_dft = form.user_type.data
        personal_id = form.data['personal']
        team_id = form.data['team']
        admin_id = form.data['admin']

        personal_type_id = form.data['personal_type']
        team_type_id = form.data['team_type']
        admin_type_id = form.data['admin_type']

        if personal_id != None:
            personal = Account.query.get(personal_id)
            personal.account_type_id = personal_type_id
            #
            # personal.account_type = AccountType.query.filter(
            #     AccountType.name.like('积分申报战队')).first()
            db.session.commit()
        elif team_id != None:
            team = Account.query.get(team_id)
            team.account_type_id = team_type_id
            #
            # team.account_type = AccountType.query.filter(
            #     AccountType.name.like('积分申报成员')).first()
            db.session.commit()
        else:
            admin = Account.query.get(admin_id)
            admin.account_type_id = admin_type_id
            #
            # team.account_type = AccountType.query.filter(
            #     AccountType.name.like('积分申报成员')).first()
            db.session.commit()

        return redirect(url_for("dashboard_bp.account"))
    return render_template(
        "account.jinja2",
        title="账号Type修改 | 后台管理",
        sub_title="账号Type变更",

        menu=menu,
        _vars=_vars,
        #
        form=form,
        # template="dashboard-template"

        _height_display='vh'
    )


@dashboard_bp.route('/dashboard/submit_v1v2', methods=['GET', 'POST'])
@login_required
def submit_v1v2():
    def vh_auto_check(is_initial, is_submit):
        # print('🤐',is_initial)
        # print('🤐', is_submit)
        if is_initial:
            return 'vh'
        elif is_submit:
            return 'auto'
        else:
            return 'vh'

    if (not account_type_check(E_ACCOUNT_TYPE.PERSONAL)) and (not account_type_check(E_ACCOUNT_TYPE.TEAM)):
        return redirect(url_for("dashboard_bp.dashboard"))

    if "g_submit_list" not in globals():
        dashboard()

    [menu, _vars] = dashboard_init()

    if 'v1' in menu[0]['text']:
        sub_title = "Point Reportv1"
        version = 'v1'
    elif 'v2' in menu[0]['text']:
        sub_title = "Point Reportv2"
        version = 'v2'

    form = VideoSubmitForm()
    current_options = submit_frame["options"]

    is_submit = False
    steps = len(_submit_v1v2)
    is_initial = True if steps == 0 else False
    if is_initial == False:
        for step in range(len(_submit_v1v2)):
            # [ [{},{}..{}], [{},{}..{}]...[{},{}..{}] ]
            # vv = [[{'aa':1,'bb':2},{'cc':3,'dd':4},{'ee':5,'ff':6}],[{'aaa':1,'bbb':2},{'ccc':3,'ddd':4},{'eee':5,'fff':6}],[{'aaaa':1,'bbbb':2},{'cccc':3,'dddd':4},{'eeee':5000,'ffff':6}]]
            # vv[0][2]['ff']是6
            # vv[2][2]['eeee']是5000

            idx = _submit_v1v2[step]['value']
            current_options = current_options[idx-1]["options"]

    form.option.choices = [(option['value'], option['name'])
                           for option in current_options]

    if version == 'v1':
        account = current_user
        # submits_num = len(current_user.submits)

        # form.edit.label = Label(
        #     field_id="edit", text="New Field Description")

        form.edit.choices = [(account.id, account.name
                              + ' <' + account.email + '>')]
        form.name.data = current_options[0]['name']

        if current_options[0]['submit'] == True:
            is_submit = True
            form.next.label.text = "提交"

            form.plan.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]
            form.edit.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]
            form.audit.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]
            form.dubb.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]
            form.trans.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]
            form.check.choices = [('0', '-- Choose --')] + [
                (account.id, account.name + ' <' + account.email + '>')]

    else:
        members = current_user.members

        if current_options[0]['submit'] == True:
            is_submit = True
            form.next.label.text = "提交"

            form.plan.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.edit.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.audit.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]
            form.dubb.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.trans.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]
            form.check.choices = [(0, '-- Choose Member --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]
            #
            # submits_num = len(current_user.submits)
            # team_initials = pinyin(
            #     current_user.team_name, style=Style.FIRST_LETTER)
            # form.code.data = (''.join(i[0].upper() for i in team_initials))[
            #     0:3:1]+'-'+(str(submits_num).zfill(4))

        form.name.data = current_options[0]['name']

    if request.method == 'POST':
        last = form.data['last']

        if last == True:
            _submit_v1v2.pop()
        else:
            if is_submit == False:
                # if current_user.team_id != None:
                #     flash(category="error", message="Team Member账号不能独立提交!")
                #     return redirect(url_for("dashboard_bp.submit_v1v2"))

                if steps == 0:
                    category = Category.query.get(form.data['option'])
                    _submit_v1v2.append({"name": category.name,
                                         "value": form.data['option']})
                elif steps == 1:
                    video = Video.query.get(form.data['option'])
                    _submit_v1v2.append({"name": video.name,
                                         "point": video.point,
                                         "value": form.data['option']})
            else:
                plan_id = form.plan.data
                edit_id = form.edit.data
                audit_id = form.audit.data
                dubb_id = form.dubb.data
                trans_id = form.trans.data
                check_id = form.check.data

                if (plan_id + edit_id + audit_id + dubb_id + trans_id + check_id) == 0:
                    flash(category='error', message="请选择负责本任务的各模块战友！")
                    return redirect(url_for("dashboard_bp.submit_v1v2"))

                category_id = _submit_v1v2[0]['value']  # Video
                sub_category_id = _submit_v1v2[1]['value']  # Simplified Video

                product_title = form.title.data
                # team_code = form.code.data

                length = form.length.data.hour*60*60 + \
                    form.length.data.minute*60+form.length.data.second

                link = form.link.data
                disk_link = form.disk_link.data

                comment = form.comment.data
                submit_status = VideoSubmitStatus.query.filter(
                    VideoSubmitStatus.name.like('%待审核%')).first()

                submits_all = VideoSubmit.query.all()
                submits_team = VideoSubmit.query.filter_by(
                    team_id=current_user.id).all()

                if current_user.team_name != None:
                    team_initials = pinyin(
                        current_user.team_name, style=Style.FIRST_LETTER)

                new_submit = VideoSubmit(
                    team_id=current_user.id,
                    category_id=category_id,
                    # sub_category_id=sub_category_id,
                    title=product_title,
                    global_code='NFSC-' + str(len(submits_all)).zfill(6),
                    team_code=None if version == 'v1' else \
                    ((''.join(i[0].upper() for i in team_initials))
                     [0:3:1])+'-'+(str(len(submits_team)).zfill(4)),

                    link=link,
                    disk_link=disk_link,
                    length=length,

                    comment=comment,
                    submit_status=submit_status)

                db.session.add(new_submit)
                db.session.commit()

                submit_id = new_submit.id

                video = Video.query.get(sub_category_id)
                video_type = video.name

                base_point = video.point

                plan_weight = video.operations[0].weight
                edit_weight = video.operations[1].weight
                audit_weight = video.operations[2].weight
                dubb_weight = video.operations[3].weight
                trans_weight = video.operations[4].weight
                check_weight = video.operations[5].weight

                # *******************************
                if plan_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%Design<{}>%'.format(video_type))).first()
                    point = (base_point * plan_weight) // 100

                    new_plan = AccountOperation(
                        submit_id=submit_id,
                        account_id=plan_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_plan)

                # *******************************
                if edit_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%编辑<{}>%'.format(video_type))).first()
                    point = (base_point * edit_weight) // 100

                    new_edit = AccountOperation(
                        submit_id=submit_id,
                        account_id=edit_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_edit)

                # *******************************
                if audit_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%审核<{}>%'.format(video_type))).first()
                    point = (base_point * audit_weight) // 100

                    new_audit = AccountOperation(
                        submit_id=submit_id,
                        account_id=audit_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_audit)

                # *******************************
                if dubb_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%配音<{}>%'.format(video_type))).first()
                    point = (base_point * dubb_weight) // 100

                    new_dubb = AccountOperation(
                        submit_id=submit_id,
                        account_id=dubb_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_dubb)

                # *******************************
                if trans_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%翻译<{}>%'.format(video_type))).first()
                    point = (base_point * trans_weight) // 100

                    new_trans = AccountOperation(
                        submit_id=submit_id,
                        account_id=trans_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_trans)

                # *******************************
                if check_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%校对<{}>%'.format(video_type))).first()
                    point = (base_point * check_weight) // 100

                    new_check = AccountOperation(
                        submit_id=submit_id,
                        account_id=check_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_check)

                db.session.commit()
                _submit_v1v2.clear()

                flash(category='success', message="Point Submitted Successfully")
                if version == 'v1':
                    return redirect(url_for("dashboard_bp.point"))
                elif version == 'v2':
                    return redirect(url_for("dashboard_bp.member"))
                # return redirect(url_for("dashboard_bp.dashboard"))

        return redirect(url_for("dashboard_bp.submit_v1v2"))
    return render_template(
        "submit_v1v2.jinja2",
        title="Task Report",
        #
        menu=menu,
        version=version,
        _vars=_vars,
        #
        sub_title=sub_title,
        current_user=current_user,
        # template="dashboard-template"

        form=form,
        is_initial=is_initial,
        is_submit=is_submit,

        _height_display=vh_auto_check(is_initial, is_submit)
    )


@dashboard_bp.route('/dashboard/submit_v3', methods=['GET', 'POST'])
@login_required
def submit_v3():
    def vh_auto_check(is_initial, is_submit):
        # print('🤐',is_initial)
        # print('🤐', is_submit)
        if is_initial:
            return 'vh'
        elif is_submit:
            return 'auto'
        else:
            return 'vh'

    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    if "g_submit_list" not in globals():
        dashboard()

    [menu, _vars] = dashboard_init()

    form = VideoSubmitForm()

    steps = len(_submit_v3)
    is_initial = True if steps == 0 else False

    if is_initial:
        is_submit = False
        team = AccountType.query.filter(
            AccountType.name.like('积分申报战队')).first()

        teams = Account.query.filter_by(account_type=team).all()
        form.teams.choices = [(0, '-- 请选择战队 --')] + [(team.id, team.name)
                                                     for team in teams]

    else:
        teams = None
        current_options = submit_frame["options"]

        if steps > 1:
            for step in range(steps-1):
                idx = _submit_v3[step + 1]['value']
                current_options = current_options[idx-1]["options"]

        if current_options[0]['submit'] != True:
            is_submit = False
            form.option.choices = [(option['value'], option['name'])
                                   for option in current_options]
            form.name.data = current_options[0]['name']
        else:
            is_submit = True

            members = Account.query.get(
                _submit_v3[0]['value']).members
            #[(1, 'C++'), (2, 'Python'), (3, 'Plain Text')]
            # submits_num = len(current_user.submits)

            # team_initials = pinyin(team_name, style=Style.FIRST_LETTER)
            # form.team_code.data = (''.join(i[0].upper() for i in team_initials))[
            #     0:3:1]+'-'+(str(submits_num).zfill(4))

            form.plan.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.edit.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.audit.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]
            form.dubb.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                        for member in members]
            form.trans.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]
            form.check.choices = [(0, '-- 请选择成员 --')] + [(member.id, '成员: ' + member.name + ' <' + member.email + '>')
                                                         for member in members]

            form.next.label.text = "提交"

    if request.method == 'POST':
        last = form.data['last']
        # next = form.data['next']
        # final = form.data['submit']

        if last == True:
            _submit_v3.pop()
        else:
            if is_submit == False:
                if steps == 0:
                    if form.teams.data == 0:
                        flash(category='error', message="请选择战队！")
                        return redirect(url_for("dashboard_bp.submit_v3"))
                    _submit_v3.append({"name": '战队',
                                       "value": form.teams.data})
                elif steps == 1:
                    category = Category.query.get(form.data['option'])
                    _submit_v3.append({"name": category.name,
                                       "value": form.data['option']})
                elif steps == 2:
                    video = Video.query.get(form.data['option'])
                    _submit_v3.append({"name": video.name,
                                       "point": video.point,
                                       "value": form.data['option']})
            else:
                plan_id = form.plan.data
                edit_id = form.edit.data
                audit_id = form.audit.data
                dubb_id = form.dubb.data
                trans_id = form.trans.data
                check_id = form.check.data

                if (plan_id + edit_id + audit_id + dubb_id + trans_id + check_id) == 0:
                    flash(category='error', message="请选择负责本任务的各模块战友！")
                    return redirect(url_for("dashboard_bp.submit_v3"))

                team_id = _submit_v3[0]['value']  # 战队n

                category_id = _submit_v3[1]['value']  # Video
                sub_category_id = _submit_v3[2]['value']  # Simplified Video

                product_title = form.title.data
                # team_code = form.code.data

                length = form.length.data.hour*60*60 + \
                    form.length.data.minute*60+form.length.data.second

                link = form.link.data
                disk_link = form.disk_link.data

                comment = form.comment.data
                submit_status = VideoSubmitStatus.query.filter(
                    VideoSubmitStatus.name.like('%待审核%')).first()

                submits_all = VideoSubmit.query.all()
                submits_team = VideoSubmit.query.filter_by(
                    team_id=team_id).all()

                team = Account.query.get(team_id)
                if team.team_name != None:
                    team_initials = pinyin(
                        team.team_name, style=Style.FIRST_LETTER)

                new_submit = VideoSubmit(
                    team_id=team_id,
                    category_id=category_id,
                    # sub_category_id=sub_category_id,
                    title=product_title,
                    global_code='NFSC-' + str(len(submits_all)).zfill(6),

                    team_code=(''.join(i[0].upper() for i in team_initials))[
                        0:3:1]+'-'+str(len(submits_team)).zfill(4),

                    link=link,
                    disk_link=disk_link,
                    length=length,

                    comment=comment,
                    submit_status=submit_status)

                db.session.add(new_submit)
                db.session.commit()

                submit_id = new_submit.id

                video = Video.query.get(sub_category_id)
                video_type_name = video.name

                base_point = video.point

                plan_weight = video.operations[0].weight
                edit_weight = video.operations[1].weight
                audit_weight = video.operations[2].weight

                dubb_weight = video.operations[3].weight
                trans_weight = video.operations[4].weight
                check_weight = video.operations[5].weight

                # *******************************
                if plan_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%Design<{}>%'.format(video_type_name))).first()
                    point = (base_point * plan_weight) // 100

                    new_plan = AccountOperation(
                        submit_id=submit_id,
                        account_id=plan_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_plan)
                    new_submit.account_operations.append(new_plan)
                    db.session.commit()

                # *******************************
                if edit_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%文案编辑<{}>%'.format(video_type_name))).first()
                    point = (base_point * edit_weight) // 100

                    new_edit = AccountOperation(
                        submit_id=submit_id,
                        account_id=edit_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_edit)
                    new_submit.account_operations.append(new_edit)
                    db.session.commit()

                # *******************************
                if audit_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%文案审核<{}>%'.format(video_type_name))).first()
                    point = (base_point * audit_weight) // 100

                    new_audit = AccountOperation(
                        submit_id=submit_id,
                        account_id=audit_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_audit)
                    new_submit.account_operations.append(new_audit)
                    db.session.commit()

                # *******************************
                if dubb_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%配音<{}>%'.format(video_type_name))).first()
                    point = (base_point * dubb_weight) // 100

                    new_dubb = AccountOperation(
                        submit_id=submit_id,
                        account_id=dubb_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_dubb)
                    new_submit.account_operations.append(new_dubb)
                    db.session.commit()

                # *******************************
                if trans_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%翻译<{}>%'.format(video_type_name))).first()
                    point = (base_point * trans_weight) // 100

                    new_trans = AccountOperation(
                        submit_id=submit_id,
                        account_id=trans_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_trans)
                    new_submit.account_operations.append(new_trans)
                    db.session.commit()

                # *******************************
                if check_id != 0:
                    operation = Operation.query.filter(
                        Operation.name.like('%翻译校对<{}>%'.format(video_type_name))).first()
                    point = (base_point * check_weight) // 100

                    new_check = AccountOperation(
                        submit_id=submit_id,
                        account_id=check_id,
                        operation=operation,
                        point=point
                    )
                    db.session.add(new_check)
                    new_submit.account_operations.append(new_check)
                    db.session.commit()

                db.session.commit()
                _submit_v3.clear()
                flash(category='success', message="积分申报成功，感谢您为新中国联邦建设的努力！")

                return redirect(url_for("dashboard_bp.dashboard"))
        return redirect(url_for("dashboard_bp.submit_v3"))
    return render_template(
        "submit_v3.jinja2",
        title="任务申报 | 后台管理",
        sub_title="任务申报v3",

        menu=menu,
        teams=teams,
        _vars=_vars,
        # template="dashboard-template"
        form=form,
        is_initial=is_initial,
        is_submit=is_submit,

        _height_display=vh_auto_check(is_initial, is_submit)
    )


@dashboard_bp.route('/dashboard/member', methods=['GET', 'POST'])
@login_required
def member():
    def get_point(member_new):
        return member_new.get('point')

    if not account_type_check(E_ACCOUNT_TYPE.TEAM):
        return redirect(url_for("dashboard_bp.dashboard"))

    """
    """
    # # Bypass if user is logged in
    # if current_user.is_authenticated:
    #     return redirect(url_for("main_bp.dashboard"))
    # [menu_left, menu_right, theme, back] = dashboard_init()
    [menu, _vars] = dashboard_init()

    # users = Account.query.all()

    # members = current_user.members
    # members_points = []
    # for member in members:
    #     points = 0
    #     member_new = {}
    #     member_new['name'] = member.name
    #     member_new['created_on'] = member.created_on
    #     member_new['email'] = member.email

    #     submits = member.submits
    #     # for submit in submits:
    #     #     points += submit.point
    #     # member_new['point'] = points
    #     members_points.append(member_new)

    # members_points.sort(key=get_point, reverse=True)

    members = current_user.members
    submits = current_user.submits

    record_num = 0
    record_num += len(members)
    if submits != None:
        record_num += len(submits)

    return render_template(
        "member.jinja2",
        title="我的成员 | 后台管理",
        sub_title="Team Member",
        #
        menu=menu,
        _vars=_vars,
        #
        # members=members,
        # members_points=members_points,
        members=members,
        submits=submits,
        # template="dashboard-template"
        # adjust4last=True,

        _height_display=('vh' if record_num < 4 else 'auto')
    )


@dashboard_bp.route('/dashboard/point', methods=['GET', 'POST'])
@login_required
def point():
    if (not account_type_check(E_ACCOUNT_TYPE.MEMBER)) and (not account_type_check(E_ACCOUNT_TYPE.PERSONAL)):
        return redirect(url_for("dashboard_bp.dashboard"))

    """
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # # Bypass if user is logged in
    # if current_user.is_authenticated:
    #     return redirect(url_for("main_bp.dashboard"))
    # [menu_left, menu_right, theme, back] = dashboard_init()
    [menu, _vars] = dashboard_init()

    record_num = 0

    is_member = None
    # users = Account.query.all()
    if u'成员' in current_user.account_type.name:
        submits = VideoSubmit.query.join(AccountOperation).filter(
            AccountOperation.account_id == current_user.id)
        record_num += submits.count()
        is_member = True
    elif u'个人' in current_user.account_type.name:
        submits = current_user.submits
        record_num += len(submits)
        is_member = False

    # if submits != None:
    #     record_num += len(submits)

    return render_template(
        "point.jinja2",
        title="我的积分 | 后台管理",
        sub_title="我的积分",
        #
        menu=menu,
        _vars=_vars,

        submits=submits,

        is_member=is_member,

        _height_display=('vh' if record_num < 10 else 'auto')
    )


@dashboard_bp.route('/dashboard/weight', methods=['GET', 'POST'])
@login_required
def weight():
    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    # video_types = ["Tiny Video", "Simplified Video", "State StructuredVideo", "Create StructedVideo", "Documentary", "EmergencyVideo", "Interview Video"]
    data_mic = Operation.query.join(Video).filter(Video.name.like('Tiny Video')).all()
    data_sim = Operation.query.join(Video).filter(
        Video.name.like('Simplified Video')).all()
    data_ref = Operation.query.join(Video).filter(
        Video.name.like('State StructuredVideo')).all()
    data_crt = Operation.query.join(Video).filter(
        Video.name.like('Create StructedVideo')).all()
    data_rcd = Operation.query.join(Video).filter(Video.name.like('Documentary')).all()
    data_ugt = Operation.query.join(Video).filter(
        Video.name.like('EmergencyVideo')).all()
    data_cht = Operation.query.join(Video).filter(
        Video.name.like('Interview Video')).all()

    # form_mic = WeightForm(E_VIDEO_TYPE .MIC_VIDEO)
    form = WeightForm()
    form.mic_plan.data = data_mic[0].weight
    form.mic_edit.data = data_mic[1].weight
    form.mic_audit.data = data_mic[2].weight
    form.mic_dubb.data = data_mic[3].weight
    form.mic_trans.data = data_mic[4].weight
    form.mic_check.data = data_mic[5].weight

    form.sim_plan.data = data_sim[0].weight
    form.sim_edit.data = data_sim[1].weight
    form.sim_audit.data = data_sim[2].weight
    form.sim_dubb.data = data_sim[3].weight
    form.sim_trans.data = data_sim[4].weight
    form.sim_check.data = data_sim[5].weight

    form.ref_plan.data = data_ref[0].weight
    form.ref_edit.data = data_ref[1].weight
    form.ref_audit.data = data_ref[2].weight
    form.ref_dubb.data = data_ref[3].weight
    form.ref_trans.data = data_ref[4].weight
    form.ref_check.data = data_ref[5].weight

    form.crt_plan.data = data_crt[0].weight
    form.crt_edit.data = data_crt[1].weight
    form.crt_audit.data = data_crt[2].weight
    form.crt_dubb.data = data_crt[3].weight
    form.crt_trans.data = data_crt[4].weight
    form.crt_check.data = data_crt[5].weight

    form.rcd_plan.data = data_rcd[0].weight
    form.rcd_edit.data = data_rcd[1].weight
    form.rcd_audit.data = data_rcd[2].weight
    form.rcd_dubb.data = data_rcd[3].weight
    form.rcd_trans.data = data_rcd[4].weight
    form.rcd_check.data = data_rcd[5].weight

    form.ugt_plan.data = data_ugt[0].weight
    form.ugt_edit.data = data_ugt[1].weight
    form.ugt_audit.data = data_ugt[2].weight
    form.ugt_dubb.data = data_ugt[3].weight
    form.ugt_trans.data = data_ugt[4].weight
    form.ugt_check.data = data_ugt[5].weight

    form.cht_plan.data = data_cht[0].weight
    form.cht_edit.data = data_cht[1].weight
    form.cht_audit.data = data_cht[2].weight
    form.cht_dubb.data = data_cht[3].weight
    form.cht_trans.data = data_cht[4].weight
    form.cht_check.data = data_cht[5].weight

    if request.method == 'POST':
        # print(form.theme.data)
        if form.mic_submit.data:
            if form.validate_mic():
                plan = form.mic_plan.raw_data[0]
                edit = form.mic_edit.raw_data[0]
                audit = form.mic_audit.raw_data[0]
                dubb = form.mic_dubb.raw_data[0]
                trans = form.mic_trans.raw_data[0]
                check = form.mic_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%Tiny Video%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.sim_submit.data:
            if form.validate_sim():
                plan = form.sim_plan.raw_data[0]
                edit = form.sim_edit.raw_data[0]
                audit = form.sim_audit.raw_data[0]
                dubb = form.sim_dubb.raw_data[0]
                trans = form.sim_trans.raw_data[0]
                check = form.sim_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%Simplified Video%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.ref_submit.data:
            if form.validate_ref():
                plan = form.ref_plan.raw_data[0]
                edit = form.ref_edit.raw_data[0]
                audit = form.ref_audit.raw_data[0]
                dubb = form.ref_dubb.raw_data[0]
                trans = form.ref_trans.raw_data[0]
                check = form.ref_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%State StructuredVideo%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.crt_submit.data:
            if form.validate_crt():
                plan = form.crt_plan.raw_data[0]
                edit = form.crt_edit.raw_data[0]
                audit = form.crt_audit.raw_data[0]
                dubb = form.crt_dubb.raw_data[0]
                trans = form.crt_trans.raw_data[0]
                check = form.crt_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%Create StructedVideo%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.rcd_submit.data:
            if form.validate_rcd():
                plan = form.rcd_plan.raw_data[0]
                edit = form.rcd_edit.raw_data[0]
                audit = form.rcd_audit.raw_data[0]
                dubb = form.rcd_dubb.raw_data[0]
                trans = form.rcd_trans.raw_data[0]
                check = form.rcd_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%Documentary%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.ugt_submit.data:
            if form.validate_ugt():
                plan = form.ugt_plan.raw_data[0]
                edit = form.ugt_edit.raw_data[0]
                audit = form.ugt_audit.raw_data[0]
                dubb = form.ugt_dubb.raw_data[0]
                trans = form.ugt_trans.raw_data[0]
                check = form.ugt_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%EmergencyVideo%')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")
        elif form.cht_submit.data:
            if form.validate_cht():
                plan = form.cht_plan.raw_data[0]
                edit = form.cht_edit.raw_data[0]
                audit = form.cht_audit.raw_data[0]
                dubb = form.cht_dubb.raw_data[0]
                trans = form.cht_trans.raw_data[0]
                check = form.cht_check.raw_data[0]

                video = Video.query.filter(Video.name.like('%Interview %')).first()

                db.session.query(Operation).filter(Operation.name.like(
                    '%Design%'), Operation.video == video).update({"weight": plan}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%编辑%'), Operation.video == video).update({"weight": edit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%审核%'), Operation.video == video).update({"weight": audit}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%配音%'), Operation.video == video).update({"weight": dubb}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%翻译%'), Operation.video == video).update({"weight": trans}, synchronize_session=False)
                db.session.query(Operation).filter(Operation.name.like(
                    '%校对%'), Operation.video == video).update({"weight": check}, synchronize_session=False)

                db.session.commit()
                flash(category='success', message="更新成功！")

        return redirect(url_for("dashboard_bp.weight"))
    return render_template(
        "weight.jinja2",
        title="设置 | 后台管理",
        sub_title="岗位权重设置",
        #
        menu=menu,
        weight_page=True,
        _vars=_vars,
        #
        form=form,
    )


@dashboard_bp.route('/dashboard/pparameter', methods=['GET', 'POST'])
@login_required
def pparameter():
    if not account_type_check(E_ACCOUNT_TYPE.ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    videos = Video.query.all()

    form = PointForm()
    form.mic_video.data = videos[0].point
    form.sim_video.data = videos[1].point
    form.ref_video.data = videos[2].point
    form.crt_video.data = videos[3].point
    form.rcd_video.data = videos[4].point
    form.ugt_video.data = videos[5].point
    form.cht_video.data = videos[6].point

    if request.method == 'POST':
        if form.submit_mic.data:
            mic_video = form.mic_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%Tiny Video%')).update({"point": mic_video}, synchronize_session=False)
        elif form.submit_sim.data:
            sim_video = form.sim_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%Simplified Video%')).update({"point": sim_video}, synchronize_session=False)
        elif form.submit_ref.data:
            ref_video = form.ref_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%State StructuredVideo%')).update({"point": ref_video}, synchronize_session=False)
        elif form.submit_crt.data:
            crt_video = form.crt_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%Create StructedVideo%')).update({"point": crt_video}, synchronize_session=False)
        elif form.submit_rcd.data:
            rcd_video = form.rcd_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%Documentary%')).update({"point": rcd_video}, synchronize_session=False)
        elif form.submit_ugt.data:
            ugt_video = form.ugt_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%EmergencyVideo%')).update({"point": ugt_video}, synchronize_session=False)
        elif form.submit_cht.data:
            cht_video = form.cht_video.raw_data[0]
            db.session.query(Video).filter(
                Video.name.like('%Interview Video%')).update({"point": cht_video}, synchronize_session=False)

        db.session.commit()

        flash(category='success', message="积分参Number设置成功！")
        return redirect(url_for("dashboard_bp.pparameter"))
    return render_template(
        "pparameter.jinja2",
        title="积分参Number设置 | 后台管理",
        sub_title="积分参Number设置",

        #
        menu=menu,
        _vars=_vars,
        #
        form=form,
        # template="dashboard-template"

        adjust4last=True,
    )


@dashboard_bp.route('/dashboard/settings', methods=['GET', 'POST'])
@login_required
def setting():
    """
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # # Bypass if user is logged in
    # if current_user.is_authenticated:
    #     return redirect(url_for("main_bp.dashboard"))
    # [menu_left, menu_right, theme, back] = dashboard_init()
    [menu, _vars] = dashboard_init()

    account = Account.query.filter(Account.id == current_user.id).first()
    form = SettingForm(theme=account.theme_id)  # theme=2
    # form = SettingForm()  # theme=2
    # form.theme(choices=[(theme.id, theme.name) for theme in Theme.query.all()])

    # _vars["theme"] = "dark" if account.theme.name == "Deep Color" else "white?"

    # form.name.data = account.name
    # form.email.data = account.email
    # form.discord.data = account.discord
    # form.farm.data = account.farm
    # form.twitter.data = account.twitter
    # form.gettr.data = account.gettr

    form.theme.choices = [(theme.id, theme.name)
                          for theme in Theme.query.all()]

    # form.theme.default = user.theme_id
    # form.process()

    if request.method == 'POST':
        if form.discord.data == None:
            discord_string = None
        else:
            discord_string = form.discord.data.strip()

        if form.farm.data == None:
            farm_string = None
        else:
            farm_string = form.farm.data.strip()

        if form.twitter.data == None:
            twitter_string = None
        else:
            twitter_string = form.twitter.data.strip()

        if form.gettr.data == None:
            gettr_string = None
        else:
            gettr_string = form.gettr.data.strip()

        if form.discord.data == None:
            discord_string = None
        else:
            discord_string = form.discord.data.strip()

        # print(form.theme.data)
        data = {"name": form.name.data,
                "email": form.email.data,
                "discord": discord_string,
                "farm": farm_string,
                "twitter": twitter_string,
                "gettr": gettr_string,
                "theme_id": form.theme.data}
        db.session.query(Account).filter(
            Account.id == current_user.id).update(data)
        db.session.commit()

        current_user.theme.id = form.theme.data

        flash(category='success', message="Setting Successfully!")
        return redirect(url_for("dashboard_bp.setting"))
    return render_template(
        "setting.jinja2",
        title="Setting | 后台管理",
        sub_title="Setting",
        #
        menu=menu,
        _vars=_vars,
        #
        user=current_user,
        #
        form=form,
        # template="dashboard-template"

        adjust4last=True,
    )


def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


@dashboard_bp.route('/dashboard/auth_list', methods=['GET', 'POST'])
@login_required
def auth_list():
    from ..auth.model_white import WhiteIP
    from ..auth.model_black import BlackIP

    if not account_type_check(E_ACCOUNT_TYPE.DATA_ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    list_white = WhiteIP.query.all()
    list_black = BlackIP.query.all()

    form = BWListForm()

    if request.method == 'POST':
        submit_white = form.submit_white.data
        # submit_black = form.submit_black
        if submit_white:
            ip = form.white.data
            note = form.white_note.data
            if (is_valid_ip(ip)):
                if bool(WhiteIP.query.filter_by(ip=ip).first()):
                    flash(category='error', message="Ip is in white List!")
                else:
                    _ip = WhiteIP(ip=ip, note=note)

                    db.session.add(_ip)
                    db.session.commit()
            else:
                flash(category='error', message="Ip Invalide!")
        else:
            ip = form.black.data
            note = form.black_note.data
            if (is_valid_ip(ip)):
                if bool(BlackIP.query.filter_by(ip=ip).first()):
                    flash(category='error', message="IP is in Black List!")
                else:
                    _ip = BlackIP(ip=ip, note=note)

                    db.session.add(_ip)
                    db.session.commit()
            else:
                flash(category='error', message="Ip Invalide!")

        return redirect(url_for("dashboard_bp.auth_list"))
    return render_template(
        "black_white.jinja2",
        title="List of IP | 后台管理",
        sub_title="List of IP",

        menu=menu,
        _vars=_vars,
        list_white=list_white,
        list_black=list_black,

        form=form,
        # template="dashboard-template"
    )


@dashboard_bp.route('/dashboard/backup', methods=['GET', 'POST'])
@login_required
def backup():
    if not account_type_check(E_ACCOUNT_TYPE.DATA_ADMIN):
        return redirect(url_for("dashboard_bp.dashboard"))

    [menu, _vars] = dashboard_init()

    form = BackupForm()

    if request.method == 'POST':
        from os import path

        name = form.backup.data
        now = str(datetime.datetime.now())[:19]
        # now = now.replace(":", "_")
        pathtwo_up = path.abspath(path.join(__file__, "../../.."))
        src_dir = pathtwo_up + "/database/db_statistics.db"
        if not name:
            dst_dir = pathtwo_up+"/backup/backup-"+name+str(now)+".db"
        else:
            dst_dir = pathtwo_up+"/backup/"+name+'-'+str(now)+".db"
        shutil.copy(src_dir, dst_dir)

        if not name:
            flash(category='success', message="备份完成!")
        else:
            flash(category='success', message=name+'-'+str(now)+".db 备份完成!")

        return redirect(url_for("dashboard_bp.backup"))
    return render_template(
        "backup.jinja2",
        title="Database Backup | 后台管理",
        sub_title="Database Backup",
        #
        menu=menu,
        _vars=_vars,
        #
        form=form,
        # template="dashboard-template"

        _height_display='vh'
    )
