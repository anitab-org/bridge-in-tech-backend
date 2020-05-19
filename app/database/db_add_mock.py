from datetime import datetime, timezone
from app.database.sqlalchemy_extension import db
from app.utils.bitschema_utils import *
from app.utils.enum_utils import *


def add_mock_data():

    db.drop_all()

    from app.database.models.ms_schema.user import UserModel
    from app.database.models.ms_schema.mentorship_relation import (
        MentorshipRelationModel,
    )
    from app.database.models.ms_schema.tasks_list import TasksListModel
    from app.database.models.ms_schema.task_comment import TaskCommentModel
    from app.database.models.bit_schema.organization import OrganizationModel
    from app.database.models.bit_schema.program import ProgramModel
    from app.database.models.bit_schema.user_extension import UserExtensionModel
    from app.database.models.bit_schema.personal_background import (
        PersonalBackgroundModel,
    )
    from app.database.models.bit_schema.mentorship_relation_extension import (
        MentorshipRelationExtensionModel,
    )

    db.create_all()

    # for users table dummy data

    # add user1 who is also an admin
    user1 = UserModel(
        name="testone",
        username="test0101",
        password="pbkdf2:sha256:50000$hY4PGrnp$b5c25743bc1308158d86b274af63e203ae4031061af5c7f9505c8420f50cae1d",
        email="rovexay139@prowerl.com",
        terms_and_conditions_checked=True,
    )
    user1.available_to_mentor = True
    user1.need_mentoring = True
    user1.registration_date = (
        1589151600.93296  # Sunday, 10 May 2020 11:00:00.932 PM UTC+0
    )
    user1.is_admin = True
    user1.is_email_verified = True
    user1.email_verification_date = "2020-05-11 09:39:37.950152"

    # add user2
    user2 = UserModel(
        name="testtwo",
        username="test0202",
        password="pbkdf2:sha256:50000$4CtuxCwF$8b6584ce767ba0d70312d285ea8013a0ef9480b55c1873f4376809761095c7d8",
        email="povey55047@whowlft.com",
        terms_and_conditions_checked=True,
    )
    user2.available_to_mentor = True
    user2.need_mentoring = True
    user2.registration_date = (
        1589238000.95326  # Monday, 11 May 2020 11:00:00.953 PM UTC+0
    )
    user1.is_admin = False
    user2.is_email_verified = True
    user2.email_verification_date = "2020-05-12 11:04:46.368948"

    # add user3
    user3 = UserModel(
        name="testthree",
        username="test0303",
        password="pbkdf2:sha256:50000$gGcSwNwu$1dba66ff19891770113f2ae4b1af003fd1ee5a2005af7c2f6654663ff03a281e",
        email="nohor47235@ximtyl.com",
        terms_and_conditions_checked=True,
    )
    user3.available_to_mentor = True
    user3.need_mentoring = False
    user3.registration_date = (
        1589410800.82208  # Wednesday, 13 May 2020 11:00:00.822 PM UTC+0
    )
    user3.is_admin = False
    user3.is_email_verified = True
    user3.email_verification_date = "2020-05-14 15:12:49.585829"

    # add user4
    user4 = UserModel(
        name="testfour",
        username="test0404",
        password="pbkdf2:sha256:50000$6zulJGqT$ea4d6f539654e49d7af38672798e0ec673beb4e7d70660ba6e884fd56d30c062",
        email="yeroy74921@whowlft.com",
        terms_and_conditions_checked=True,
    )
    user4.available_to_mentor = False
    user4.need_mentoring = True
    user4.registration_date = (
        1589371200.61836  # Wednesday, 13 May 2020 12:00:00.618 PM UTC+0
    )
    user4.is_admin = False
    user4.is_email_verified = False

    # add users data
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

    # save to users table
    db.session.commit()

    # for users_extension dummy data

    # user1 users_extension
    user1_extension = UserExtensionModel(
        user_id=user1.id,
        is_organization_rep=True,
        timezone=Timezone.AUSTRALIAN_EASTERN_STANDARD_TIME,
    )
    user1_extension.additional_info = {"phone": "03-88887777"}

    # user2 users_extension
    user2_extension = UserExtensionModel(
        user_id=user2.id,
        is_organization_rep=False,
        timezone=Timezone.ALASKA_STANDARD_TIME,
    )
    user2_extension.additional_info = {
        "phone": "2130-99-11-99",
        "personal_website": "testtwo@github.io",
    }

    # user3 users_extension
    user3_extension = UserExtensionModel(
        user_id=user3.id,
        is_organization_rep=True,
        timezone=Timezone.CENTRAL_EUROPEAN_TIME,
    )
    user3_extension.additional_info = {
        "mobile": "+44-5555-666-777",
        "personal_website": "testthree@github.io",
    }

    # user4 users_extension. Not yet confirm their email.
    user4_extension = UserExtensionModel(
        user_id=user4.id, is_organization_rep=False, timezone=Timezone.CHARLIE_TIME
    )

    # add users_extension data
    db.session.add(user1_extension)
    db.session.add(user2_extension)
    db.session.add(user3_extension)
    db.session.add(user4_extension)

    # save to users_extension table
    db.session.commit()

    # for personal_background dummy data

    # user1 personal_background
    user1_background = PersonalBackgroundModel(
        user_id=user1.id,
        gender=Gender.FEMALE,
        age=Age.AGE_25_TO_34,
        ethnicity=Ethnicity.CAUCASIAN,
        sexual_orientation=SexualOrientation.LGBTIA,
        religion=Religion.BUDDHISM,
        physical_ability=PhysicalAbility.WITHOUT_DISABILITY,
        mental_ability=MentalAbility.WITHOUT_DISORDER,
        socio_economic=SocioEconomic.LOWER_MIDDLE,
        highest_education=HighestEducation.BACHELOR,
        years_of_experience=YearsOfExperience.UP_TO_10,
    )
    user1_background.is_public = True

    # user2 personal_background
    user2_background = PersonalBackgroundModel(
        user_id=user2.id,
        gender=Gender.OTHER,
        age=Age.AGE_35_TO_44,
        ethnicity=Ethnicity.ASIAN,
        sexual_orientation=SexualOrientation.HETEROSEXUAL,
        religion=Religion.OTHER,
        physical_ability=PhysicalAbility.WITH_DISABILITY,
        mental_ability=MentalAbility.WITHOUT_DISORDER,
        socio_economic=SocioEconomic.BELOW_POVERTY,
        highest_education=HighestEducation.HIGH_SCHOOL,
        years_of_experience=YearsOfExperience.UP_TO_3,
    )
    user2_background.others = {"religion": "Daoism"}
    user2_background.is_public = True

    # user3 personal_background
    user3_background = PersonalBackgroundModel(
        user_id=user3.id,
        gender=Gender.DECLINED,
        age=Age.DECLINED,
        ethnicity=Ethnicity.DECLINED,
        sexual_orientation=SexualOrientation.DECLINED,
        religion=Religion.DECLINED,
        physical_ability=PhysicalAbility.DECLINED,
        mental_ability=MentalAbility.DECLINED,
        socio_economic=SocioEconomic.DECLINED,
        highest_education=HighestEducation.DECLINED,
        years_of_experience=YearsOfExperience.DECLINED,
    )
    user3_background.is_public = False

    # user4 has no background data because email has yet to be verified

    # add users background data
    db.session.add(user1_background)
    db.session.add(user2_background)
    db.session.add(user3_background)

    # save to personal_background table
    db.session.commit()

    # for organizations dummy data

    # organization1 data
    organization1 = OrganizationModel(
        rep_id=user1.id,
        name="ABC Pty Ltd",
        email="abc_pty_ltd@mail.com",
        address="506 Elizabeth St, Melbourne VIC 3000, Australia",
        website="abc_pty_ltd.com",
        timezone=user1_extension.timezone,
    )
    organization1.status = OrganizationStatus.DRAFT
    organization1.join_date = 1589284800  # Tuesday, 12 May 2020 12:00:00 PM UTC+0

    # organization2 data
    organization2 = OrganizationModel(
        rep_id=user3.id,
        name="BCD.Co",
        email="bdc_co@mail.com",
        address="Novalisstraße 10, 10115 Berlin, Germany",
        website="bcd_co.com",
        timezone=user3_extension.timezone,
    )
    organization2.rep_department = "IT Department"
    organization2.about = "This is about us..."
    organization2.phone = "+49-30-688364150"
    organization2.status = OrganizationStatus.PUBLISH
    organization2.join_date = 1589544000  # Friday, 15 May 2020 12:00:00 PM UTC+0

    # add organizations data
    db.session.add(organization1)
    db.session.add(organization2)

    # save to organizations table
    db.session.commit()

    # for programs dummy data

    # program1 data
    program1 = ProgramModel(
        program_name="Program A",
        organization_id=organization1,
        start_date=1596236400,  # Friday, 31 July 2020 11:00:00 PM UTC+0
        end_date=1598828400,  # Sunday, 30 August 2020 11:00:00 PM UTC+0
    )
    program1.creation_date = 1589457600  # Thursday, 14 May 2020 12:00:00 PM UTC+0

    # program2 data
    program2 = ProgramModel(
        program_name="Program B",
        organization_id=organization2,
        start_date=1590062400,  # Thursday, 21 May 2020 12:00:00 PM UTC+0
        end_date=1596186000,  # Friday, 31 July 2020 9:00:00 AM UTC+0
    )
    program2.description = "This is program B description..."
    program2.target_skills = ["Python", "PostgreSQL", "ReactJS"]
    program2.target_candidate = {
        "gender": Gender.FEMALE.value,
        "age": Age.AGE_45_TO_54.value,
    }
    program2.payment_amount = 2500.00
    program2.payment_currency = "GBP"
    program2.contact_type = ContactType.FACE_TO_FACE
    program2.zone = Zone.LOCAL
    program2.student_responsibility = ["responsibility1", "responsibility2"]
    program2.mentor_responsibility = ["responsibility1", "responsibility2"]
    program2.organization_responsibility = ["responsibility1", "responsibility2"]
    program2.student_requirements = ["requirement1", "requirement2"]
    program2.mentor_requirements = ["requirement1", "requirement2"]
    program2.resources_provided = ["resources1", "resources2"]
    program2.contact_name = user3.name
    program2.contact_department = "HR Department"
    program2.program_address = organization2.address
    program2.contact_phone = organization2.phone
    program2.contact_mobile = user3_extension.additional_info.get("mobile")
    program2.contact_email = user3.email
    program2.program_website = organization2.website
    program2.irc_channel = "bcd_co@zulip.chat"
    program2.tags = program2.target_skills
    program2.status = ProgramStatus.IN_PROGRESS
    program2.creation_date = 1589544000  # Friday, 15 May 2020 12:00:00 PM UTC+0

    # program3 data
    program3 = ProgramModel(
        program_name="Program C",
        organization_id=organization2,
        start_date=1594814400,  # Wednesday, 15 July 2020 12:00:00 PM UTC+0
        end_date=1598875200,  # Monday, 31 August 2020 12:00:00 PM UTC+0
    )
    program3.description = "This is program C description..."
    program3.target_skills = ["Dart", "Firebase", "Flutter"]
    program3.target_candidate = {
        "physical_ability": PhysicalAbility.WITH_DISABILITY.value,
        "sexual_orientation": SexualOrientation.LGBTIA.value,
    }
    program3.payment_amount = 3500.00
    program3.payment_currency = "GBP"
    program3.contact_type = ContactType.BOTH
    program3.zone = Zone.NATIONAL
    program3.student_responsibility = ["responsibility1", "responsibility2"]
    program3.mentor_responsibility = ["responsibility1", "responsibility2"]
    program3.organization_responsibility = ["responsibility1", "responsibility2"]
    program3.student_requirements = ["requirement1", "requirement2"]
    program3.mentor_requirements = ["requirement1", "requirement2"]
    program3.resources_provided = ["resources1", "resources2"]
    program3.contact_name = user3.name
    program3.contact_department = "HR Department"
    program3.program_address = organization2.address
    program3.contact_phone = organization2.phone
    program3.contact_mobile = user3_extension.additional_info.get("mobile")
    program3.contact_email = user3.email
    program3.program_website = organization2.website
    program3.irc_channel = "bcd_co@zulip.chat"
    program3.tags = program3.target_skills
    program3.status = ProgramStatus.OPEN
    program3.creation_date = 1589630400  # Saturday, 16 May 2020 12:00:00 PM UTC+0

    # add programs data
    db.session.add(program1)
    db.session.add(program2)
    db.session.add(program3)

    # save to programs table
    db.session.commit()

    # for mentorship_relations dummy data

    # 1st scenario.
    # Program send request to mentor and mentee

    # prepare empty tasks_list for mentorship_relation1
    tasks_list_1 = TasksListModel()
    db.session.add(tasks_list_1)
    db.session.commit()

    # create mentorship_relation1 when program sending request to mentor
    mentorship_relation1 = MentorshipRelationModel(
        action_user_id=organization2.rep_id,
        mentor_user=user1,
        mentee_user=None,
        creation_date=1589630400,  # Saturday, 16 May 2020 12:00:00 PM UTC+0
        end_date=program2.end_date,  # Friday, 31 July 2020 9:00:00 AM UTC+0 == program2 end_date
        state=MentorshipRelationState.PENDING,
        notes="Please be a mentor...",
        tasks_list=tasks_list_1,
    )
    mentorship_relation1.start_date = (
        program2.start_date
    )  # Thursday, 21 May 2020 12:00:00 PM UTC+0

    db.session.add(mentorship_relation1)
    db.session.commit()

    # initiate mentorship_relations_extension
    mentorship_relations_extension1 = MentorshipRelationExtensionModel(
        program_id=program2.id, mentorship_relation_id=mentorship_relation1.id
    )
    mentorship_relations_extension1.mentor_request_date = (
        mentorship_relation1.creation_date
    )

    db.session.add(mentorship_relations_extension1)
    db.session.commit()

    # later, mentor accepted program request
    mentorship_relation1.action_id = user1.id
    mentorship_relation1.notes = "ok, will do."
    mentorship_relations_extension1.mentor_agreed_date = (
        1589803200  # Monday, 18 May 2020 12:00:00 PM UTC+0
    )
    # update related tables
    db.session.add(mentorship_relation1)
    db.session.add(mentorship_relations_extension1)
    db.session.commit()

    # then program send request to mentee
    mentorship_relation1.action_id = organization2.rep_id
    mentorship_relation1.mentee_id = user2.id
    mentorship_relation1.notes = "You're invited to work with us as a mentee."
    mentorship_relations_extension1.mentee_request_date = (
        1589803200  # Monday, 18 May 2020 12:00:00 PM UTC+0
    )
    # update related tables
    db.session.add(mentorship_relation1)
    db.session.add(mentorship_relations_extension1)
    db.session.commit()

    # mentee accepted program request
    mentorship_relation1.action_id = user2.id
    mentorship_relation1.notes = "sure, why not."
    mentorship_relations_extension1.mentee_agreed_date = (
        1589976000  # Wednesday, 20 May 2020 12:00:00 PM UTC+0
    )
    # update mentorship_relation state
    mentorship_relation1.state = MentorshipRelationState.ACCEPTED
    mentorship_relation1.accept_date = (
        mentorship_relations_extension1.mentee_agreed_date
    )
    # update program status
    program2.status = ProgramStatus.IN_PROGRESS

    # update related tables
    db.session.add(mentorship_relation1)
    db.session.add(mentorship_relations_extension1)
    db.session.add(program2)
    db.session.commit()

    # create list of tasks assigned at the beginning of the program
    tasks_list_1_task_a = "this is task a for tasks list 1"
    tasks_list_1_task_b = "this is task b for tasks list 1"

    tasks_list_1.add_task(
        description=tasks_list_1_task_a, created_at=1590062400
    )  # Thursday, 21 May 2020 12:00:00 PM UTC+0
    tasks_list_1.add_task(
        description=tasks_list_1_task_b, created_at=1590062400
    )  # Thursday, 21 May 2020 12:00:00 PM UTC+0

    db.session.add(tasks_list_1)
    db.session.commit()

    # mentor comment on task a
    tasks_list_1_task_comment_a = TaskCommentModel(
        user_id=user1.id,
        task_id=1,
        relation_id=1,
        comment="Do you need help with the task?",
    )
    tasks_list_1_task_comment_a.creation_date = (
        1590062400  # Thursday, 21 May 2020 12:00:00 PM UTC+0 == tasks a creation date
    )

    db.session.add(tasks_list_1_task_comment_a)
    db.session.commit()

    # mentee responded to mentor comment
    tasks_list_1_task_comment_a.user_id = user2.id
    tasks_list_1_task_comment_a.comment = "Nope. All good"
    tasks_list_1_task_comment_a.modification_date = (
        1590148800  # Friday, 22 May 2020 12:00:00 PM UTC+0
    )

    db.session.add(tasks_list_1_task_comment_a)
    db.session.commit()

    # when task a completed
    tasks_list_1.update_task(
        task_id=1,
        is_done=True,
        completed_at=1590235200,  # Saturday, 23 May 2020 12:00:00 PM UTC+0
    )

    # mentor add comment on task a completion
    tasks_list_1_task_comment_a.user_id = user1.id
    tasks_list_1_task_comment_a.comment = "Well done!"
    tasks_list_1_task_comment_a.modification_date = (
        1590235200  # Saturday, 23 May 2020 12:00:00 PM UTC+0
    )

    db.session.add(tasks_list_1)
    db.session.add(tasks_list_1_task_comment_a)
    db.session.commit()

