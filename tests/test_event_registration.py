import unittest
from event_registration import EventManager


class EventRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.manager = EventManager()
        self.event = self.manager.create_event("Python meetup", 1)

    def test_capacity_waitlist_and_fifo_promotion(self):
        self.assertEqual(self.manager.register(self.event, "Ari"), "confirmed")
        self.assertEqual(self.manager.register(self.event, "Bo"), "waitlisted")
        self.assertEqual(self.manager.register(self.event, "Cy"), "waitlisted")
        self.assertEqual(self.manager.cancel(self.event, "Ari"), "Bo")
        statuses = {r["attendee"]: r["status"] for r in self.manager.get_event(self.event)["registrations"]}
        self.assertEqual(statuses, {"Ari": "cancelled", "Bo": "confirmed", "Cy": "waitlisted"})

    def test_attendance_only_for_confirmed_registration(self):
        self.manager.register(self.event, "Ari")
        self.manager.mark_attendance(self.event, "Ari")
        self.assertTrue(self.manager.get_event(self.event)["registrations"][0]["attended"])
        self.manager.register(self.event, "Bo")
        with self.assertRaises(KeyError):
            self.manager.mark_attendance(self.event, "Bo")

    def test_cancel_allows_reregistration(self):
        self.manager.register(self.event, "Ari")
        self.manager.cancel(self.event, "Ari")
        self.assertEqual(self.manager.register(self.event, "Ari"), "confirmed")

    def test_rejects_invalid_capacity_and_duplicates(self):
        with self.assertRaises(ValueError):
            self.manager.create_event("bad", -1)
        self.manager.register(self.event, "Ari")
        with self.assertRaises(ValueError):
            self.manager.register(self.event, "Ari")


if __name__ == "__main__":
    unittest.main()
