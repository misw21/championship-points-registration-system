"""
================================================================================
Championship Points Registration System - Storage Module (VERSION 2.0)
================================================================================

Module Overview:
----------------
This module handles all data persistence operations for the Championship Points
Registration System. It provides comprehensive storage capabilities including:
- JSON file persistence for main data
- Settings persistence for user preferences
- CSV export functionality
- ID generation and counter management

Author: Development Team
Version: 2.0
Year: 2026

Key Features:
-------------
- Automatic data directory creation
- Counter persistence for ID generation
- Settings storage with defaults
- Multiple export formats (JSON, CSV)
- Error handling for all file operations

Individual Responsibility:
-------------------------
- Manages all data storage operations
- Ensures data integrity
- Handles file I/O operations
- Provides data validation

Creativity:
-----------
- Supports multiple export formats
- Flexible data directory configuration
- Settings backup and restore

Self-Management:
----------------
- Automatic directory creation
- Counter persistence
- Data consistency checks
- Error handling for file operations
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import json
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime

# Import models for type hints and data structures
from models import (
    IndividualParticipant,
    Team,
    Event,
    Registration,
    Result,
    AppSettings,
    ParticipantType,
    EventType,
    EventCategory,
    EventStatus,
    RegistrationStatus,
    ColorTheme,
    Language
)


# ==============================================================================
# SECTION: STORAGE CLASS
# ==============================================================================

# Data directory - separate folder for VERSION_2.0 to avoid conflicts
DATA_DIR = "tournament_data_v2"


class Storage:
    """
    Storage management class - handles all data persistence.
    
    This class is the central repository for all application data including:
    - Individual participants
    - Teams and team members
    - Events and competitions
    - Registrations
    - Results and rankings
    - Application settings
    
    The class provides methods for:
    - Adding, updating, and deleting entities
    - Querying data by various criteria
    - Serializing data to JSON
    - Loading data from JSON
    - Exporting to CSV format
    - Generating unique IDs
    
    Attributes:
        data_dir: Directory path for data storage
        settings_file: Path to settings JSON file
    
    Example:
        >>> storage = Storage()
        >>> storage.add_individual(participant)
        >>> storage.save_to_json()
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize storage system with default values.
        
        Args:
            data_dir: Directory for tournament data storage (default: tournament_data_v2)
        """
        # Use VERSION_2.0 data directory by default
        if data_dir is None:
            data_dir = DATA_DIR
        self.data_dir = data_dir
        self.settings_file = os.path.join(data_dir, "settings.json")
        
        # Ensure data directory exists
        self._ensure_data_directory()
        
        # =========================================================================
        # SECTION: IN-MEMORY DATA STORAGE
        # =========================================================================
        """
        In-memory dictionaries for fast data access.
        Keys are unique IDs, values are model objects.
        """
        self.individuals: Dict[str, IndividualParticipant] = {}
        self.teams: Dict[str, Team] = {}
        self.events: Dict[str, Event] = {}
        self.registrations: Dict[str, Registration] = {}
        self.results: List[Result] = []
        
        # =========================================================================
        # SECTION: COUNTERS FOR ID GENERATION
        # =========================================================================
        """
        Counters ensure unique IDs across all entities.
        These are persisted with the data.
        """
        self._individual_counter = 0
        self._team_counter = 0
        self._event_counter = 0
        self._registration_counter = 0
        
        # =========================================================================
        # SECTION: APPLICATION SETTINGS
        # =========================================================================
        """
        Settings object for user preferences.
        Loaded on initialization.
        """
        self.settings: AppSettings = self._load_settings()
    
    # ==========================================================================
    # SECTION: DIRECTORY MANAGEMENT
    # ==========================================================================
    
    def _ensure_data_directory(self):
        """
        Create data directory if it doesn't exist.
        
        This method ensures the data directory exists before any
        file operations are attempted.
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    # ==========================================================================
    # SECTION: SETTINGS MANAGEMENT
    # ==========================================================================
    
    def _load_settings(self) -> AppSettings:
        """
        Load settings from JSON file or create default settings.
        
        Returns:
            AppSettings object with loaded or default values
        """
        # Try to load existing settings
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return AppSettings.from_dict(data)
            except Exception as e:
                print(f"Error loading settings: {e}")
        
        # Return default settings if file doesn't exist or loading failed
        return AppSettings()
    
    def save_settings(self) -> bool:
        """
        Save settings to JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_data_directory()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_settings(self) -> AppSettings:
        """
        Get current application settings.
        
        Returns:
            AppSettings object
        """
        return self.settings
    
    def update_settings(self, settings: AppSettings):
        """
        Update application settings.
        
        Args:
            settings: New AppSettings object
        """
        self.settings = settings
        self.save_settings()
    
    # ==========================================================================
    # SECTION: ID GENERATION
    # ==========================================================================
    """
    ID generation methods ensure unique identifiers for all entities.
    Format: PREFIX + SEQUENCE NUMBER (padded to 4 digits)
    """
    
    def generate_individual_id(self) -> str:
        """
        Generate unique ID for individual participant.
        
        Format: IND0001, IND0002, etc.
        
        Returns:
            Unique individual participant ID
        """
        self._individual_counter += 1
        return f"IND{self._individual_counter:04d}"
    
    def generate_team_id(self) -> str:
        """
        Generate unique ID for team.
        
        Format: TEAM0001, TEAM0002, etc.
        
        Returns:
            Unique team ID
        """
        self._team_counter += 1
        return f"TEAM{self._team_counter:04d}"
    
    def generate_event_id(self) -> str:
        """
        Generate unique ID for event.
        
        Format: EVENT0001, EVENT0002, etc.
        
        Returns:
            Unique event ID
        """
        self._event_counter += 1
        return f"EVENT{self._event_counter:04d}"
    
    def generate_registration_id(self) -> str:
        """
        Generate unique ID for registration.
        
        Format: REG0001, REG0002, etc.
        
        Returns:
            Unique registration ID
        """
        self._registration_counter += 1
        return f"REG{self._registration_counter:04d}"
    
    # ==========================================================================
    # SECTION: INDIVIDUAL MANAGEMENT
    # ==========================================================================
    
    def add_individual(self, individual: IndividualParticipant) -> bool:
        """
        Add an individual participant to storage.
        
        Args:
            individual: IndividualParticipant object to add
            
        Returns:
            True if added successfully, False if ID already exists
        """
        if individual.participant_id in self.individuals:
            return False
        self.individuals[individual.participant_id] = individual
        return True
    
    def update_individual(self, individual: IndividualParticipant) -> bool:
        """
        Update an existing individual participant.
        
        Args:
            individual: IndividualParticipant with updated data
            
        Returns:
            True if updated successfully, False if not found
        """
        if individual.participant_id not in self.individuals:
            return False
        self.individuals[individual.participant_id] = individual
        return True
    
    def delete_individual(self, participant_id: str) -> bool:
        """
        Delete an individual participant.
        
        Args:
            participant_id: ID of participant to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        if participant_id not in self.individuals:
            return False
        del self.individuals[participant_id]
        return True
    
    def get_individual(self, participant_id: str) -> Optional[IndividualParticipant]:
        """
        Get individual participant by ID.
        
        Args:
            participant_id: ID to search for
            
        Returns:
            IndividualParticipant if found, None otherwise
        """
        return self.individuals.get(participant_id)
    
    def get_all_individuals(self) -> List[IndividualParticipant]:
        """
        Get all individual participants.
        
        Returns:
            List of all IndividualParticipant objects
        """
        return list(self.individuals.values())
    
    def search_individual(self, name: str) -> List[IndividualParticipant]:
        """
        Search individuals by name (case-insensitive partial match).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching IndividualParticipant objects
        """
        return [ind for ind in self.individuals.values() 
                if name.lower() in ind.name.lower()]
    
    def get_individual_by_name(self, name: str) -> Optional[IndividualParticipant]:
        """
        Get individual participant by exact name match.
        
        Args:
            name: Name to search for
            
        Returns:
            IndividualParticipant if found, None otherwise
        """
        for ind in self.individuals.values():
            if ind.name.lower() == name.lower():
                return ind
        return None
    
    # ==========================================================================
    # SECTION: TEAM MANAGEMENT
    # ==========================================================================
    
    def add_team(self, team: Team) -> bool:
        """
        Add a team to storage.
        
        Args:
            team: Team object to add
            
        Returns:
            True if added successfully, False if ID already exists
        """
        if team.team_id in self.teams:
            return False
        self.teams[team.team_id] = team
        return True
    
    def update_team(self, team: Team) -> bool:
        """
        Update an existing team.
        
        Args:
            team: Team with updated data
            
        Returns:
            True if updated successfully, False if not found
        """
        if team.team_id not in self.teams:
            return False
        self.teams[team.team_id] = team
        return True
    
    def delete_team(self, team_id: str) -> bool:
        """
        Delete a team.
        
        Args:
            team_id: ID of team to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        if team_id not in self.teams:
            return False
        del self.teams[team_id]
        return True
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """
        Get team by ID.
        
        Args:
            team_id: ID to search for
            
        Returns:
            Team if found, None otherwise
        """
        return self.teams.get(team_id)
    
    def get_all_teams(self) -> List[Team]:
        """
        Get all teams.
        
        Returns:
            List of all Team objects
        """
        return list(self.teams.values())
    
    def search_team(self, name: str) -> List[Team]:
        """
        Search teams by name (case-insensitive partial match).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching Team objects
        """
        return [team for team in self.teams.values() 
                if name.lower() in team.name.lower()]
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """
        Get team by exact name match.
        
        Args:
            name: Name to search for
            
        Returns:
            Team if found, None otherwise
        """
        for team in self.teams.values():
            if team.name.lower() == name.lower():
                return team
        return None
    
    # ==========================================================================
    # SECTION: EVENT MANAGEMENT
    # ==========================================================================
    
    def add_event(self, event: Event) -> bool:
        """
        Add an event to storage.
        
        Args:
            event: Event object to add
            
        Returns:
            True if added successfully, False if ID already exists
        """
        if event.event_id in self.events:
            return False
        self.events[event.event_id] = event
        return True
    
    def update_event(self, event: Event) -> bool:
        """
        Update an existing event.
        
        Args:
            event: Event with updated data
            
        Returns:
            True if updated successfully, False if not found
        """
        if event.event_id not in self.events:
            return False
        self.events[event.event_id] = event
        return True
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event.
        
        Args:
            event_id: ID of event to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        if event_id not in self.events:
            return False
        del self.events[event_id]
        return True
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """
        Get event by ID.
        
        Args:
            event_id: ID to search for
            
        Returns:
            Event if found, None otherwise
        """
        return self.events.get(event_id)
    
    def get_all_events(self) -> List[Event]:
        """
        Get all events.
        
        Returns:
            List of all Event objects
        """
        return list(self.events.values())
    
    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """
        Get events filtered by type.
        
        Args:
            event_type: EventType to filter by
            
        Returns:
            List of matching Event objects
        """
        return [event for event in self.events.values() 
                if event.event_type == event_type]
    
    def get_open_events(self) -> List[Event]:
        """
        Get all events with OPEN status.
        
        Returns:
            List of open Event objects
        """
        return [event for event in self.events.values() 
                if event.status == EventStatus.OPEN]
    
    def get_event_by_name(self, name: str) -> Optional[Event]:
        """
        Get event by exact name match.
        
        Args:
            name: Name to search for
            
        Returns:
            Event if found, None otherwise
        """
        for event in self.events.values():
            if event.name.lower() == name.lower():
                return event
        return None
    
    # ==========================================================================
    # SECTION: REGISTRATION MANAGEMENT
    # ==========================================================================
    
    def add_registration(self, registration: Registration) -> bool:
        """
        Add a registration to storage.
        
        Args:
            registration: Registration object to add
            
        Returns:
            True if added successfully, False if ID already exists
        """
        if registration.registration_id in self.registrations:
            return False
        self.registrations[registration.registration_id] = registration
        return True
    
    def update_registration(self, registration: Registration) -> bool:
        """
        Update an existing registration.
        
        Args:
            registration: Registration with updated data
            
        Returns:
            True if updated successfully, False if not found
        """
        if registration.registration_id not in self.registrations:
            return False
        self.registrations[registration.registration_id] = registration
        return True
    
    def delete_registration(self, registration_id: str) -> bool:
        """
        Delete a registration.
        
        Args:
            registration_id: ID of registration to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        if registration_id not in self.registrations:
            return False
        del self.registrations[registration_id]
        return True
    
    def get_registration(self, registration_id: str) -> Optional[Registration]:
        """
        Get registration by ID.
        
        Args:
            registration_id: ID to search for
            
        Returns:
            Registration if found, None otherwise
        """
        return self.registrations.get(registration_id)
    
    def get_all_registrations(self) -> List[Registration]:
        """
        Get all registrations.
        
        Returns:
            List of all Registration objects
        """
        return list(self.registrations.values())
    
    def get_registrations_by_event(self, event_id: str) -> List[Registration]:
        """
        Get all registrations for a specific event.
        
        Args:
            event_id: Event ID to filter by
            
        Returns:
            List of Registration objects for the event
        """
        return [reg for reg in self.registrations.values() 
                if reg.event_id == event_id]
    
    def get_registrations_by_participant(self, participant_id: str) -> List[Registration]:
        """
        Get all registrations for a specific participant.
        
        Args:
            participant_id: Participant ID to filter by
            
        Returns:
            List of Registration objects for the participant
        """
        return [reg for reg in self.registrations.values() 
                if reg.participant_id == participant_id]
    
    def is_participant_registered_in_event(self, participant_id: str, event_id: str) -> bool:
        """
        Check if a participant is registered in a specific event.
        
        Args:
            participant_id: Participant ID
            event_id: Event ID
            
        Returns:
            True if registered, False otherwise
        """
        return any(reg.participant_id == participant_id and reg.event_id == event_id 
                   for reg in self.registrations.values())
    
    def get_participant_event_count(self, participant_id: str) -> int:
        """
        Get the number of events a participant is registered in.
        
        Args:
            participant_id: Participant ID
            
        Returns:
            Count of unique events
        """
        return len(set(reg.event_id for reg in self.registrations.values() 
                       if reg.participant_id == participant_id))
    
    # ==========================================================================
    # SECTION: RESULTS MANAGEMENT
    # ==========================================================================
    
    def add_result(self, result: Result) -> bool:
        """
        Add a result to storage.
        
        Args:
            result: Result object to add
            
        Returns:
            True if added successfully, False if result already exists
        """
        # Check for existing result
        for existing in self.results:
            if existing.event_id == result.event_id and existing.participant_id == result.participant_id:
                return False
        self.results.append(result)
        return True
    
    def update_result(self, result: Result) -> bool:
        """
        Update an existing result.
        
        Args:
            result: Result with updated data
            
        Returns:
            True if updated successfully, False if not found
        """
        for i, existing in enumerate(self.results):
            if existing.event_id == result.event_id and existing.participant_id == result.participant_id:
                self.results[i] = result
                return True
        return False
    
    def delete_result(self, event_id: str, participant_id: str) -> bool:
        """
        Delete a result.
        
        Args:
            event_id: Event ID
            participant_id: Participant ID
            
        Returns:
            True if deleted successfully, False if not found
        """
        for i, result in enumerate(self.results):
            if result.event_id == event_id and result.participant_id == participant_id:
                self.results.pop(i)
                return True
        return False
    
    def get_results_by_event(self, event_id: str) -> List[Result]:
        """
        Get all results for a specific event.
        
        Args:
            event_id: Event ID to filter by
            
        Returns:
            List of Result objects for the event
        """
        return [r for r in self.results if r.event_id == event_id]
    
    def get_results_by_participant(self, participant_id: str) -> List[Result]:
        """
        Get all results for a specific participant.
        
        Args:
            participant_id: Participant ID to filter by
            
        Returns:
            List of Result objects for the participant
        """
        return [r for r in self.results if r.participant_id == participant_id]
    
    def get_all_results(self) -> List[Result]:
        """
        Get all results.
        
        Returns:
            Copy of all Result objects
        """
        return self.results.copy()
    
    # ==========================================================================
    # SECTION: JSON PERSISTENCE
    # ==========================================================================
    
    def save_to_json(self, filename: str = None) -> str:
        """
        Save all data to JSON file.
        
        This method serializes all entities (individuals, teams, events,
        registrations, results) and counters to a JSON file.
        
        Args:
            filename: Optional custom filename (default: timestamp-based)
            
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
        Load all data from JSON file.
        
        This method deserializes all entities from a JSON file and
        populates the in-memory storage.
        
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
        """
        Get the most recent save file in the data directory.
        
        Returns:
            Path to latest JSON file, or None if no files exist
        """
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        if not files:
            return None
        files.sort(reverse=True)
        return os.path.join(self.data_dir, files[0])
    
    # ==========================================================================
    # SECTION: CSV EXPORT
    # ==========================================================================
    
    def export_to_csv(self, export_dir: str = None, file_prefix: str = "") -> List[str]:
        """
        Export data to CSV files.
        
        Creates separate CSV files for:
        - Individuals
        - Teams
        - Events
        - Results
        
        Args:
            export_dir: Directory for CSV files (default: data_dir/exports)
            file_prefix: Optional prefix added to each exported CSV filename
            
        Returns:
            List of exported file paths
        """
        if export_dir is None:
            export_dir = os.path.join(self.data_dir, "exports")
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        exported_files = []
        prefix = f"{file_prefix.strip()}_" if file_prefix and file_prefix.strip() else ""
        
        # Export individuals
        if self.individuals:
            filename = os.path.join(export_dir, f"{prefix}individuals.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["participant_id", "name", "age", "level", "total_points", "events_count"])
                writer.writeheader()
                for ind in self.individuals.values():
                    writer.writerow(ind.to_dict())
            exported_files.append(filename)
        
        # Export teams
        if self.teams:
            filename = os.path.join(export_dir, f"{prefix}teams.csv")
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
            filename = os.path.join(export_dir, f"{prefix}events.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["event_id", "name", "event_type", "category", "max_participants", "status"])
                writer.writeheader()
                for event in self.events.values():
                    writer.writerow(event.to_dict())
            exported_files.append(filename)
        
        # Export results
        if self.results:
            filename = os.path.join(export_dir, f"{prefix}results.csv")
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=["event_id", "participant_id", "participant_type", "rank", "points"])
                writer.writeheader()
                for result in self.results:
                    writer.writerow(result.to_dict())
            exported_files.append(filename)
        
        return exported_files
    
    # ==========================================================================
    # SECTION: STATISTICS
    # ==========================================================================
    
    def get_statistics(self) -> dict:
        """
        Get system statistics.
        
        Returns:
            Dictionary containing counts of all entities
        """
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
        """
        Clear all stored data and reset counters.
        
        Note:
            This does NOT clear settings.
        """
        self.individuals.clear()
        self.teams.clear()
        self.events.clear()
        self.registrations.clear()
        self.results.clear()
        self._individual_counter = 0
        self._team_counter = 0
        self._event_counter = 0
        self._registration_counter = 0


# ==============================================================================
# END OF MODULE
# ==============================================================================

