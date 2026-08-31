"""
Championship Points Registration System - Unit Tests
================================================================================

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

Individual Responsibility:
- Each test has clear purpose and assertions
- Self-contained test cases
- Proper setup and teardown

Creativity:
- Tests cover normal and edge cases
- Validation testing
- Integration testing

Self-Management:
- Automatic test data cleanup
- Independent test execution
- Clear pass/fail criteria
"""

import sys
import os
import unittest
from typing import Optional

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from models import (
    IndividualParticipant, Team, TeamMember, Event, Registration, Result,
    ParticipantType, EventType, EventCategory, EventStatus, RegistrationStatus, PointsSystem
)
from services import TournamentService
from storage import Storage


class TestPointsSystem(unittest.TestCase):
    """Test cases for Points System"""
    
    def test_default_points(self):
        """Test default points allocation"""
        self.assertEqual(PointsSystem.get_points(1), 10)
        self.assertEqual(PointsSystem.get_points(2), 8)
        self.assertEqual(PointsSystem.get_points(3), 6)
        self.assertEqual(PointsSystem.get_points(4), 4)
        self.assertEqual(PointsSystem.get_points(5), 2)
    
    def test_points_beyond_fifth(self):
        """Test points for ranks beyond 5th"""
        self.assertEqual(PointsSystem.get_points(6), 0)
        self.assertEqual(PointsSystem.get_points(10), 0)
    
    def test_custom_points(self):
        """Test custom points setting"""
        PointsSystem.set_points(1, 20)
        self.assertEqual(PointsSystem.get_points(1), 20)
        # Reset
        PointsSystem.set_points(1, 10)


class TestIndividualParticipant(unittest.TestCase):
    """Test cases for Individual Participant model"""
    
    def test_create_individual(self):
        """Test creating an individual participant"""
        ind = IndividualParticipant(
            participant_id="IND0001",
            name="Ahmed Mohamed",
            age=20,
            level="First Year"
        )
        self.assertEqual(ind.name, "Ahmed Mohamed")
        self.assertEqual(ind.age, 20)
        self.assertEqual(ind.total_points, 0)
    
    def test_empty_name(self):
        """Test empty name validation"""
        with self.assertRaises(ValueError):
            IndividualParticipant(
                participant_id="IND0001",
                name=""
            )
    
    def test_negative_age(self):
        """Test negative age validation"""
        with self.assertRaises(ValueError):
            IndividualParticipant(
                participant_id="IND0001",
                name="Ahmed",
                age=-5
            )
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        ind = IndividualParticipant(
            participant_id="IND0001",
            name="Ahmed",
            age=20
        )
        data = ind.to_dict()
        self.assertEqual(data["name"], "Ahmed")
        self.assertEqual(data["age"], 20)
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "participant_id": "IND0001",
            "name": "Ahmed",
            "age": 20,
            "level": "First Year",
            "total_points": 10,
            "events_count": 2
        }
        ind = IndividualParticipant.from_dict(data)
        self.assertEqual(ind.name, "Ahmed")
        self.assertEqual(ind.total_points, 10)


class TestTeam(unittest.TestCase):
    """Test cases for Team model"""
    
    def test_create_team(self):
        """Test creating a team"""
        members = [TeamMember(name=f"Member{i}") for i in range(5)]
        team = Team(
            team_id="TEAM0001",
            name="Victory Team",
            members=members
        )
        self.assertEqual(team.name, "Victory Team")
        self.assertEqual(len(team.members), 5)
    
    def test_empty_team_name(self):
        """Test empty team name validation"""
        members = [TeamMember(name=f"Member{i}") for i in range(5)]
        with self.assertRaises(ValueError):
            Team(team_id="TEAM0001", name="", members=members)
    
    def test_less_than_five_members(self):
        """Test minimum members validation"""
        members = [TeamMember(name=f"Member{i}") for i in range(3)]
        with self.assertRaises(ValueError):
            Team(team_id="TEAM0001", name="Team", members=members)
    
    def test_add_member(self):
        """Test adding a team member"""
        members = [TeamMember(name=f"Member{i}") for i in range(5)]
        team = Team(team_id="TEAM0001", name="Team", members=members)
        
        team.add_member(TeamMember(name="New Member"))
        self.assertEqual(len(team.members), 6)
    
    def test_max_members(self):
        """Test maximum members limit"""
        members = [TeamMember(name=f"Member{i}") for i in range(10)]
        team = Team(team_id="TEAM0001", name="Team", members=members)
        
        with self.assertRaises(ValueError):
            team.add_member(TeamMember(name="Extra Member"))
    
    def test_remove_member(self):
        """Test removing a team member"""
        members = [TeamMember(name=f"Member{i}") for i in range(5)]
        team = Team(team_id="TEAM0001", name="Team", members=members)
        
        result = team.remove_member("Member0")
        self.assertTrue(result)
        self.assertEqual(len(team.members), 4)


class TestEvent(unittest.TestCase):
    """Test cases for Event model"""
    
    def test_create_event(self):
        """Test creating an event"""
        event = Event(
            event_id="EVENT0001",
            name="100m Race",
            event_type=EventType.INDIVIDUAL,
            category=EventCategory.SPORTS
        )
        self.assertEqual(event.name, "100m Race")
        self.assertEqual(event.status, EventStatus.OPEN)
    
    def test_empty_event_name(self):
        """Test empty event name validation"""
        with self.assertRaises(ValueError):
            Event(
                event_id="EVENT0001",
                name="",
                event_type=EventType.INDIVIDUAL,
                category=EventCategory.SPORTS
            )
    
    def test_is_full(self):
        """Test event capacity checking"""
        event = Event(
            event_id="EVENT0001",
            name="Event",
            event_type=EventType.INDIVIDUAL,
            category=EventCategory.SPORTS,
            max_participants=10
        )
        self.assertFalse(event.is_full(5))
        self.assertTrue(event.is_full(10))
        self.assertTrue(event.is_full(15))


class TestStorage(unittest.TestCase):
    """Test cases for Storage module"""
    
    def setUp(self):
        """Setup test environment"""
        self.storage = Storage(data_dir="test_data")
    
    def tearDown(self):
        """Cleanup after tests"""
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    def test_generate_ids(self):
        """Test ID generation"""
        id1 = self.storage.generate_individual_id()
        id2 = self.storage.generate_individual_id()
        self.assertNotEqual(id1, id2)
    
    def test_add_individual(self):
        """Test adding individual"""
        ind = IndividualParticipant(
            participant_id="IND0001",
            name="Ahmed"
        )
        result = self.storage.add_individual(ind)
        self.assertTrue(result)
        
        # Try adding again
        result = self.storage.add_individual(ind)
        self.assertFalse(result)
    
    def test_get_individual(self):
        """Test getting individual"""
        ind = IndividualParticipant(
            participant_id="IND0001",
            name="Ahmed"
        )
        self.storage.add_individual(ind)
        
        retrieved = self.storage.get_individual("IND0001")
        self.assertEqual(retrieved.name, "Ahmed")
        
        not_found = self.storage.get_individual("IND9999")
        self.assertIsNone(not_found)
    
    def test_delete_individual(self):
        """Test deleting individual"""
        ind = IndividualParticipant(
            participant_id="IND0001",
            name="Ahmed"
        )
        self.storage.add_individual(ind)
        
        result = self.storage.delete_individual("IND0001")
        self.assertTrue(result)
        
        result = self.storage.delete_individual("IND0001")
        self.assertFalse(result)
    
    def test_save_and_load_json(self):
        """Test JSON save and load"""
        # Add data
        ind = IndividualParticipant(participant_id="IND0001", name="Ahmed")
        self.storage.add_individual(ind)
        
        # Save
        filename = self.storage.save_to_json("test_data/test.json")
        self.assertTrue(os.path.exists(filename))
        
        # Create new storage and load
        new_storage = Storage(data_dir="test_data")
        result = new_storage.load_from_json(filename)
        self.assertTrue(result)
        
        loaded = new_storage.get_individual("IND0001")
        self.assertEqual(loaded.name, "Ahmed")


class TestTournamentService(unittest.TestCase):
    """Test cases for Tournament Service"""
    
    def setUp(self):
        """Setup test environment"""
        self.storage = Storage(data_dir="test_data")
        self.service = TournamentService(self.storage)
    
    def tearDown(self):
        """Cleanup after tests"""
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    def test_add_individual(self):
        """Test adding individual"""
        success, message, ind = self.service.add_individual("Ahmed", 20, "First Year")
        
        self.assertTrue(success)
        self.assertIsNotNone(ind)
        self.assertEqual(ind.name, "Ahmed")
    
    def test_add_individual_empty_name(self):
        """Test adding individual with empty name"""
        success, message, ind = self.service.add_individual("")
        
        self.assertFalse(success)
        self.assertIsNone(ind)
    
    def test_add_team(self):
        """Test adding team"""
        members = ["Ahmed", "Mohamed", "Ali", "Khaled", "Saeed"]
        success, message, team = self.service.add_team("Victory Team", members)
        
        self.assertTrue(success)
        self.assertIsNotNone(team)
        self.assertEqual(len(team.members), 5)
    
    def test_add_team_less_members(self):
        """Test adding team with insufficient members"""
        members = ["Ahmed", "Mohamed"]
        success, message, team = self.service.add_team("Team", members)
        
        self.assertFalse(success)
        self.assertIsNone(team)
    
    def test_add_event(self):
        """Test adding event"""
        success, message, event = self.service.add_event(
            "100m Race",
            EventType.INDIVIDUAL,
            EventCategory.SPORTS,
            20,
            False
        )
        
        self.assertTrue(success)
        self.assertIsNotNone(event)
    
    def test_register_individual_in_individual_event(self):
        """Test registering individual in individual event"""
        # Add individual
        _, _, ind = self.service.add_individual("Ahmed")
        
        # Add individual event
        _, _, event = self.service.add_event(
            "Race",
            EventType.INDIVIDUAL,
            EventCategory.SPORTS
        )
        
        # Register
        success, message = self.service.register_participant(
            ind.participant_id,
            ParticipantType.INDIVIDUAL,
            event.event_id
        )
        
        self.assertTrue(success)
    
    def test_register_team_in_group_event(self):
        """Test registering team in group event"""
        # Add team
        members = ["Ahmed", "Mohamed", "Ali", "Khaled", "Saeed"]
        _, _, team = self.service.add_team("Victory Team", members)
        
        # Add group event
        _, _, event = self.service.add_event(
            "Football",
            EventType.GROUP,
            EventCategory.SPORTS
        )
        
        # Register
        success, message = self.service.register_participant(
            team.team_id,
            ParticipantType.TEAM,
            event.event_id
        )
        
        self.assertTrue(success)
    
    def test_register_team_in_individual_event_fail(self):
        """Test that team cannot register in individual event"""
        # Add team
        members = ["Ahmed", "Mohamed", "Ali", "Khaled", "Saeed"]
        _, _, team = self.service.add_team("Victory Team", members)
        
        # Add individual event
        _, _, event = self.service.add_event(
            "Race",
            EventType.INDIVIDUAL,
            EventCategory.SPORTS
        )
        
        # Try to register
        success, message = self.service.register_participant(
            team.team_id,
            ParticipantType.TEAM,
            event.event_id
        )
        
        self.assertFalse(success)
        self.assertIn("Cannot", message)
    
    def test_register_individual_in_group_event_fail(self):
        """Test that individual cannot register in group event"""
        # Add individual
        _, _, ind = self.service.add_individual("Ahmed")
        
        # Add group event
        _, _, event = self.service.add_event(
            "Football",
            EventType.GROUP,
            EventCategory.SPORTS
        )
        
        # Try to register
        success, message = self.service.register_participant(
            ind.participant_id,
            ParticipantType.INDIVIDUAL,
            event.event_id
        )
        
        self.assertFalse(success)
    
    def test_duplicate_registration(self):
        """Test duplicate registration prevention"""
        # Add individual and event
        _, _, ind = self.service.add_individual("Ahmed")
        _, _, event = self.service.add_event("Race", EventType.INDIVIDUAL, EventCategory.SPORTS)
        
        # Register once
        self.service.register_participant(ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        
        # Try to register again
        success, message = self.service.register_participant(
            ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id
        )
        
        self.assertFalse(success)
        self.assertIn("registered", message)
    
    def test_enter_result(self):
        """Test entering result"""
        # Add individual, event, and register
        _, _, ind = self.service.add_individual("Ahmed")
        _, _, event = self.service.add_event("Race", EventType.INDIVIDUAL, EventCategory.SPORTS)
        self.service.register_participant(ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        
        # Enter result
        success, message = self.service.enter_result(
            event.event_id,
            ind.participant_id,
            ParticipantType.INDIVIDUAL,
            1
        )
        
        self.assertTrue(success)
        
        # Check points update
        ind = self.service.storage.get_individual(ind.participant_id)
        self.assertEqual(ind.total_points, 10)  # First place = 10 points
    
    def test_calculate_rankings(self):
        """Test ranking calculation"""
        # Add participants, events, and results
        _, _, ind1 = self.service.add_individual("Ahmed")
        _, _, ind2 = self.service.add_individual("Mohamed")
        
        # Event 1
        _, _, event1 = self.service.add_event("Race", EventType.INDIVIDUAL, EventCategory.SPORTS)
        self.service.register_participant(ind1.participant_id, ParticipantType.INDIVIDUAL, event1.event_id)
        self.service.register_participant(ind2.participant_id, ParticipantType.INDIVIDUAL, event1.event_id)
        self.service.enter_result(event1.event_id, ind1.participant_id, ParticipantType.INDIVIDUAL, 1)
        self.service.enter_result(event1.event_id, ind2.participant_id, ParticipantType.INDIVIDUAL, 2)
        
        # Calculate rankings
        ind_rankings, _ = self.service.calculate_rankings()
        
        self.assertEqual(len(ind_rankings), 2)
        self.assertEqual(ind_rankings[0].participant_name, "Ahmed")  # First
        self.assertEqual(ind_rankings[1].participant_name, "Mohamed")  # Second
    
    def test_single_event_only(self):
        """Test single event only constraint"""
        # Add individual
        _, _, ind = self.service.add_individual("Ahmed")
        
        # Add single events
        _, _, event1 = self.service.add_event("Race1", EventType.INDIVIDUAL, EventCategory.SPORTS, single_event_only=True)
        _, _, event2 = self.service.add_event("Race2", EventType.INDIVIDUAL, EventCategory.SPORTS, single_event_only=True)
        
        # Register in first event
        success, _ = self.service.register_participant(
            ind.participant_id, ParticipantType.INDIVIDUAL, event1.event_id
        )
        self.assertTrue(success)
        
        # Try to register in second event
        success, message = self.service.register_participant(
            ind.participant_id, ParticipantType.INDIVIDUAL, event2.event_id
        )
        
        self.assertFalse(success)
        self.assertIn("one event", message)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        """Setup test environment"""
        self.storage = Storage(data_dir="test_data")
        self.service = TournamentService(self.storage)
    
    def tearDown(self):
        """Cleanup after tests"""
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    def test_max_events_per_participant(self):
        """Test maximum events per participant"""
        # Add individual
        _, _, ind = self.service.add_individual("Ahmed")
        
        # Add 5 events
        for i in range(5):
            _, _, event = self.service.add_event(
                f"Event{i}", EventType.INDIVIDUAL, EventCategory.SPORTS
            )
            self.service.register_participant(
                ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id
            )
        
        # Try to add 6th event
        _, _, event6 = self.service.add_event("Event6", EventType.INDIVIDUAL, EventCategory.SPORTS)
        success, message = self.service.register_participant(
            ind.participant_id, ParticipantType.INDIVIDUAL, event6.event_id
        )
        
        self.assertFalse(success)
    
    def test_event_full(self):
        """Test event capacity"""
        # Add event with max 2
        _, _, event = self.service.add_event("Event", EventType.INDIVIDUAL, EventCategory.SPORTS, max_participants=2)
        
        # Add participants
        _, _, ind1 = self.service.add_individual("Ahmed")
        _, _, ind2 = self.service.add_individual("Mohamed")
        
        self.service.register_participant(ind1.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        self.service.register_participant(ind2.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        
        # Try to add third
        _, _, ind3 = self.service.add_individual("Ali")
        success, message = self.service.register_participant(
            ind3.participant_id, ParticipantType.INDIVIDUAL, event.event_id
        )
        
        self.assertFalse(success)
        self.assertIn("full", message)
    
    def test_same_rank_not_allowed(self):
        """Test duplicate rank prevention"""
        _, _, ind1 = self.service.add_individual("Ahmed")
        _, _, ind2 = self.service.add_individual("Mohamed")
        _, _, event = self.service.add_event("Race", EventType.INDIVIDUAL, EventCategory.SPORTS)
        
        self.service.register_participant(ind1.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        self.service.register_participant(ind2.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        
        # Enter same rank
        self.service.enter_result(event.event_id, ind1.participant_id, ParticipantType.INDIVIDUAL, 1)
        success, message = self.service.enter_result(
            event.event_id, ind2.participant_id, ParticipantType.INDIVIDUAL, 1
        )
        
        self.assertFalse(success)
    
    def test_negative_rank(self):
        """Test negative rank validation"""
        _, _, ind = self.service.add_individual("Ahmed")
        _, _, event = self.service.add_event("Race", EventType.INDIVIDUAL, EventCategory.SPORTS)
        self.service.register_participant(ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id)
        
        success, message = self.service.enter_result(
            event.event_id, ind.participant_id, ParticipantType.INDIVIDUAL, -1
        )
        
        self.assertFalse(success)


if __name__ == '__main__':
    print("Running tests...")
    unittest.main(verbosity=2)


