import sys
sys.path.append('..')
from unittest.mock import Mock
import os
import streamlit as st
from dotenv import load_dotenv

from app.registrationrepo import RegistrationRepo
from app.workshoprepo import WorkshopRepo
from app.app import App
from app import RegistrantWorkflows, RegistrationRecord, ListWorkshopsWorkflow, AttendanceWorkflow
from web.presenters import RegistrantPresenter, WorkshopPresenter
from web.view import View
from web.view_model import AppState, ViewModel
from adapters import ZoomRegistrationRepo, ZoomWorkshopRepo
from adapters.registrationrepo_inmemory import InMemoryRegistrationRepo
from adapters.workshoprepo_inmemory import InMemoryWorkshopRepo, WorkshopRecord
from external.zoom_api import list_registrants, OAuthGetToken, zoom_call_update_registration, list_group_members, get_meeting, get_meetings


if 'initialized' not in st.session_state: 
    load_dotenv()

    # Build plugins
    workshop_repo: WorkshopRepo
    registration_repo: RegistrationRepo
    if os.environ.get("PRODUCTION") == '1':
        oauth_get_token = OAuthGetToken(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            account_id=os.environ["ACCOUNT_ID"],
        )
        workshop_repo = ZoomWorkshopRepo(
            oauth_get_token=oauth_get_token, 
            get_meeting=get_meeting, 
            get_meetings=get_meetings, 
            list_group_members=list_group_members, 
            group_id=os.environ['TEST_GROUP_ID']
            )
        registration_repo = ZoomRegistrationRepo(
            oauth_get_token=oauth_get_token,
            list_registrants=list_registrants,
            zoom_call_update_registration=zoom_call_update_registration
            )
    else:
        workshop_repo = InMemoryWorkshopRepo()
        workshop_repo.add_workshop(
            workshop=WorkshopRecord(
                id='12345',
                link='www.fakeworkshops.com/12345',
                title='Intro to Python',
                date='11-05-2023',
                capacity=14,
            )
        )
        workshop_repo.add_workshop(
            workshop=WorkshopRecord(
                id='54321',
                link='www.fakeworkshops.com/54321',
                title='Intro to Matlab',
                date='11-15-2023',
                capacity=20,
            )
        )
        registration_repo = InMemoryRegistrationRepo(
            registrations=[
                RegistrationRecord(
                    id="54321",
                    workshop_id="12345",
                    name="eve",
                    email="e@e.com",
                    registered_on="25092023",
                    custom_questions=[{'value': 'Prof. Sangee'}],
                    status='approved',
                ),
                RegistrationRecord(
                    id="11111",
                    workshop_id="12345",
                    name="adam",
                    email="a@a.com",
                    registered_on="26092023",
                    custom_questions=[{'value': 'Prof. Bee'}],
                    status='waitlisted',
                ),
            ],
        )

    # Assemble App
    app_state = AppState(data=ViewModel())
    view = View(
        controller=App(
            workshop_workflow=ListWorkshopsWorkflow(
                workshop_repo=workshop_repo,
                registration_repo=registration_repo,
                presenter=WorkshopPresenter(state=app_state),
            ),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=registration_repo,
                presenter=RegistrantPresenter(state=app_state),
            ),
            attendance_workflow=Mock(AttendanceWorkflow)
        )
    )

    # Store App for future runs
    st.session_state['initialized'] = True
    st.session_state['render'] = lambda: view.render(app_state.data)
    

# Render (runs each ui update)
st.session_state['render']()
    
    