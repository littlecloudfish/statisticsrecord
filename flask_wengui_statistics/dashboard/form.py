"""Sign-up & log-in forms."""

from flask import flash
from email import message
from flask_wtf import FlaskForm
from wtforms import PasswordField, RadioField, IntegerRangeField, IntegerField, SelectField, StringField, HiddenField, TextAreaField, EmailField, TimeField, URLField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from datetime import time, datetime
from ..dashboard.model_video import E_VIDEO_TYPE


class VideoSubmitForm(FlaskForm):
    '''
    '''
    name = HiddenField('name')
    teams = SelectField('战队', coerce=int, default=0, render_kw={
        'class': 'form-control mt-1 form-select bg-light border border-3 border-danger rounded-pill'})
    # point = HiddenField('point')
    #
    option = RadioField(u"", coerce=int, validate_choice=False, render_kw={
        'class': 'form-check-input'}, default=1)
    # else:
    title = StringField('视频名称',
                        #   validators=[DataRequired(
                        #       message='视频名称必填.')],
                        render_kw={"placeholder": "视频名称", 'class': 'form-control mt-1 border border-3 border-info text-primary bg-light', 'minlength': 1, 'maxlength': 150})
    # team_code = StringField(
    #     "作品编号",
    #     # validators=[DataRequired("作品编号必填.")],
    #     render_kw={'class': 'form-control rounded-pill', 'readonly': 'true'}
    # )

    length = TimeField('视频时长',
                       format='%H:%M:%S',
                       #    validators=[DataRequired()],
                       render_kw={'placeholder': '起始时间', 'step': '1',
                                  'min': '00:00',
                                  'max': '23:59',
                                  'class': 'form-control mt-1 border border-3 border-info text-info bg-light rounded-pill'
                                  },  # default=time(hour=1, minute=2, second=3)
                       default=time()
                       )

    coop = StringField(
        "协调",
        # validators=[DataRequired("协调必填.")]
    )
    guide = StringField(
        "视频导语",
        # validators=[DataRequired("视频导语必填.")]
    )
    link = URLField('链接',
                    # validators=[DataRequired()],
                    render_kw={'placeholder': '作品链接', 'class': 'form-control mt-1 bg-light rounded-pill'})
    disk_link = URLField('网盘链接',
                         # validators=[DataRequired()],
                         render_kw={'placeholder': '网盘链接', 'class': 'form-control mt-1 bg-light rounded-pill'})
    # 文案编辑
    # 文案审核
    # 配音
    # 翻译
    # 翻译校队
    plan = SelectField('策划(没有则留空)', default=0, coerce=int, render_kw={
                       'class': 'form-control mt-1 form-select border border-3 border-danger text-danger bg-light rounded-pill'})
    edit = SelectField('编辑(没有则留空)', default=0, coerce=int, render_kw={
                       'class': 'form-control mt-1 form-select border border-3 border-info text-info bg-light rounded-pill'})
    audit = SelectField('文案审核(没有则留空)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-warning bg-light text-warning rounded-pill'})
    dubb = SelectField('配音(没有则留空)', default=0, coerce=int,  render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-primary text-primary bg-light rounded-pill'})
    trans = SelectField('翻译(没有则留空)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger bg-light rounded-pill'})
    check = SelectField('翻译校队(没有则留空)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-success bg-light text-success rounded-pill'})
    #
    comment = TextAreaField('备注',
                            #   validators=[DataRequired(
                            #       message='视频名称必填.')],
                            render_kw={"placeholder": "提交说明, 备注等", 'class': 'form-control mt-1 border border-3 border-info text-primary bg-light', 'minlength': 0, 'maxlength': 350})
    #

    last = SubmitField(
        u"上一步", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    next = SubmitField(
        u"下一步", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class TypeForm(FlaskForm):
    """?? Form."""

    personal = SelectField(u'成员账号', render_kw={
        'class': 'form-control mt-1 form-select'})
    team = SelectField(u'战队账号', render_kw={
                       'class': 'form-control mt-1 form-select'})
    admin = SelectField(u'管理员账号', render_kw={
        'class': 'form-control mt-1 form-select'})
    personal_type = SelectField(
        u'账号类型', render_kw={'class': 'form-control mt-1 form-select'})
    team_type = SelectField(
        u'账号类型', render_kw={'class': 'form-control mt-1 form-select'})
    admin_type = SelectField(
        u'账号类型', render_kw={'class': 'form-control mt-1 form-select'})
    # account_type = SelectField(
    #     u'账号类型', render_kw={'class': 'form-control form-select'})
    submit = SubmitField(u"修改为", render_kw={'class': 'btn btn-primary'})


class StatusForm(FlaskForm):
    """?? Form."""

    # ["正常", "挂起", "只读", "锁定"]
    normal = SelectField(u'账号(正常)', render_kw={
        'class': 'form-control mt-1 form-select'})
    pending = SelectField(u'账号(挂起)', render_kw={
        'class': 'form-control mt-1 form-select'})
    read = SelectField(u'账号(只读)', render_kw={
        'class': 'form-control mt-1 form-select'})
    locked = SelectField(
        u'账号(锁定)', render_kw={'class': 'form-control mt-1 form-select'})
    #
    status_normal = SelectField(
        u'状态选择', render_kw={'class': 'form-control mt-1 form-select'})
    status_pending = SelectField(
        u'状态选择', render_kw={'class': 'form-control mt-1 form-select'})
    status_read = SelectField(
        u'状态选择', render_kw={'class': 'form-control mt-1 form-select'})
    status_locked = SelectField(
        u'状态选择', render_kw={'class': 'form-control mt-1 form-select'})
    #
    submit = SubmitField(u"修改为", render_kw={'class': 'btn btn-primary'})

# primary， success ， info ， warning ， danger ， secondary ， dark ， light，


class CreateForm(FlaskForm):
    name = StringField(u'账号名称',
                       validators=[DataRequired(message=u'名称需要.')],
                       render_kw={"placeholder": "账号名称", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill', 'minlength': 5, 'maxlength': 150})

    email = EmailField(u'邮箱',
                       validators=[DataRequired(message=u'邮箱地址需要'),
                                   Email(message=u'格式错误')],
                       render_kw={"placeholder": "邮箱地址", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill'})

    password = PasswordField(
        "密码",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ], render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}
    )

    type = SelectField(u'账号类型', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})

    team = SelectField(u'所属战队', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})

    create = SubmitField(u"创建", render_kw={'class': 'btn btn-primary w-100'})

    def validate_on_submit(self):
        if not self.name.data.strip():
            return False
        if self.type.data != 0:
            type = self.type.data
            choice = self.type.choices[type][1]
            if (u'成员' in choice) and self.team.data == 0:
                return False
        return True

class AuditForm(FlaskForm):
    """?? Form."""
    auditing = SelectField(u'待审核提交', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})
    #
    title = StringField('视频名称',
                        #   validators=[DataRequired(
                        #       message='视频名称必填.')],
                        render_kw={"placeholder": "视频名称", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill', 'minlength': 5, 'maxlength': 150, 'readonly': 'true'})
    global_code = StringField(
        "作品编号(全球)",
        # validators=[DataRequired("作品编号必填.")],
        render_kw={
            'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'}
    )

    team_code = StringField(
        "作品编号(战队)",
        # validators=[DataRequired("作品编号必填.")],
        render_kw={
            'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'}
    )

    # length = TimeField('视频时长',
    #                    format='%H:%M:%S',
    #                    #    validators=[DataRequired()],
    #                    render_kw={'placeholder': '起始时间', 'step': '1',
    #                               'min': '00:00',
    #                               'max': '23:59',
    #                               'class': 'form-control border border-1 border-danger text-danger rounded-pill',
    #                               'readonly': 'true'
    #                               },  # default=time(hour=1, minute=2, second=3)
    #                    default=time()
    #                    )
    length = StringField(
        "视频时长", render_kw={'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'}
        # validators=[DataRequired("协调必填.")]
    )

    coop = StringField(
        "协调", render_kw={'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill'}
        # validators=[DataRequired("协调必填.")]
    )
    guide = StringField(
        "视频导语", render_kw={'class': 'form-control mt-1 border border-1 border-danger, text-danger, rounded-pill'}
        # validators=[DataRequired("视频导语必填.")]
    )
    link = URLField('链接',
                    # validators=[DataRequired()],
                    render_kw={'placeholder': '作品链接', 'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    disk_link = URLField('网盘链接',
                         # validators=[DataRequired()],
                         render_kw={'placeholder': '网盘链接', 'class': 'form-control mt-1 border border-1 border-dark  rounded-pill', 'readonly': 'true'})
    # primary ， success ， info ， warning ， danger ， secondary ， dark ， light ，
    plan = StringField('策划', render_kw={
                       'class': 'form-control mt-1 border border-1 border-primary text-primary rounded-pill', 'readonly': 'true'})
    plan_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-primary text-primary rounded-pill', 'readonly': 'true'})

    edit = StringField('编辑', render_kw={
                       'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'})
    edit_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'})

    audit = StringField('文案审核', render_kw={
                        'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'})
    audit_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'})

    dubb = StringField('配音', render_kw={
                       'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill', 'readonly': 'true'})
    dubb_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill', 'readonly': 'true'})

    trans = StringField('翻译', render_kw={
                        'class': 'form-control mt-1 border border-1 border-danger text-danger rounded-pill', 'readonly': 'true'})
    trans_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-danger text-danger rounded-pill', 'readonly': 'true'})

    check = StringField('翻译校队', render_kw={
                        'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    check_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    #
    comment = TextAreaField('备注',
                            #   validators=[DataRequired(
                            #       message='视频名称必填.')],
                            render_kw={"placeholder": "提交说明, 备注等", 'class': 'form-control mt-1 border border-1 border-danger text-danger', 'minlength': 0, 'maxlength': 350, 'readonly': 'true'})
    comment_audit = TextAreaField('审核反馈',
                                  #   validators=[DataRequired(
                                  #       message='视频名称必填.')],
                                  render_kw={"placeholder": "未通过原因等", 'class': 'form-control mt-1 border border-1 border-success text-success', 'minlength': 0, 'maxlength': 350, 'resize': 'none'})
    #
    apply = SubmitField(u"确定", render_kw={'class': 'btn btn-primary'})
    approve = SubmitField(u"通过", render_kw={'class': 'btn btn-primary'})
    deny = SubmitField(u"参照反馈,重新提交", render_kw={'class': 'btn btn-primary'})


class SettingForm(FlaskForm):
    """User Account Form."""
    name = StringField(
        u"账号名", validators=[DataRequired()], render_kw={'class': 'form-control mt-1 border border-danger text-danger bg-light rounded-pill'})

    team_name = StringField(
        u"战队名", render_kw={'class': 'form-control mt-1 border border-danger text-danger rounded-pill', 'readonly': 'true'})

    email = EmailField(
        "邮箱",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired()
        ], render_kw={'class': 'form-control mt-1 border border-info text-info rounded-pill', 'readonly': 'true'}
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ], render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}
    )
    confirm = PasswordField(
        "重复密码",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ], render_kw={'class': 'form-control mt-1 border border-success text-success bg-light rounded-pill'}
    )

    discord = StringField("Discord", render_kw={
                          'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}, validators=None)
    farm = StringField(u"所在农场", render_kw={
                       'class': 'form-control mt-1 border border-success text-success bg-light rounded-pill'}, validators=None)
    twitter = StringField(
        u"推特账号", render_kw={'class': 'form-control mt-1 border border-primary text-primary bg-light  rounded-pill'}, validators=None)
    gettr = StringField(u"盖特账号", render_kw={
                        'class': 'form-control mt-1 border border-dark text-dark bg-light rounded-pill'}, validators=None)
    theme = SelectField(
        u"主题", render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light form-select rounded-pill'}, coerce=int, validators=None)

    submit = SubmitField(
        u"修改", render_kw={'class': 'form-control mt-1 border border-none text-white bg-primary rounded-pill'})


# @unique
# class E_VIDEO_TYPE (IntEnum):
#     MIC_VIDEO = 0
#     SIM_VIDEO = 1
#     REF_VIDEO = 2
#     CRT_VIDEO = 3
#     RCD_VIDEO = 4
#     UGT_VIDEO = 5
#     CHT_VIDEO = 6
# video_types = ["微视频", "简化视频", "引述结构视频", "创作结构视频", "纪录片", "应急视频", "访谈视频"]
class WeightForm(FlaskForm):
    '''
    '''

    def __init__(self, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type == E_VIDEO_TYPE .MIC_VIDEO:
            self.name = "微视频"
            self.id = 'MIC_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .SIM_VIDEO:
            self.name = "简化视频"
            self.id = 'SIM_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .REF_VIDEO:
            self.name = "引述结构视频"
            self.id = 'REF_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .CRT_VIDEO:
            self.name = "创作结构视频"
            self.id = 'CRT_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .RCD_VIDEO:
            self.name = "纪录片"
            self.id = 'RCD_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .UGT_VIDEO:
            self.name = "应急视频"
            self.id = 'UGT_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .CHT_VIDEO:
            self.name = "访谈视频"
            self.id = 'CHT_VIDEO'.lower()
        else:
            # self.name = "FKCCP"
            # self.id = 'NSFC'.lower()
            self.mic_name = "微视频"
            self.sim_name = "简化视频"
            self.ref_name = "引述结构视频"
            self.crt_name = "创作结构视频"
            self.rcd_name = "纪录片"
            self.ugt_name = "应急视频"
            self.cht_name = "访谈视频"
            self.mic_id = 'MIC_VIDEO'.lower()
            self.sim_id = 'SIM_VIDEO'.lower()
            self.ref_id = 'REF_VIDEO'.lower()
            self.crt_id = 'CRT_VIDEO'.lower()
            self.rcd_id = 'RCD_VIDEO'.lower()
            self.ugt_id = 'UGT_VIDEO'.lower()
            self.cht_id = 'CHT_VIDEO'.lower()

    # 文案编辑
    # 文案审核
    # 配音
    # 翻译
    # 翻译校队
    # indicater = StringField("(%):", validators=[DataRequired()], render_kw={
    #     'class': 'form-control border border-2 border-danger text-danger text-center', 'readonly': 'true'})

    # ["微视频", "简化视频", "引述结构视频", "创作结构视频", "纪录片", "应急视频", "访谈视频"]
    mic_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'list': 'tickmarks', 'oninput': "weight_change(this);", 'oncdbllick': "this.disabled=false;"})

    mic_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this);"})

    mic_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    sim_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    ref_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    crt_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    rcd_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    ugt_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    cht_plan = IntegerRangeField('策划权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_edit = IntegerRangeField('编辑权重', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_audit = IntegerRangeField('文案审核权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_dubb = IntegerRangeField('配音权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_trans = IntegerRangeField('翻译权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # check = IntegerRangeField('翻译校队权重:', default='1', render_kw={
    #     'class': 'form-control border border-2 border-secondary text-secondary bg-light rounded-pill', 'min': 0, 'max': 100, 'step': 1, 'oninput': "this.previousElementSibling.previousElementSibling.innerHTML = this.value"})

    mic_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    sim_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    ref_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    crt_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    rcd_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    ugt_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    cht_submit = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    def validate_mic(self):
        weight_total = int(self.mic_plan.raw_data[0]) + int(self.mic_edit.raw_data[0]) + int(self.mic_audit.raw_data[0]) + \
            int(self.mic_dubb.raw_data[0]) + \
            int(self.mic_trans.raw_data[0]) + int(self.mic_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_sim(self):
        weight_total = int(self.sim_plan.raw_data[0]) + int(self.sim_edit.raw_data[0]) + int(self.sim_audit.raw_data[0]) + \
            int(self.sim_dubb.raw_data[0]) + \
            int(self.sim_trans.raw_data[0]) + int(self.sim_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_ref(self):
        weight_total = int(self.ref_plan.raw_data[0]) + int(self.ref_edit.raw_data[0]) + int(self.ref_audit.raw_data[0]) + \
            int(self.ref_dubb.raw_data[0]) + \
            int(self.ref_trans.raw_data[0]) + int(self.ref_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_crt(self):
        weight_total = int(self.crt_plan.raw_data[0]) + int(self.crt_edit.raw_data[0]) + int(self.crt_audit.raw_data[0]) + \
            int(self.crt_dubb.raw_data[0]) + \
            int(self.crt_trans.raw_data[0]) + int(self.crt_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_rcd(self):
        weight_total = int(self.rcd_plan.raw_data[0]) + int(self.rcd_edit.raw_data[0]) + int(self.rcd_audit.raw_data[0]) + \
            int(self.rcd_dubb.raw_data[0]) + \
            int(self.rcd_trans.raw_data[0]) + int(self.rcd_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_ugt(self):
        weight_total = int(self.ugt_plan.raw_data[0]) + int(self.ugt_edit.raw_data[0]) + int(self.ugt_audit.raw_data[0]) + \
            int(self.ugt_dubb.raw_data[0]) + \
            int(self.ugt_trans.raw_data[0]) + int(self.ugt_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    def validate_cht(self):
        weight_total = int(self.cht_plan.raw_data[0]) + int(self.cht_edit.raw_data[0]) + int(self.cht_audit.raw_data[0]) + \
            int(self.cht_dubb.raw_data[0]) + \
            int(self.cht_trans.raw_data[0]) + int(self.cht_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='总权重不能大于100%!')
            return False
        else:
            return True

    # def validate_on_submit(self):
    #     return self.validate_time(self.start, self.finish)


# danger
# info
# warning
# primary
# danger
# success
class PointForm(FlaskForm):
    '''
    '''
    # MIC_VIDEO = 0
    # SIM_VIDEO = 1
    # REF_VIDEO = 2
    # CRT_VIDEO = 3
    # RCD_VIDEO = 4
    # UGT_VIDEO = 5
    # CHT_VIDEO = 6
    mic_video = IntegerField('微视频:', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill'})

    sim_video = IntegerField('简化视频:', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill'})

    ref_video = IntegerField('引述结构视频:', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill'})

    crt_video = IntegerField('创作结构视频:', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill'})

    rcd_video = IntegerField('纪录片:', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill'})

    ugt_video = IntegerField('应急视频:', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill'})

    cht_video = IntegerField('访谈视频:', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill'})

    submit_mic = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_sim = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_ref = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_crt = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_rcd = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_ugt = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_cht = SubmitField(
        u"设置", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class BackupForm(FlaskForm):
    '''
    '''

    backup = StringField('数据库备份:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': '名称..'})

    submit = SubmitField(
        u"备份", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class BWListForm(FlaskForm):
    '''
    '''

    black = StringField('黑名单:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': 'IP'})
    black_note = StringField('备注:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill'})

    white = StringField('白名单:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': 'IP'})
    white_note = StringField('备注:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill'})

    submit_black = SubmitField(
        u"保存", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_white = SubmitField(
        u"保存", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
