
from typing import Literal
import json
import requests
from external.zoom_api.list_registrants import ZoomRegistrant


def update_registration(access_token: str,
                        meeting_id: str,
                        registrant: ZoomRegistrant,
                        new_status: Literal["approved", "rejected"]) -> None:
    
    action_from_new_status = {"approved": "approve",
                              "rejected": "deny"}
    
    parameters = {
                "action": action_from_new_status[new_status],
                "registrants":[
                    {"email": registrant.email,
                     "id": registrant.id}
                ]
                  }
    response = requests.put(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/status",
        headers={"Authorization": f"Bearer {access_token}"},
        json=parameters
    )
    response.raise_for_status()