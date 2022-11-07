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
    teams = SelectField('Team', coerce=int, default=0, render_kw={
        'class': 'form-control mt-1 form-select bg-light border border-3 border-danger rounded-pill'})
    # point = HiddenField('point')
    #
    option = RadioField(u"", coerce=int, validate_choice=False, render_kw={
        'class': 'form-check-input'}, default=1)
    # else:
    title = StringField('Video Name',
                        #   validators=[DataRequired(
                        #       message='Video Name必填.')],
                        render_kw={"placeholder": "Video Name", 'class': 'form-control mt-1 border border-3 border-info text-primary bg-light', 'minlength': 1, 'maxlength': 150})
    # team_code = StringField(
    #     "CreativeWorkCode",
    #     # validators=[DataRequired("CreativeWorkCode必填.")],
    #     render_kw={'class': 'form-control rounded-pill', 'readonly': 'true'}
    # )

    length = TimeField('Video Length',
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
        "Video导语",
        # validators=[DataRequired("Video导语必填.")]
    )
    link = URLField('Link',
                    # validators=[DataRequired()],
                    render_kw={'placeholder': 'CreativeWorkLink', 'class': 'form-control mt-1 bg-light rounded-pill'})
    disk_link = URLField('DriveLink',
                         # validators=[DataRequired()],
                         render_kw={'placeholder': 'DriveLink', 'class': 'form-control mt-1 bg-light rounded-pill'})
    # File Edit
    # File InReview
    # Voice
    # Translate
    # TranslateCorrection
    plan = SelectField('Design(Empty Allowed)', default=0, coerce=int, render_kw={
                       'class': 'form-control mt-1 form-select border border-3 border-danger text-danger bg-light rounded-pill'})
    edit = SelectField('Edit(Empty Allowed)', default=0, coerce=int, render_kw={
                       'class': 'form-control mt-1 form-select border border-3 border-info text-info bg-light rounded-pill'})
    audit = SelectField('File InReview(Empty Allowed)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-warning bg-light text-warning rounded-pill'})
    dubb = SelectField('Voice(Empty Allowed)', default=0, coerce=int,  render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-primary text-primary bg-light rounded-pill'})
    trans = SelectField('Translate(Empty Allowed)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger bg-light rounded-pill'})
    check = SelectField('TranslateCorrection(Empty Allowed)', default=0, coerce=int,  render_kw={
                        'class': 'form-control mt-1 form-select border border-3 border-success bg-light text-success rounded-pill'})
    #
    comment = TextAreaField('Comment',
                            #   validators=[DataRequired(
                            #       message='Video Name必填.')],
                            render_kw={"placeholder": "SubmitExplain, Commentetc", 'class': 'form-control mt-1 border border-3 border-info text-primary bg-light', 'minlength': 0, 'maxlength': 350})
    #

    last = SubmitField(
        u"Previous", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    next = SubmitField(
        u"Next", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class TypeForm(FlaskForm):
    """?? Form."""

    personal = SelectField(u'MateAccount', render_kw={
        'class': 'form-control mt-1 form-select'})
    team = SelectField(u'TeamAccount', render_kw={
                       'class': 'form-control mt-1 form-select'})
    admin = SelectField(u'ManagementAccount', render_kw={
        'class': 'form-control mt-1 form-select'})
    personal_type = SelectField(
        u'AccountType', render_kw={'class': 'form-control mt-1 form-select'})
    team_type = SelectField(
        u'AccountType', render_kw={'class': 'form-control mt-1 form-select'})
    admin_type = SelectField(
        u'AccountType', render_kw={'class': 'form-control mt-1 form-select'})
    # account_type = SelectField(
    #     u'AccountType', render_kw={'class': 'form-control form-select'})
    submit = SubmitField(u"ChangeAs", render_kw={'class': 'btn btn-primary'})


class StatusForm(FlaskForm):
    """?? Form."""

    # ["Normal", "Suspending", "ReadOnly", "Locked"]
    normal = SelectField(u'Account(Normal)', render_kw={
        'class': 'form-control mt-1 form-select'})
    pending = SelectField(u'Account(Suspending)', render_kw={
        'class': 'form-control mt-1 form-select'})
    read = SelectField(u'Account(ReadOnly)', render_kw={
        'class': 'form-control mt-1 form-select'})
    locked = SelectField(
        u'Account(Locked)', render_kw={'class': 'form-control mt-1 form-select'})
    #
    status_normal = SelectField(
        u'StatusChoice', render_kw={'class': 'form-control mt-1 form-select'})
    status_pending = SelectField(
        u'StatusChoice', render_kw={'class': 'form-control mt-1 form-select'})
    status_read = SelectField(
        u'StatusChoice', render_kw={'class': 'form-control mt-1 form-select'})
    status_locked = SelectField(
        u'StatusChoice', render_kw={'class': 'form-control mt-1 form-select'})
    #
    submit = SubmitField(u"ChangeAs", render_kw={'class': 'btn btn-primary'})

# primary， success ， info ， warning ， danger ， secondary ， dark ， light，


class CreateForm(FlaskForm):
    name = StringField(u'Account Name',
                       validators=[DataRequired(message=u'Name Needed.')],
                       render_kw={"placeholder": "Account Name", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill', 'minlength': 5, 'maxlength': 150})

    email = EmailField(u'Email',
                       validators=[DataRequired(message=u'Email Address Needed'),
                                   Email(message=u'Wrong Type')],
                       render_kw={"placeholder": "Email Address", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill'})

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ], render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}
    )

    type = SelectField(u'Account Type', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})

    team = SelectField(u'Belong Team', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})

    create = SubmitField(u"Create", render_kw={'class': 'btn btn-primary w-100'})

    def validate_on_submit(self):
        if not self.name.data.strip():
            return False
        if self.type.data != 0:
            type = self.type.data
            choice = self.type.choices[type][1]
            if (u'Mate' in choice) and self.team.data == 0:
                return False
        return True

class AuditForm(FlaskForm):
    """?? Form."""
    auditing = SelectField(u'In Review', coerce=int, render_kw={
        'class': 'form-control mt-1 form-select border border-3 border-danger text-danger rounded-pill'})
    #
    title = StringField('Video Name',
                        #   validators=[DataRequired(
                        #       message='Video Name必填.')],
                        render_kw={"placeholder": "Video Name", 'class': 'form-control mt-1 border border-1 border-primary text-primar, rounded-pill', 'minlength': 5, 'maxlength': 150, 'readonly': 'true'})
    global_code = StringField(
        "CreativeWorkCode(Global)",
        # validators=[DataRequired("CreativeWorkCode必填.")],
        render_kw={
            'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'}
    )

    team_code = StringField(
        "CreativeWorkCode(Team)",
        # validators=[DataRequired("CreativeWorkCode必填.")],
        render_kw={
            'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'}
    )

    # length = TimeField('Video Length',
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
        "Video Length", render_kw={'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'}
        # validators=[DataRequired("协调必填.")]
    )

    coop = StringField(
        "协调", render_kw={'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill'}
        # validators=[DataRequired("协调必填.")]
    )
    guide = StringField(
        "Video导语", render_kw={'class': 'form-control mt-1 border border-1 border-danger, text-danger, rounded-pill'}
        # validators=[DataRequired("Video导语必填.")]
    )
    link = URLField('Link',
                    # validators=[DataRequired()],
                    render_kw={'placeholder': 'CreativeWorkLink', 'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    disk_link = URLField('DriveLink',
                         # validators=[DataRequired()],
                         render_kw={'placeholder': 'DriveLink', 'class': 'form-control mt-1 border border-1 border-dark  rounded-pill', 'readonly': 'true'})
    # primary ， success ， info ， warning ， danger ， secondary ， dark ， light ，
    plan = StringField('Design', render_kw={
                       'class': 'form-control mt-1 border border-1 border-primary text-primary rounded-pill', 'readonly': 'true'})
    plan_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-primary text-primary rounded-pill', 'readonly': 'true'})

    edit = StringField('Edit', render_kw={
                       'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'})
    edit_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-success text-success rounded-pill', 'readonly': 'true'})

    audit = StringField('File InReview', render_kw={
                        'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'})
    audit_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-info text-info rounded-pill', 'readonly': 'true'})

    dubb = StringField('Voice', render_kw={
                       'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill', 'readonly': 'true'})
    dubb_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-warning text-warning rounded-pill', 'readonly': 'true'})

    trans = StringField('Translate', render_kw={
                        'class': 'form-control mt-1 border border-1 border-danger text-danger rounded-pill', 'readonly': 'true'})
    trans_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-danger text-danger rounded-pill', 'readonly': 'true'})

    check = StringField('TranslateCorrection', render_kw={
                        'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    check_point = StringField('', render_kw={
        'class': 'form-control mt-1 border border-1 border-secondary text-secondary rounded-pill', 'readonly': 'true'})
    #
    comment = TextAreaField('Comment',
                            #   validators=[DataRequired(
                            #       message='Video Name必填.')],
                            render_kw={"placeholder": "SubmitExplain, Commentetc", 'class': 'form-control mt-1 border border-1 border-danger text-danger', 'minlength': 0, 'maxlength': 350, 'readonly': 'true'})
    comment_audit = TextAreaField('InReview Feedback',
                                  #   validators=[DataRequired(
                                  #       message='Video Name必填.')],
                                  render_kw={"placeholder": " Rejected Reasonetc", 'class': 'form-control mt-1 border border-1 border-success text-success', 'minlength': 0, 'maxlength': 350, 'resize': 'none'})
    #
    apply = SubmitField(u"Yes", render_kw={'class': 'btn btn-primary'})
    approve = SubmitField(u"Pass", render_kw={'class': 'btn btn-primary'})
    deny = SubmitField(u"Resubmit", render_kw={'class': 'btn btn-primary'})


class SettingForm(FlaskForm):
    """User Account Form."""
    name = StringField(
        u"Account Name", validators=[DataRequired()], render_kw={'class': 'form-control mt-1 border border-danger text-danger bg-light rounded-pill'})

    team_name = StringField(
        u"Team Name", render_kw={'class': 'form-control mt-1 border border-danger text-danger rounded-pill', 'readonly': 'true'})

    email = EmailField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired()
        ], render_kw={'class': 'form-control mt-1 border border-info text-info rounded-pill', 'readonly': 'true'}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ], render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}
    )
    confirm = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ], render_kw={'class': 'form-control mt-1 border border-success text-success bg-light rounded-pill'}
    )

    discord = StringField("Discord", render_kw={
                          'class': 'form-control mt-1 border border-warning text-warning bg-light rounded-pill'}, validators=None)
    farm = StringField(u"Belong Farm", render_kw={
                       'class': 'form-control mt-1 border border-success text-success bg-light rounded-pill'}, validators=None)
    twitter = StringField(
        u"Twitter Account", render_kw={'class': 'form-control mt-1 border border-primary text-primary bg-light  rounded-pill'}, validators=None)
    gettr = StringField(u"Gettr Account", render_kw={
                        'class': 'form-control mt-1 border border-dark text-dark bg-light rounded-pill'}, validators=None)
    theme = SelectField(
        u"Theme", render_kw={'class': 'form-control mt-1 border border-warning text-warning bg-light form-select rounded-pill'}, coerce=int, validators=None)

    submit = SubmitField(
        u"Change", render_kw={'class': 'form-control mt-1 border border-none text-white bg-primary rounded-pill'})


# @unique
# class E_VIDEO_TYPE (IntEnum):
#     MIC_VIDEO = 0
#     SIM_VIDEO = 1
#     REF_VIDEO = 2
#     CRT_VIDEO = 3
#     RCD_VIDEO = 4
#     UGT_VIDEO = 5
#     CHT_VIDEO = 6
# video_types = ["Tiny Video", "Simplified Video", "State StructuredVideo", "Create StructedVideo", "Documentary", "EmergencyVideo", "Interview Video"]
class WeightForm(FlaskForm):
    '''
    '''

    def __init__(self, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type == E_VIDEO_TYPE .MIC_VIDEO:
            self.name = "Tiny Video"
            self.id = 'MIC_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .SIM_VIDEO:
            self.name = "Simplified Video"
            self.id = 'SIM_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .REF_VIDEO:
            self.name = "State StructuredVideo"
            self.id = 'REF_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .CRT_VIDEO:
            self.name = "Create StructedVideo"
            self.id = 'CRT_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .RCD_VIDEO:
            self.name = "Documentary"
            self.id = 'RCD_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .UGT_VIDEO:
            self.name = "EmergencyVideo"
            self.id = 'UGT_VIDEO'.lower()
        elif type == E_VIDEO_TYPE .CHT_VIDEO:
            self.name = "Interview Video"
            self.id = 'CHT_VIDEO'.lower()
        else:
            # self.name = "FKCCP"
            # self.id = 'NSFC'.lower()
            self.mic_name = "Tiny Video"
            self.sim_name = "Simplified Video"
            self.ref_name = "State StructuredVideo"
            self.crt_name = "Create StructedVideo"
            self.rcd_name = "Documentary"
            self.ugt_name = "EmergencyVideo"
            self.cht_name = "Interview Video"
            self.mic_id = 'MIC_VIDEO'.lower()
            self.sim_id = 'SIM_VIDEO'.lower()
            self.ref_id = 'REF_VIDEO'.lower()
            self.crt_id = 'CRT_VIDEO'.lower()
            self.rcd_id = 'RCD_VIDEO'.lower()
            self.ugt_id = 'UGT_VIDEO'.lower()
            self.cht_id = 'CHT_VIDEO'.lower()

    # File Edit
    # File InReview
    # Voice
    # Translate
    # TranslateCorrection
    # indicater = StringField("(%):", validators=[DataRequired()], render_kw={
    #     'class': 'form-control border border-2 border-danger text-danger text-center', 'readonly': 'true'})

    # ["Tiny Video", "Simplified Video", "State StructuredVideo", "Create StructedVideo", "Documentary", "EmergencyVideo", "Interview Video"]
    mic_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'list': 'tickmarks', 'oninput': "weight_change(this);", 'oncdbllick': "this.disabled=false;"})

    mic_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this);"})

    mic_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    mic_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-mic', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    sim_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    sim_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-sim', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    ref_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ref_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-ref', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    crt_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    crt_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-crt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    rcd_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    rcd_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-rcd', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    ugt_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    ugt_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-ugt', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # ***********************************************************************************
    cht_plan = IntegerRangeField('DesignWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_edit = IntegerRangeField('EditWeight', default='1', render_kw={
        'class': 'form-control border border-2 border-success text-success bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_audit = IntegerRangeField('File InReviewWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_dubb = IntegerRangeField('VoiceWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_trans = IntegerRangeField('TranslateWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})

    cht_check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
        'class': 'form-control border border-2 border-secondary text-secondary bg-light mt-1 rounded-pill weight-slider weight-cht', 'min': 0, 'max': 100, 'step': 1, 'oninput': "weight_change(this)"})
    # check = IntegerRangeField('TranslateCorrectionWeight:', default='1', render_kw={
    #     'class': 'form-control border border-2 border-secondary text-secondary bg-light rounded-pill', 'min': 0, 'max': 100, 'step': 1, 'oninput': "this.previousElementSibling.previousElementSibling.innerHTML = this.value"})

    mic_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    sim_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    ref_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    crt_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    rcd_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    ugt_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
    cht_submit = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    def validate_mic(self):
        weight_total = int(self.mic_plan.raw_data[0]) + int(self.mic_edit.raw_data[0]) + int(self.mic_audit.raw_data[0]) + \
            int(self.mic_dubb.raw_data[0]) + \
            int(self.mic_trans.raw_data[0]) + int(self.mic_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_sim(self):
        weight_total = int(self.sim_plan.raw_data[0]) + int(self.sim_edit.raw_data[0]) + int(self.sim_audit.raw_data[0]) + \
            int(self.sim_dubb.raw_data[0]) + \
            int(self.sim_trans.raw_data[0]) + int(self.sim_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_ref(self):
        weight_total = int(self.ref_plan.raw_data[0]) + int(self.ref_edit.raw_data[0]) + int(self.ref_audit.raw_data[0]) + \
            int(self.ref_dubb.raw_data[0]) + \
            int(self.ref_trans.raw_data[0]) + int(self.ref_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_crt(self):
        weight_total = int(self.crt_plan.raw_data[0]) + int(self.crt_edit.raw_data[0]) + int(self.crt_audit.raw_data[0]) + \
            int(self.crt_dubb.raw_data[0]) + \
            int(self.crt_trans.raw_data[0]) + int(self.crt_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_rcd(self):
        weight_total = int(self.rcd_plan.raw_data[0]) + int(self.rcd_edit.raw_data[0]) + int(self.rcd_audit.raw_data[0]) + \
            int(self.rcd_dubb.raw_data[0]) + \
            int(self.rcd_trans.raw_data[0]) + int(self.rcd_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_ugt(self):
        weight_total = int(self.ugt_plan.raw_data[0]) + int(self.ugt_edit.raw_data[0]) + int(self.ugt_audit.raw_data[0]) + \
            int(self.ugt_dubb.raw_data[0]) + \
            int(self.ugt_trans.raw_data[0]) + int(self.ugt_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
            return False
        else:
            return True

    def validate_cht(self):
        weight_total = int(self.cht_plan.raw_data[0]) + int(self.cht_edit.raw_data[0]) + int(self.cht_audit.raw_data[0]) + \
            int(self.cht_dubb.raw_data[0]) + \
            int(self.cht_trans.raw_data[0]) + int(self.cht_check.raw_data[0])
        if weight_total > 100:
            flash(category='error', message='TotalWeight不能大于100%!')
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
    mic_video = IntegerField('Tiny Video:', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill'})

    sim_video = IntegerField('Simplified Video:', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill'})

    ref_video = IntegerField('State StructuredVideo:', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill'})

    crt_video = IntegerField('Create StructedVideo:', render_kw={
        'class': 'form-control border border-2 border-primary text-primary bg-light mt-1 rounded-pill'})

    rcd_video = IntegerField('Documentary:', render_kw={
        'class': 'form-control border border-2 border-danger text-danger bg-light mt-1 rounded-pill'})

    ugt_video = IntegerField('EmergencyVideo:', render_kw={
        'class': 'form-control border border-2 border-info text-info bg-light mt-1 rounded-pill'})

    cht_video = IntegerField('Interview Video:', render_kw={
        'class': 'form-control border border-2 border-warning text-warning bg-light mt-1 rounded-pill'})

    submit_mic = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_sim = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_ref = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_crt = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_rcd = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_ugt = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_cht = SubmitField(
        u"Setting", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class BackupForm(FlaskForm):
    '''
    '''

    backup = StringField('Database Backup:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': 'Name..'})

    submit = SubmitField(
        u"Backup", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})


class BWListForm(FlaskForm):
    '''
    '''

    black = StringField('Black List:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': 'IP'})
    black_note = StringField('Comment:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill'})

    white = StringField('White List:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill', 'placeholder': 'IP'})
    white_note = StringField('Comment:', render_kw={
        'class': 'form-control mt-1 border border-2 border-primary text-primary bg-light rounded-pill'})

    submit_black = SubmitField(
        u"Save", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})

    submit_white = SubmitField(
        u"Save", render_kw={'class': 'btn btn-primary col-sm-2 w-100'})
