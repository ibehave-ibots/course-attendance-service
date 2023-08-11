import numpy as np

from ..core.attendance_workflows import AttendeeInstance, AttendanceRepo, Session

from ...external.zoom_api import ZoomRestApi

# Implementation of AttendanceRepo
# RESPONSIBLE for AttendanceRepo contract
# For Zoom attendance
class ZoomAttendeeRepo(AttendanceRepo):
    def __init__(self, zoom_api: ZoomRestApi) -> None:
        self.api = zoom_api
        self.access_token = 'ACCESS TOKEN'

    def get_session_details(self, session_id: str) -> Session:
        meeting = self.api.get_past_meeting_details(access_token=self.access_token,meeting_id=session_id)
        report = self.api.get_zoom_participant_report(access_token=self.access_token,meeting_id=session_id)
        participants = report['participants']
        attendees = []
        for participant in participants:
            if participant['status'] == 'in_meeting':
                attendees.append(AttendeeInstance(name=participant['name'],
                         email=participant['user_email'],
                         join_start=participant['join_time'],
                         join_end=participant['leave_time']))
        return Session(
            session_id=session_id,
            start_time=meeting['start_time'],
            end_time=meeting['end_time'],
            attendees=attendees
        )

