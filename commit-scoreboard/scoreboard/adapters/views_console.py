from pprint import pprint

from scoreboard.core.app import AppModel, ScoreboardView


class ConsoleView2(ScoreboardView):
    def __init__(self) -> None:
        self.first_shown = False

    def _show_header(self, model: AppModel):
        line = '|'
        for team, status in model.statuses.items():
            entry = f' {team:<8}|'
            line += entry
        print(line)

    def update(self, model: AppModel) -> None:
        if not self.first_shown:
            self._show_header(model=model)
            self.first_shown = True

        line = '|'
        for team, status in model.statuses.items():
            ding = "*" if status.play_sound else ""
            entry = f' {str(status.points) + ding:<8}|'
            line += entry
        print(line)


class DebuggerView(ScoreboardView):
    def update(self, model: AppModel) -> None:
        pprint(dict(model.statuses))

