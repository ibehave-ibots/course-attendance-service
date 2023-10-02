from dataclasses import dataclass
from typing import Callable, Dict, List, Literal

from app import RegistrationRepo, RegistrationRecord
from external.zoom_api import OAuthGetToken, list_registrants
from external.zoom_api.list_registrants import ZoomRegistrant
from external.zoom_api.update_registration import zoom_call_update_registration

@dataclass(frozen=True)
class ZoomRegistrationRepo(RegistrationRepo):
    oauth_get_token: OAuthGetToken
    list_registrants: Callable = list_registrants
    zoom_call_update_registration: Callable = zoom_call_update_registration

    def get_registrations(self, workshop_id: str) -> List[RegistrationRecord]:
        access_token = self.oauth_get_token.create_access_token()["access_token"]
        registration_records = []
        zoom_status_mapping: Dict[str, Literal['approved', 'waitlisted', 'rejected']] = {
            "approved": "approved",
            "pending": "waitlisted",
            "denied": "rejected",
        }
        for status in ["approved", "pending", "denied"]:
            zoom_registrants = self.list_registrants(
                access_token=access_token, meeting_id=workshop_id, status=status
            )
            for zoom_registrant in zoom_registrants:
                zoom_registrant_status = zoom_status_mapping[zoom_registrant.status]
                registration_record = RegistrationRecord(
                    workshop_id=workshop_id,
                    name=" ".join(
                        [zoom_registrant.first_name, zoom_registrant.last_name]
                    ),
                    status= zoom_registrant_status,
                    registered_on=zoom_registrant.registered_on,
                    custom_questions=zoom_registrant.custom_questions,
                    email=zoom_registrant.email,
                    id = zoom_registrant.id                
                )
                registration_records.append(registration_record)

        return registration_records
    
    def change_registration_status(self, registration: RegistrationRecord, new_status: Literal["approved", "rejected", "waitlisted"]) -> None:
        access_token = self.oauth_get_token.create_access_token()["access_token"]
        zoom_status_mapping : Dict[str, Literal["approved", "pending", "denied"]]= {
             "approved": "approved",
             "waitlisted":"pending",
             "rejected": "denied" ,
        }
        status = zoom_status_mapping[registration.status]
        registrant = ZoomRegistrant(first_name = registration.name.rsplit(' ', 1)[0] ,
                                    last_name = registration.name.rsplit(' ', 1)[1] ,
                                    email = registration.email,
                                    status = status,
                                    registered_on = registration.registered_on,
                                    custom_questions = registration.custom_questions,
                                    id = registration.id

        )
        meeting_id = registration.workshop_id
        self.zoom_call_update_registration(
            access_token= access_token, 
            meeting_id=meeting_id,
            registrant = registrant,
            new_status= new_status
            )
        
    def update_registration(self, registration: RegistrationRecord) -> None:
        access_token = self.oauth_get_token.create_access_token()["access_token"]
        meeting_id = registration.workshop_id
        registrant: ZoomRegistrant = self.create_zoom_registrant_from_registration_record(registration)
        self.zoom_call_update_registration(
            access_token= access_token, 
            meeting_id=meeting_id,
            registrant=registrant,
            )
    
    @staticmethod
    def create_zoom_registrant_from_registration_record(registration: RegistrationRecord) -> ZoomRegistrant:
        status_mapping: dict[Literal['approved', 'waitlisted', 'rejected'], Literal['approved', 'pending', 'denied']] = {
            "approved": "approved",
            "rejected": "denied",
            }
        return ZoomRegistrant(
            first_name = registration.name.rsplit(' ', 1)[0],
            last_name = registration.name.rsplit(' ', 1)[1],
            email = registration.email,
            status = status_mapping[registration.status],
            registered_on = registration.registered_on,
            custom_questions = registration.custom_questions,
            id = registration.id
            )