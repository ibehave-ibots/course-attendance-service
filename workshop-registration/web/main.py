import sys
from unittest.mock import Mock
sys.path.append('..')

import streamlit as st

from app.app import App
from app import RegistrantWorkflows, RegistrationRecord
from web.presenter import Observable, Presenter
from web.view import View
from web.view_model import ViewModel
from web.observable import Observable
from adapters import InMemoryRegistrationRepo


if 'initialized' not in st.session_state:

    repo = InMemoryRegistrationRepo(
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

    
    app_state = Observable(data=ViewModel())
    presenter = Presenter(state=app_state)
    view = View(
        controller=App(
            workshop_workflow=Mock(),
            registrant_workflows=RegistrantWorkflows(
                registration_repo=repo,
                presenter=presenter,
            )
        )
    )
    app_state.updated.connect(view.render)
    app_state.send_all()
    st.session_state['initialized'] = True
    