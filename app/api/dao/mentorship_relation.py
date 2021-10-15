from datetime import datetime, timedelta
from typing import Dict
from http import HTTPStatus
from app import messages
from app.database.models.bit_schema.mentorship_relation_extension import MentorshipRelationExtensionModel
from app.database.models.bit_schema.user_extension import UserExtensionModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState


class MentorshipRelationDAO:
    """Data Access Object for mentorship relation functionalities.

    Provides various functions pertaining to mentorship.

    Attributes:
        MAXIMUM_MENTORSHIP_DURATION
        MINIMUM_MENTORSHIP_DURATION
    """

    MAXIMUM_MENTORSHIP_DURATION = timedelta(weeks=24)  # 6 months = approximately 6*4
    MINIMUM_MENTORSHIP_DURATION = timedelta(weeks=4)

    def create_mentorship_relation(self, user_id: int, data: Dict[str, str]):
        """Creates a relationship between two users.

        Establishes the mentor-mentee relationship.

        Args:
            user_id: ID of the user initiating this request. Has to be either the mentor or the mentee.
            data: List containing the mentor_id, mentee_id, end_date_timestamp and notes.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relationship is established, failure if otherwise.
        """
        action_user_id = user_id
        mentor_id = data["mentor_id"]
        mentee_id = data["mentee_id"]
        end_date_timestamp = data["end_date"]
        notes = data["notes"]

        # user_id has to match either mentee_id or mentor_id
        is_valid_user_ids = action_user_id == mentor_id or action_user_id == mentee_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTOR_OR_MENTEE, HTTPStatus.BAD_REQUEST

        # mentor_id has to be different from mentee_id
        if mentor_id == mentee_id:
            return messages.MENTOR_ID_SAME_AS_MENTEE_ID, HTTPStatus.BAD_REQUEST

        try:
            end_date_datetime = datetime.fromtimestamp(end_date_timestamp)
        except ValueError:
            return messages.INVALID_END_DATE, HTTPStatus.BAD_REQUEST

        now_datetime = datetime.now()
        if end_date_datetime < now_datetime:
            return messages.END_TIME_BEFORE_PRESENT, HTTPStatus.BAD_REQUEST

        # business logic constraints

        max_relation_duration = end_date_datetime - now_datetime
        if max_relation_duration > self.MAXIMUM_MENTORSHIP_DURATION:
            return messages.MENTOR_TIME_GREATER_THAN_MAX_TIME, HTTPStatus.BAD_REQUEST

        if max_relation_duration < self.MINIMUM_MENTORSHIP_DURATION:
            return messages.MENTOR_TIME_LESS_THAN_MIN_TIME, HTTPStatus.BAD_REQUEST

        # validate if mentor user exists
        mentor_user = UserModel.find_by_id(mentor_id)
        if mentor_user is None:
            return messages.MENTOR_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        # validate if mentor is available to mentor
        if not mentor_user.available_to_mentor:
            return messages.MENTOR_NOT_AVAILABLE_TO_MENTOR, HTTPStatus.BAD_REQUEST

        # validate if mentee user exists
        mentee_user = UserModel.find_by_id(mentee_id)
        if mentee_user is None:
            return messages.MENTEE_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        # validate if mentee is wants to be mentored
        if not mentee_user.need_mentoring:
            return messages.MENTEE_NOT_AVAIL_TO_BE_MENTORED, HTTPStatus.BAD_REQUEST

        # TODO add tests for this portion

        all_mentor_relations = (
            mentor_user.mentor_relations + mentor_user.mentee_relations
        )
        for relation in all_mentor_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTOR_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST

        all_mentee_relations = (
            mentee_user.mentor_relations + mentee_user.mentee_relations
        )
        for relation in all_mentee_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTEE_ALREADY_IN_A_RELATION, HTTPStatus.BAD_REQUEST

        # All validations were checked

        tasks_list = TasksListModel()
        tasks_list.save_to_db()

        mentorship_relation = MentorshipRelationModel(
            action_user_id=action_user_id,
            mentor_user=mentor_user,
            mentee_user=mentee_user,
            creation_date=datetime.now().timestamp(),
            end_date=end_date_timestamp,
            state=MentorshipRelationState.PENDING,
            notes=notes,
            tasks_list=tasks_list,
        )

        mentorship_relation.save_to_db()

        return messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, HTTPStatus.CREATED
