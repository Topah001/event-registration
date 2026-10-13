"""Small in-memory event registration with capacity and FIFO waitlists."""

from dataclasses import dataclass, field


@dataclass
class Registration:
    attendee: str
    status: str
    attended: bool = False


@dataclass
class Event:
    event_id: int
    name: str
    capacity: int
    registrations: dict[str, Registration] = field(default_factory=dict)


class EventManager:
    def __init__(self):
        self.events: dict[int, Event] = {}
        self._next_id = 1

    def create_event(self, name: str, capacity: int) -> int:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Event name is required")
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 0:
            raise ValueError("Capacity must be a non-negative integer")
        event_id = self._next_id
        self._next_id += 1
        self.events[event_id] = Event(event_id, name.strip(), capacity)
        return event_id

    def _event(self, event_id: int) -> Event:
        try:
            return self.events[event_id]
        except KeyError as exc:
            raise KeyError("Event not found") from exc

    def register(self, event_id: int, attendee: str) -> str:
        event = self._event(event_id)
        if not isinstance(attendee, str) or not attendee.strip():
            raise ValueError("Attendee name is required")
        attendee = attendee.strip()
        current = event.registrations.get(attendee)
        if current and current.status != "cancelled":
            raise ValueError("Attendee already registered")
        confirmed = sum(r.status == "confirmed" for r in event.registrations.values())
        status = "confirmed" if confirmed < event.capacity else "waitlisted"
        event.registrations[attendee] = Registration(attendee, status)
        return status

    def cancel(self, event_id: int, attendee: str) -> str:
        event = self._event(event_id)
        registration = event.registrations.get(attendee)
        if registration is None or registration.status == "cancelled":
            raise KeyError("Active registration not found")
        was_confirmed = registration.status == "confirmed"
        registration.status = "cancelled"
        registration.attended = False
        if was_confirmed:
            next_up = next((r for r in event.registrations.values() if r.status == "waitlisted"), None)
            if next_up:
                next_up.status = "confirmed"
                return next_up.attendee
        return ""

    def mark_attendance(self, event_id: int, attendee: str, attended: bool = True) -> None:
        event = self._event(event_id)
        registration = event.registrations.get(attendee)
        if registration is None or registration.status != "confirmed":
            raise KeyError("Confirmed registration not found")
        registration.attended = bool(attended)

    def get_event(self, event_id: int) -> dict:
        event = self._event(event_id)
        return {
            "event_id": event.event_id,
            "name": event.name,
            "capacity": event.capacity,
            "registrations": [
                {"attendee": r.attendee, "status": r.status, "attended": r.attended}
                for r in event.registrations.values()
            ],
        }
