from __future__ import annotations
from dataclasses import asdict, dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Dict

from app.workshoprepo import WorkshopRepo
from app.registrationrepo import RegistrationRepo

class ListWorkshopsPresenter(ABC):

    @abstractmethod
    def show(self, upcoming_workshops: list[WorkshopRegistrationSummary]) -> None:
        ...


@dataclass(frozen=False)
class ListWorkshopsWorkflow:
    workshop_repo: WorkshopRepo
    registration_repo: RegistrationRepo
    presenter: ListWorkshopsPresenter

    def check_upcoming_workshops(self):
        upcoming_workshop_records = self.workshop_repo.get_upcoming_workshops()
        workshop_summaries = []
        for workshop in upcoming_workshop_records:
            registration_records = self.registration_repo.get_registrations(workshop.id)
            num_approved = sum(reg.status == 'approved' for reg in registration_records)
            num_waitlisted = sum(reg.status == 'waitlisted' for reg in registration_records)
            num_rejected = sum(reg.status == 'rejected' for reg in registration_records)
            num_free_spots = workshop.capacity - num_approved


            workshop_summary = WorkshopRegistrationSummary(
                link = workshop.link,
                title = workshop.title,
                date = workshop.date,
                capacity = workshop.capacity,
                id = workshop.id,
                num_approved=num_approved,
                num_waitlisted=num_waitlisted,
                num_rejected=num_rejected,
                num_free_spots=num_free_spots,
            )
            workshop_summaries.append(workshop_summary)
        self.presenter.show(upcoming_workshops=workshop_summaries)


@dataclass
class AppModel:
    upcoming_workshops: list[WorkshopRegistrationSummary] = field(default_factory=list)


@dataclass(frozen=True)
class WorkshopRegistrationSummary:
    link: str
    title: str
    date: str
    capacity: int
    id: str
    num_approved: int
    num_waitlisted: int
    num_rejected: int
    num_free_spots: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)