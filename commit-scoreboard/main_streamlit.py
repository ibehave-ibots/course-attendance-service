from unittest.mock import Mock
import streamlit as st

from scoreboard.controllers import run_simulation
from scoreboard.core.app import AppModel, Application
from scoreboard.core.scoreboard_view import ComponentScoreboardView
from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker
from scoreboard.adapters.views_streamlit import TextBarStreamlitTeamScoreComponent


branches = [f'team-{n}' for n in range(1, 4)] 

if not st.session_state.get('app'):
    model = AppModel(reference_branch='main')
    model.add_teams(branches, points=0, interval=6)
    st.session_state['model'] = model
    
    view = ComponentScoreboardView(component_factory=TextBarStreamlitTeamScoreComponent)
    view.init(model=model)

    app = Application(
        view=view,
        model=model,
        vcs_repo=DummyVersionControlRepo(**{'main': 0} | {name: 0 for name in branches}),
        speaker=Mock(), #SounddeviceSpeaker(),
    )

run_simulation(app=app, vcs=app.vcs_repo)