# 45 — Event Registration

A functional local event-management library: create events with capacity, register attendees, place overflow registrations on a FIFO waitlist, cancel registrations (promoting the next attendee), and track attendance for confirmed attendees. Data is in memory for this prototype and is not persisted.

## Run

Requires Python 3.10+. Use `python -m unittest discover -s tests -v`. Import `EventManager` from `event_registration.py`; `create_event(name, capacity)` returns an event ID and the remaining methods operate on that ID.
