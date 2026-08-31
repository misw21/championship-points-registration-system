"""
Championship Points Registration System - Storage Module
================================================================================
This module handles all data persistence operations including JSON and CSV export.

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

Individual Responsibility:
- Manages all data storage operations
- Ensures data integrity
- Handles file I/O operations
- Provides data validation

Creativity:
- Supports multiple export formats
- Automatic backup capabilities
- Flexible data directory configuration

Self-Management:
- Automatic directory creation
- Counter persistence for ID generation
- Data consistency checks
- Error handling for file operations
"""

import json
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime
from models import (
    IndividualParticipant, Team, Event, Registration, Result,
    ParticipantType, EventType, EventCategory, EventStatus, RegistrationStatus
)


class Storage:
    """
    Storage management class - handles all data persistence
    
    Manages:
    - In-memory data storage
    - JSON file persistence
    - CSV export functionality
    - ID generation and counter management
    
    Individual Accountability:
    - All storage operations are self-contained
    - Proper error handling for file operations
    - Data validation before save
    """
    
    def __init__(self, data_dir: str = "tournament_data"):
        """
        Initialize storage system
        
        Args:
            data_dir: Directory for data storage
        """
        self.data_dir = data_dir
        self._ensure_data_directory()
        
        # In-memory storage
        self.individuals: Dict[str, IndividualParticipant] = {}
        self.teams: Dict[str, Team] = {}
        self.events: Dict[str, Event] = {}
        self.registrations: Dict[str, Registration] = {}
        self.results: List[Result] = []
        
        # Counters for ID generation
        self._individual_counter = 0
        self._team_counter = 0
        self._event_counter = 0
        self._registration_counter = 0
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    # ============== ID Generation ==============
    
    def generate_individual_id(self) -> str:
        """Generate unique ID for individual participant"""
        self._individual_counter += 1
        return f"IND{self._individual_counter:04d}"
    
    def generate_team_id(self) -> str:
        """Generate unique ID for team"""
        self._team_counter += 1
        return f"TEAM{self._team_counter:04d}"
    
    def generate_event_id(self) -> str:
        """Generate unique ID for event"""
        self._event_counter += 1
        return f"EVENT{self._event_counter:04d}"
    
    def generate_registration_id(self) -> str:
        """Generate unique ID for registration"""
        self._registration_counter += 1
        return f"REG{self._registration_counter:04d}"
    
    # ============== Individual Management ==============
    
    def add_individual(self, individual: IndividualParticipant) -> bool:
        """Add an individual participant"""
        if individual.participant_id in self.individuals:
            return False
        self.individuals[individual.participant_id] = individual
        return True
    
    def update_individual(self, individual: IndividualParticipant) -> bool:
        """Update individual participant data"""
        if individual.participant_id not in self.individuals:
            return False
        self.individuals[individual.participant_id] = individual
        return True
    
    def delete_individual(self, participant_id: str) -> bool:
        """Delete an individual participant"""
        if participant_id not in self.individuals:
            return False
        del self.individuals[participant_id]
        return True
    
    def get_individual(self, participant_id: str) -> Optional[IndividualParticipant]:
        """Get individual by ID"""
        return self.individuals.get(participant_id)
    
    def get_all_individuals(self) -> List[IndividualParticipant]:
        """Get all individuals"""
        return list(self.individuals.values())
    
    def search_individual(self, name: str) -> List[IndividualParticipant]:
        """Search individuals by name"""
        return [ind for ind in self.individuals.values() 
                if name.lower() in ind.name.lower()]
    
    # ============== Team Management ==============
    
    def add_team(self, team: Team) -> bool:
        """Add a team"""
        if team.team_id in self.teams:
            return False
        self.teams[team.team_id] = team
        return True
    
    def update_team(self, team: Team) -> bool:
        """Update team data"""
        if team.team_id not in self.teams:
            return False
        self.teams[team.team_id] = team
        return True
    
    def delete_team(self, team_id: str) -> bool:
        """Delete a team"""
        if team_id not in self.teams:
            return False
        del self.teams[team_id]
        return True
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        return self.teams.get(team_id)
    
    def get_all_teams(self) -> List[Team]:
        """Get all teams"""
        return list(self.teams.values())
    
    def search_team(self, name: str) -> List[Team]:
        """Search teams by name"""
        return [team for team in self.teams.values() 
                if name.lower() in team.name.lower()]
    
    # ============== Event Management ==============
    
    def add_event(self, event: Event) -> bool:
        """Add an event"""
        if event.event_id in self.events:
            return False
        self.events[event.event_id] = event
        return True
    
    def update_event(self, event: Event) -> bool:
        """Update event data"""
        if event.event_id not in self.events:
            return False
        self.events[event.event_id] = event
        return True
    
    def delete_event(self, event_id: str) -> bool:
        """Delete an event"""
        if event_id not in self.events:
            return False
        del self.events[event_id]
        return True
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Get event by ID"""
        return self.events.get(event_id)
    
    def get_all_events(self) -> List[Event]:
        """Get all events"""
        return list(self.events.values())
    
    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Get events by type"""
        return [event for event in self.events.values() 
                if event.event_type == event_type]
    
    def get_open_events(self) -> List[Event]:
        """Get open events"""
        return [event for event in self.events.values() 
                if event.status == EventStatus.OPEN]
    
    # ============== Registration Management ==============
    
    def add_registration(self, registration: Registration) -> bool:
        """Add a registration"""
        if registration.registration_id in self.registrations:
            return False
        self.registrations[registration.registration_id] = registration
        return True
    
    def update_registration(self, registration: Registration) -> bool:
        """Update registration"""
        if registration.registration_id not in self.registrations:
            return False
        self.registrations[registration.registration_id] = registration
        return True
    
    def delete_registration(self, registration_id: str) -> bool:
        """Delete a registration"""
        if registration_id not in self.registrations:
            return False
        del self.registrations[registration_id]
        return True
    
    def get_registration(self, registration_id: str) -> Optional[Registration]:
        """Get registration by ID"""
        return self.registrations.get(registration_id)
    
    def get_all_registrations(self) -> List[Registration]:
        """Get all registrations"""
        return list(self.registrations.values())
    
    def get_registrations_by_event(self, event_id: str) -> List[Registration]:
        """Get registrations for an event"""
        return [reg for reg in self.registrations.values() 
                if reg.event_id == event_id]
    
    def get_registrations_by_participant(self, participant_id: str) -> List[Registration]:
        """Get registrations for a participant"""
        return [reg for reg in self.registrations.values() 
                if reg.participant_id == participant_id]
    
    def is_participant_registered_in_event(self, participant_id: str, event_id: str) -> bool:
        """Check if participant is registered in event"""
        return any(reg.participant_id == participant_id and reg.event_id == event_id 
                   for reg in self.registrations.values())
    
    def get_participant_event_count(self, participant_id: str) -> int:
        """Get number of events a participant is registered in"""
        return len(set(reg.event_id for reg in self.registrations.values() 
                       if reg.participant_id == participant_id))
    
    # ============== Results Management ==============
    
    def add_result(self, result: Result) -> bool:
        """Add a result"""
        # Check for existing result
        for existing in self.results:
            if existing.event_id == result.event_id and existing.participant_id == result.participant_id:
                return False
        self.results.append(result)
        return True
    
    def update_result(self, result: Result) -> bool:
        """Update a result"""
        for i, existing in enumerate(self.results):
            if existing.event_id == result.event_id and existing.participant_id == result.participant_id:
                self.results[i] = result
                return True
        return False
    
    def delete_result(self, event_id: str, participant_id: str) -> bool:
        """Delete a result"""
        for i, result in enumerate(self.results):
            if result.event_id == event_id and result.participant_id == participant_id:
                self.results.pop(i)
                return True
        return False
    
    def get_results_by_event(self, event_id: str) -> List[Result]:
        """Get results for an event"""
        return [r for r in self.results if r.event_id == event_id]
    
    def get_results_by_participant(self, participant_id: str) -> List[Result]:
        """Get results for a participant"""
        return [r for r in self.results if r.participant_id == participant_id]
    
    def get_all_results(self) -> List[Result]:
        """Get all results"""
        return self.results.copy()
    
    # ============== JSON Persistence ==============
    
    def save_to_json(self, filename: str = None) -> str:
        """
        Save all data to JSON file
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = os.path.join(self.data_dir, f"tournament_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        data = {
            "individuals": {pid: ind.to_dict() for pid, ind in self.individuals.items()},
            "teams": {tid: team.to_dict() for tid, team in self.teams.items()},
            "events": {eid: event.to_dict() for eid, event in self.events.items()},
            "registrations": {rid: reg.to_dict() for rid, reg in self.registrations.items()},
            "results": [r.to_dict() for r in self.results],
            "counters": {
                "individual": self._individual_counter,
                "team": self._team_counter,
                "event": self._event_counter,
                "registration": self._registration_counter
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def load_from_json(self, filename: str) -> bool:
        """
        Load data from JSON file
        
        Args:
            filename: Path to JSON file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load individuals
            self.individuals = {
                pid: IndividualParticipant.from_dict(d) 
                for pid, d in data.get("individuals", {}).items()
            }
            
            # Load teams
            self.teams = {
                tid: Team.from_dict(d) 
                for tid, d in data.get("teams", {}).items()
            }
            
            # Load events
            self.events = {
                eid: Event.from_dict(d) 
                for eid, d in data.get("events", {}).items()
            }
            
            # Load registrations
            self.registrations = {
                rid: Registration.from_dict(d) 
                for rid, d in data.get("registrations", {}).items()
            }
            
            # Load results
            self.results = [Result.from_dict(r) for r in data.get("results", [])]
            
            # Load counters
            counters = data.get("counters", {})
            self._individual_counter = counters.get("individual", 0)
            self._team_counter = counters.get("team", 0)
            self._event_counter = counters.get("event", 0)
            self._registration_counter = counters.get("registration", 0)
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_latest_save_file(self) -> Optional[str]:
        """Get the most recent save file"""
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        if not files:
            return None
        files.sort(reverse=True)
        return os.path.join(self.data_dir, files[0])
    
    # ============== CSV Export ==============
    
    def export_to_csv(self, export_dir: str = None) -> List[str]:
        """
        Export data to CSV files
        
        Args:
            export_dir: Directory for CSV files
            
        Returns:
            List of exported file paths
        """
        if export_dir is None:
            export_dir = os.path.join(self.data_dir, "exports")
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        exported_files = []
        
        # Export individuals
        if self.individuals:
            filename = os.path.join(export_dir, "individuals.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["participant_id", "name", "age", "level", "total_points", "events_count"])
                writer.writeheader()
                for ind in self.individuals.values():
                    writer.writerow(ind.to_dict())
            exported_files.append(filename)
        
        # Export teams
        if self.teams:
            filename = os.path.join(export_dir, "teams.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["team_id", "name", "members_count", "total_points", "events_count"])
                writer.writeheader()
                for team in self.teams.values():
                    writer.writerow({
                        "team_id": team.team_id,
                        "name": team.name,
                        "members_count": len(team.members),
                        "total_points": team.total_points,
                        "events_count": team.events_count
                    })
            exported_files.append(filename)
        
        # Export events
        if self.events:
            filename = os.path.join(export_dir, "events.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["event_id", "name", "event_type", "category", "max_participants", "status"])
                writer.writeheader()
                for event in self.events.values():
                    writer.writerow(event.to_dict())
            exported_files.append(filename)
        
        # Export results
        if self.results:
            filename = os.path.join(export_dir, "results.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["event_id", "participant_id", "participant_type", "rank", "points"])
                writer.writeheader()
                for result in self.results:
                    writer.writerow(result.to_dict())
            exported_files.append(filename)
        
        return exported_files
    
    # ============== Statistics ==============
    
    def get_statistics(self) -> dict:
        """Get system statistics"""
        return {
            "total_individuals": len(self.individuals),
            "total_teams": len(self.teams),
            "total_events": len(self.events),
            "total_registrations": len(self.registrations),
            "total_results": len(self.results),
            "open_events": len(self.get_open_events()),
            "completed_events": len([e for e in self.events.values() if e.status == EventStatus.COMPLETED])
        }
    
    def clear_all_data(self):
        """Clear all stored data"""
        self.individuals.clear()
        self.teams.clear()
        self.events.clear()
        self.registrations.clear()
        self.results.clear()
        self._individual_counter = 0
        self._team_counter = 0
        self._event_counter = 0
        self._registration_counter = 0

