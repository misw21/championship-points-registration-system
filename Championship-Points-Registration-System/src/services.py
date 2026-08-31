"""
================================================================================
Championship Points Registration System - Business Services (VERSION 2.0)
================================================================================

Module Overview:
----------------
This module contains all business logic and service operations for the system.
It acts as an intermediary layer between the GUI (presentation) and Storage
(data persistence). All core functionality is implemented here with proper
validation, error handling, and business rules.

Author: Development Team
Version: 2.0
Year: 2026

Key Features:
-------------
- Individual and Team participant management
- Event creation and management
- Registration system with validation
- Results entry and ranking calculation
- Points system management
- Statistics and reporting

Individual Responsibility:
---------------------------
- Each service method has clear input validation
- Comprehensive error handling
- Detailed logging and audit trail
- Self-contained business logic

Creativity:
-----------
- Flexible points system
- Event type validation
- Participant eligibility checking
- Results validation

Self-Management:
----------------
- Automatic points calculation
- Ranking computation
- Statistics generation
- Event status management
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from typing import List, Optional, Tuple, Dict

# Import all models and enums
from models import (
    IndividualParticipant,
    Team,
    TeamMember,
    Event,
    Registration,
    Result,
    Ranking,
    ParticipantType,
    EventType,
    EventCategory,
    EventStatus,
    RegistrationStatus,
    PointsSystem,
    AppSettings,
    ColorTheme,
    Language,
    FontSize
)

# Import storage for data persistence
from storage import Storage


# ==============================================================================
# SECTION: TOURNAMENT SERVICE CLASS
# ==============================================================================

class TournamentService:
    """
    Tournament management service - handles all business logic.
    
    This class serves as the main service layer for tournament management.
    It provides methods for managing participants, teams, events, registrations,
    results, and rankings. All operations are validated and return consistent
    response types for error handling.
    
    Attributes:
        storage: Storage instance for data persistence
        max_events_per_participant: Maximum events a participant can join
    
    Individual Accountability:
    ---------------------------
    - All operations are validated before execution
    - Clear success/failure returns with descriptive messages
    - Comprehensive error handling
    
    Example:
        >>> service = TournamentService(Storage())
        >>> success, message, individual = service.add_individual("John Doe", age=25)
        >>> print(success, message)
        True Individual added successfully (ID: IND0001)
    """
    
    def __init__(self, storage: Storage):
        """
        Initialize service with storage instance.
        
        Args:
            storage: Storage instance for data persistence
        """
        self.storage = storage
        self.max_events_per_participant = 5  # Maximum events per participant
    
    # ==========================================================================
    # SECTION: SETTINGS MANAGEMENT
    # ==========================================================================
    
    def get_settings(self) -> AppSettings:
        """
        Get current application settings.
        
        Returns:
            AppSettings object with current preferences
        """
        return self.storage.get_settings()
    
    def update_settings(self, settings: AppSettings) -> bool:
        """
        Update application settings.
        
        Args:
            settings: New AppSettings object
            
        Returns:
            True if successful, False otherwise
        """
        return self.storage.update_settings(settings)
    
    def set_volume(self, volume: float) -> Tuple[bool, str]:
        """
        Set the volume level.
        
        Args:
            volume: Volume level between 0.0 and 1.0
            
        Returns:
            Tuple of (success, message)
        """
        try:
            settings = self.storage.get_settings()
            settings.set_volume(volume)
            self.storage.save_settings()
            return True, f"Volume set to {int(volume * 100)}%"
        except ValueError as e:
            return False, str(e)
    
    def increase_volume(self) -> Tuple[bool, str]:
        """
        Increase volume by 10%.
        
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.increase_volume()
        self.storage.save_settings()
        return True, f"Volume increased to {int(settings.volume * 100)}%"
    
    def decrease_volume(self) -> Tuple[bool, str]:
        """
        Decrease volume by 10%.
        
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.decrease_volume()
        self.storage.save_settings()
        return True, f"Volume decreased to {int(settings.volume * 100)}%"
    
    def toggle_sound(self) -> Tuple[bool, str]:
        """
        Toggle sound effects on/off.
        
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        enabled = settings.toggle_sound()
        self.storage.save_settings()
        status = "enabled" if enabled else "disabled"
        return True, f"Sound {status}"
    
    def set_language(self, language: Language) -> Tuple[bool, str]:
        """
        Set the UI language.
        
        Args:
            language: Language enumeration value
            
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.set_language(language)
        self.storage.save_settings()
        return True, f"Language changed to {language.value}"
    
    def set_theme(self, theme: ColorTheme) -> Tuple[bool, str]:
        """
        Set the color theme.
        
        Args:
            theme: ColorTheme enumeration value
            
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.set_theme(theme)
        self.storage.save_settings()
        return True, f"Theme changed to {theme.value}"
    
    def set_logo_path(self, path: str) -> Tuple[bool, str]:
        """
        Set custom logo image path.
        
        Args:
            path: Path to logo image file
            
        Returns:
            Tuple of (success, message)
        """
        import os
        if path and not os.path.exists(path):
            return False, "Image file not found"
        
        settings = self.storage.get_settings()
        settings.logo_path = path
        self.storage.save_settings()
        return True, "Logo updated successfully"
    
    def mark_video_watched(self):
        """
        Mark video guide as watched.
        """
        settings = self.storage.get_settings()
        settings.video_guide_watched = True
        self.storage.save_settings()
    
    def set_font_size(self, font_size: FontSize) -> Tuple[bool, str]:
        """
        Set the font size for accessibility.
        
        Args:
            font_size: FontSize enumeration value
            
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.font_size = font_size
        self.storage.save_settings()
        return True, f"Font size changed to {font_size.value}"
    
    def set_custom_title(self, title: str) -> Tuple[bool, str]:
        """
        Set custom window title.
        
        Args:
            title: Custom title string
            
        Returns:
            Tuple of (success, message)
        """
        settings = self.storage.get_settings()
        settings.custom_title = title.strip() if title else None
        self.storage.save_settings()
        return True, "Custom title updated successfully"
    
    def set_video_path(self, path: str) -> Tuple[bool, str]:
        """
        Set custom video tutorial path.
        
        Args:
            path: Path to video file
            
        Returns:
            Tuple of (success, message)
        """
        import os
        if path and not os.path.exists(path):
            return False, "Video file not found"
        
        settings = self.storage.get_settings()
        settings.video_path = path
        self.storage.save_settings()
        return True, "Video tutorial path updated successfully"
    
    # ==========================================================================
    # SECTION: INDIVIDUAL MANAGEMENT
    # ==========================================================================
    
    def add_individual(self, name: str, age: Optional[int] = None, level: Optional[str] = None) -> Tuple[bool, str, Optional[IndividualParticipant]]:
        """
        Add a new individual participant to the system.
        
        This method creates a new individual participant with a unique ID
        and adds them to the storage. It validates all input parameters
        before creating the participant.
        
        Args:
            name: Participant's full name (required)
            age: Optional age in years
            level: Optional skill/education level (e.g., "Beginner", "Advanced")
            
        Returns:
            Tuple of (success, message, individual)
            - success: True if added successfully, False otherwise
            - message: Descriptive message about the operation
            - individual: The created IndividualParticipant object if successful
        
        Example:
            >>> success, msg, ind = service.add_individual("John Doe", age=25, level="Advanced")
            >>> print(success)
            True
        """
        try:
            # Validate input - name is required
            if not name.strip():
                return False, "Name cannot be empty", None
            
            # Generate unique ID for the participant
            participant_id = self.storage.generate_individual_id()
            
            # Create participant object with validated data
            individual = IndividualParticipant(
                participant_id=participant_id,
                name=name.strip(),
                age=age,
                level=level
            )
            
            # Add to storage and return result
            if self.storage.add_individual(individual):
                return True, f"Individual added successfully (ID: {participant_id})", individual
            else:
                return False, "Failed to add individual", None
                
        except ValueError as e:
            # Handle validation errors from model
            return False, str(e), None
        except Exception as e:
            # Handle unexpected errors
            return False, f"Unexpected error: {str(e)}", None
    
    def update_individual(self, participant_id: str, name: str = None, age: Optional[int] = None, level: Optional[str] = None) -> Tuple[bool, str]:
        """
        Update an existing individual participant's information.
        
        Args:
            participant_id: ID of participant to update
            name: New name (optional)
            age: New age (optional)
            level: New level (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing individual
        individual = self.storage.get_individual(participant_id)
        if not individual:
            return False, "Individual not found"
        
        try:
            # Update provided fields
            if name:
                individual.name = name.strip()
            if age is not None:
                individual.age = age
            if level is not None:
                individual.level = level
            
            # Save changes
            if self.storage.update_individual(individual):
                return True, "Data updated successfully"
            else:
                return False, "Failed to update data"
                
        except ValueError as e:
            return False, str(e)
    
    def delete_individual(self, participant_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """
        Delete an individual participant from the system.
        
        Args:
            participant_id: ID of participant to delete
            confirm: If True, also delete related registrations and results
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing individual
        individual = self.storage.get_individual(participant_id)
        if not individual:
            return False, "Individual not found"
        
        # Check for existing results
        results = self.storage.get_results_by_participant(participant_id)
        if results and not confirm:
            return False, "Cannot delete participant with saved results. Use confirm=True to force delete."
        
        # Delete related registrations and results if confirmed
        if confirm:
            for reg in self.storage.get_registrations_by_participant(participant_id):
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(participant_id, result.event_id)
        
        # Perform deletion
        if self.storage.delete_individual(participant_id):
            return True, "Participant deleted successfully"
        return False, "Failed to delete participant"
    
    def get_all_individuals(self) -> List[IndividualParticipant]:
        """
        Get all individual participants.
        
        Returns:
            List of all IndividualParticipant objects
        """
        return self.storage.get_all_individuals()
    
    def search_individual(self, name: str) -> List[IndividualParticipant]:
        """
        Search for individual participants by name.
        
        Args:
            name: Name to search for (partial match)
            
        Returns:
            List of matching IndividualParticipant objects
        """
        return self.storage.search_individual(name)
    
    def get_individual_by_name(self, name: str) -> Optional[IndividualParticipant]:
        """
        Get individual participant by exact name.
        
        Args:
            name: Exact name to search for
            
        Returns:
            IndividualParticipant if found, None otherwise
        """
        return self.storage.get_individual_by_name(name)
    
    # ==========================================================================
    # SECTION: TEAM MANAGEMENT
    # ==========================================================================
    
    def add_team(self, name: str, member_names: List[str]) -> Tuple[bool, str, Optional[Team]]:
        """
        Add a new team to the system.
        
        This method creates a new team with the specified name and members.
        It validates that the team has the required minimum of 5 members
        and maximum of 10 members.
        
        Args:
            name: Team name (required, must be unique)
            member_names: List of member names (5-10 required)
            
        Returns:
            Tuple of (success, message, team)
        
        Example:
            >>> success, msg, team = service.add_team("Champions", ["Alice", "Bob", "Charlie", "David", "Eve"])
            >>> print(success)
            True
        """
        try:
            # Validate team name
            if not name.strip():
                return False, "Team name cannot be empty", None
            
            # Validate member count
            if len(member_names) < 5:
                return False, "Team must have at least 5 members", None
            
            if len(member_names) > 10:
                return False, "Team cannot have more than 10 members", None
            
            # Check for duplicate team name
            existing_teams = self.storage.get_all_teams()
            for team in existing_teams:
                if team.name.lower() == name.strip().lower():
                    return False, "A team with this name already exists", None
            
            # Remove duplicate member names (case-insensitive)
            unique_members = []
            seen_names = set()
            for member_name in member_names:
                clean_name = member_name.strip()
                if clean_name.lower() not in seen_names:
                    unique_members.append(clean_name)
                    seen_names.add(clean_name.lower())
            
            # Re-validate after removing duplicates
            if len(unique_members) < 5:
                return False, "Team must have at least 5 unique members (duplicates removed)", None
            
            # Generate unique team ID
            team_id = self.storage.generate_team_id()
            
            # Create team members
            members = [TeamMember(name=name.strip()) for name in unique_members]
            
            # Create team object
            team = Team(
                team_id=team_id,
                name=name.strip(),
                members=members
            )
            
            # Add to storage
            if self.storage.add_team(team):
                return True, f"Team added successfully (ID: {team_id})", team
            else:
                return False, "Failed to add team", None
                
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def update_team_name(self, team_id: str, new_name: str) -> Tuple[bool, str]:
        """
        Update a team's name.
        
        Args:
            team_id: ID of team to update
            new_name: New team name
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing team
        team = self.storage.get_team(team_id)
        if not team:
            return False, "Team not found"
        
        # Check for duplicate name
        if new_name.strip():
            existing = self.storage.get_team_by_name(new_name)
            if existing and existing.team_id != team_id:
                return False, "A team with this name already exists"
        
        try:
            team.name = new_name.strip()
            if self.storage.update_team(team):
                return True, "Team name updated successfully"
            return False, "Failed to update team"
        except ValueError as e:
            return False, str(e)
    
    def update_team(self, team_id: str, name: str = None, add_members: List[str] = None, remove_members: List[str] = None) -> Tuple[bool, str]:
        """
        Update team data including name and members.
        
        Args:
            team_id: ID of team to update
            name: New team name (optional)
            add_members: List of member names to add (optional)
            remove_members: List of member names to remove (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing team
        team = self.storage.get_team(team_id)
        if not team:
            return False, "Team not found"
        
        try:
            # Update name if provided
            if name:
                # Check for duplicate
                existing = self.storage.get_team_by_name(name)
                if existing and existing.team_id != team_id:
                    return False, "A team with this name already exists"
                team.name = name.strip()
            
            # Add members if provided
            if add_members:
                for member_name in add_members:
                    if len(team.members) < 10:
                        team.add_member(TeamMember(name=member_name.strip()))
            
            # Remove members if provided
            if remove_members:
                for member_name in remove_members:
                    team.remove_member(member_name)
                
                # Ensure minimum members
                if len(team.members) < 5:
                    return False, "Cannot reduce team members below 5"
            
            # Save changes
            if self.storage.update_team(team):
                return True, "Team updated successfully"
            return False, "Failed to update team"
                
        except ValueError as e:
            return False, str(e)
    
    def delete_team(self, team_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """
        Delete a team from the system.
        
        Args:
            team_id: ID of team to delete
            confirm: If True, also delete related data
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing team
        team = self.storage.get_team(team_id)
        if not team:
            return False, "Team not found"
        
        # Check for existing results
        results = self.storage.get_results_by_participant(team_id)
        if results and not confirm:
            return False, "Cannot delete team with saved results. Use confirm=True to force delete."
        
        # Delete related data if confirmed
        if confirm:
            for reg in self.storage.get_registrations_by_participant(team_id):
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(team_id, result.event_id)
        
        # Perform deletion
        if self.storage.delete_team(team_id):
            return True, "Team deleted successfully"
        return False, "Failed to delete team"
    
    def get_all_teams(self) -> List[Team]:
        """
        Get all teams.
        
        Returns:
            List of all Team objects
        """
        return self.storage.get_all_teams()
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """
        Get team by exact name match.
        
        Args:
            name: Team name to search for
            
        Returns:
            Team if found, None otherwise
        """
        return self.storage.get_team_by_name(name)
    
    def get_team_details(self, team_id: str) -> Optional[Team]:
        """
        Get team details by ID.
        
        Args:
            team_id: Team ID to retrieve
            
        Returns:
            Team object if found, None otherwise
        """
        return self.storage.get_team(team_id)
    
    def search_team(self, name: str) -> List[Team]:
        """
        Search teams by name.
        
        Args:
            name: Name to search for (partial match)
            
        Returns:
            List of matching Team objects
        """
        return self.storage.search_team(name)
    
    # ==========================================================================
    # SECTION: EVENT MANAGEMENT
    # ==========================================================================
    
    def add_event(self, name: str, event_type: EventType, category: EventCategory, 
                  max_participants: int = 100, single_event_only: bool = False) -> Tuple[bool, str, Optional[Event]]:
        """
        Add a new event to the system.
        
        This method creates a new competition event with the specified parameters.
        Events can be either individual or group type, and either sports or academic category.
        
        Args:
            name: Event name (required, must be unique)
            event_type: INDIVIDUAL or GROUP
            category: SPORTS or ACADEMIC
            max_participants: Maximum number of participants (default: 100)
            single_event_only: If True, participants can only join this event
            
        Returns:
            Tuple of (success, message, event)
        
        Example:
            >>> success, msg, event = service.add_event(
            ...     "100m Sprint",
            ...     EventType.INDIVIDUAL,
            ...     EventCategory.SPORTS,
            ...     max_participants=20
            ... )
            >>> print(success)
            True
        """
        try:
            # Validate event name
            if not name.strip():
                return False, "Event name cannot be empty", None
            
            # Validate max participants
            if max_participants < 1:
                return False, "Max participants must be at least 1", None
            
            # Generate unique event ID
            event_id = self.storage.generate_event_id()
            
            # Create event object
            event = Event(
                event_id=event_id,
                name=name.strip(),
                event_type=event_type,
                category=category,
                max_participants=max_participants,
                single_event_only=single_event_only,
                status=EventStatus.OPEN
            )
            
            # Add to storage
            if self.storage.add_event(event):
                return True, f"Event added successfully (ID: {event_id})", event
            else:
                return False, "Failed to add event", None
                
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def update_event(self, event_id: str, name: str = None, max_participants: int = None, 
                    single_event_only: bool = None, status: EventStatus = None) -> Tuple[bool, str]:
        """
        Update event information.
        
        Args:
            event_id: ID of event to update
            name: New event name (optional)
            max_participants: New max participants (optional)
            single_event_only: New single event setting (optional)
            status: New status (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing event
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        try:
            # Update provided fields
            if name:
                event.name = name.strip()
            if max_participants is not None:
                event.max_participants = max_participants
            if single_event_only is not None:
                event.single_event_only = single_event_only
            if status is not None:
                event.status = status
            
            # Save changes
            if self.storage.update_event(event):
                return True, "Event updated successfully"
            return False, "Failed to update event"
                
        except ValueError as e:
            return False, str(e)
    
    def update_event_name(self, event_id: str, new_name: str) -> Tuple[bool, str]:
        """
        Update an event's name.
        
        Args:
            event_id: ID of event to update
            new_name: New event name
            
        Returns:
            Tuple of (success, message)
        """
        return self.update_event(event_id, name=new_name)
    
    def delete_event(self, event_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """
        Delete an event from the system.
        
        Args:
            event_id: ID of event to delete
            confirm: If True, also delete related registrations and results
            
        Returns:
            Tuple of (success, message)
        """
        # Get existing event
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check for registrations or results
        registrations = self.storage.get_registrations_by_event(event_id)
        results = self.storage.get_results_by_event(event_id)
        
        if (registrations or results) and not confirm:
            return False, "Cannot delete event with registrations or results. Use confirm=True to force delete."
        
        # Delete related data if confirmed
        if confirm:
            for reg in registrations:
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(event_id, result.participant_id)
        
        # Perform deletion
        if self.storage.delete_event(event_id):
            return True, "Event deleted successfully"
        return False, "Failed to delete event"
    
    def get_all_events(self) -> List[Event]:
        """
        Get all events.
        
        Returns:
            List of all Event objects
        """
        return self.storage.get_all_events()
    
    def get_open_events(self) -> List[Event]:
        """
        Get all events with OPEN status.
        
        Returns:
            List of open Event objects
        """
        return self.storage.get_open_events()
    
    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """
        Get events filtered by type.
        
        Args:
            event_type: EventType to filter by
            
        Returns:
            List of matching Event objects
        """
        return self.storage.get_events_by_type(event_type)
    
    # ==========================================================================
    # SECTION: REGISTRATION
    # ==========================================================================
    
    def register_participant(self, participant_id: str, participant_type: ParticipantType, event_id: str) -> Tuple[bool, str]:
        """
        Register a participant in an event.
        
        This method handles the registration process with comprehensive validation:
        - Event must exist and be open
        - Participant type must match event type
        - No duplicate registrations allowed
        - Event capacity checks
        - Participant event limit checks
        
        Args:
            participant_id: ID of participant to register
            participant_type: Type of participant (INDIVIDUAL or TEAM)
            event_id: ID of event to register for
            
        Returns:
            Tuple of (success, message)
        
        Example:
            >>> success, msg = service.register_participant("IND0001", ParticipantType.INDIVIDUAL, "EVENT0001")
            >>> print(msg)
            Registration successful
        """
        # Check event exists
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check event is open
        if event.status != EventStatus.OPEN:
            return False, "Event is closed and not accepting registrations"
        
        # Validate participant type matches event type
        if event.event_type == EventType.INDIVIDUAL and participant_type == ParticipantType.TEAM:
            return False, "Cannot register a team in an individual event"
        
        if event.event_type == EventType.GROUP and participant_type == ParticipantType.INDIVIDUAL:
            return False, "Cannot register an individual in a group event"
        
        # Check for duplicate registration
        if self.storage.is_participant_registered_in_event(participant_id, event_id):
            return False, "Participant is already registered in this event"
        
        # Check single event only constraint
        if event.single_event_only:
            event_count = self.storage.get_participant_event_count(participant_id)
            if event_count > 0:
                return False, "This event allows participation in only one event"
        
        # Check max participants
        current_registrations = len(self.storage.get_registrations_by_event(event_id))
        if event.is_full(current_registrations):
            return False, "Event is full - maximum participants reached"
        
        # Check max events per participant
        if not event.single_event_only:
            event_count = self.storage.get_participant_event_count(participant_id)
            if event_count >= self.max_events_per_participant:
                return False, f"Participant has reached maximum events limit ({self.max_events_per_participant})"
        
        # Create registration
        registration_id = self.storage.generate_registration_id()
        registration = Registration(
            registration_id=registration_id,
            participant_id=participant_id,
            participant_type=participant_type,
            event_id=event_id,
            status=RegistrationStatus.CONFIRMED
        )
        
        # Add to storage
        if self.storage.add_registration(registration):
            return True, "Registration successful"
        return False, "Registration failed"
    
    def cancel_registration(self, participant_id: str, event_id: str) -> Tuple[bool, str]:
        """
        Cancel a participant's registration.
        
        Args:
            participant_id: ID of participant
            event_id: ID of event
            
        Returns:
            Tuple of (success, message)
        """
        # Find registration
        registrations = self.storage.get_registrations_by_event(event_id)
        for reg in registrations:
            if reg.participant_id == participant_id:
                # Update status to cancelled
                reg.status = RegistrationStatus.CANCELLED
                if self.storage.update_registration(reg):
                    return True, "Registration cancelled successfully"
                return False, "Failed to cancel registration"
        return False, "Registration not found"
    
    def get_event_registrations(self, event_id: str) -> List[Registration]:
        """
        Get all registrations for an event.
        
        Args:
            event_id: Event ID
            
        Returns:
            List of Registration objects
        """
        return self.storage.get_registrations_by_event(event_id)
    
    def get_participant_registrations(self, participant_id: str) -> List[Registration]:
        """
        Get all registrations for a participant.
        
        Args:
            participant_id: Participant ID
            
        Returns:
            List of Registration objects
        """
        return self.storage.get_registrations_by_participant(participant_id)
    
    # ==========================================================================
    # SECTION: RESULTS
    # ==========================================================================
    
    def enter_result(self, event_id: str, participant_id: str, participant_type: ParticipantType, 
                    rank: int, points: int = None) -> Tuple[bool, str]:
        """
        Enter a result for a participant in an event.
        
        This method records the competition result and automatically calculates
        points based on the rank if not explicitly provided. It also updates the
        participant's total points.
        
        Args:
            event_id: Event ID
            participant_id: Participant ID
            participant_type: Type of participant
            rank: Final rank/position (1 = first place)
            points: Optional points (auto-calculated if not provided)
            
        Returns:
            Tuple of (success, message)
        
        Example:
            >>> success, msg = service.enter_result(
            ...     "EVENT0001", "IND0001", ParticipantType.INDIVIDUAL, 1
            ... )
            >>> print(msg)
            Result entered successfully (Rank 1 - 10 points)
        """
        # Check event exists
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check participant is registered
        if not self.storage.is_participant_registered_in_event(participant_id, event_id):
            return False, "Participant not registered in this event"
        
        # Validate rank
        if rank < 1:
            return False, "Rank must be 1 or higher"
        
        # Check for duplicate rank
        existing_results = self.storage.get_results_by_event(event_id)
        for result in existing_results:
            if result.rank == rank:
                return False, f"Rank {rank} is already assigned to another participant"
        
        # Calculate points if not provided
        if points is None:
            points = PointsSystem.get_points(rank)
        
        # Validate points
        if points < 0:
            return False, "Points cannot be negative"
        
        # Create result object
        result = Result(
            event_id=event_id,
            participant_id=participant_id,
            participant_type=participant_type,
            rank=rank,
            points=points
        )
        
        # Add result to storage
        if self.storage.add_result(result):
            # Update participant's total points and event count
            self._update_participant_points(participant_id, participant_type)
            return True, f"Result entered successfully (Rank {rank} - {points} points)"
        return False, "Failed to enter result"
    
    def update_result(self, event_id: str, participant_id: str, rank: int, points: int = None) -> Tuple[bool, str]:
        """
        Update an existing result.
        
        Args:
            event_id: Event ID
            participant_id: Participant ID
            rank: New rank
            points: Optional new points
            
        Returns:
            Tuple of (success, message)
        """
        # Delete old result
        if not self.storage.delete_result(event_id, participant_id):
            return False, "Result not found"
        
        # Get participant type
        registrations = self.storage.get_registrations_by_event(event_id)
        participant_type = None
        for reg in registrations:
            if reg.participant_id == participant_id:
                participant_type = reg.participant_type
                break
        
        if not participant_type:
            return False, "Participant not registered in this event"
        
        # Add new result
        return self.enter_result(event_id, participant_id, participant_type, rank, points)
    
    def _update_participant_points(self, participant_id: str, participant_type: ParticipantType):
        """
        Update participant's total points and event count.
        
        This internal method recalculates the total points and events count
        for a participant based on all their results.
        
        Args:
            participant_id: ID of participant
            participant_type: Type of participant
        """
        # Get all results for participant
        results = self.storage.get_results_by_participant(participant_id)
        
        # Calculate totals
        total_points = sum(r.points for r in results)
        events_count = len(set(r.event_id for r in results))
        
        # Update based on participant type
        if participant_type == ParticipantType.INDIVIDUAL:
            individual = self.storage.get_individual(participant_id)
            if individual:
                individual.total_points = total_points
                individual.events_count = events_count
                self.storage.update_individual(individual)
        else:
            team = self.storage.get_team(participant_id)
            if team:
                team.total_points = total_points
                team.events_count = events_count
                self.storage.update_team(team)
    
    def get_event_results(self, event_id: str) -> List[Result]:
        """
        Get all results for an event, sorted by rank.
        
        Args:
            event_id: Event ID
            
        Returns:
            List of Result objects sorted by rank
        """
        return sorted(self.storage.get_results_by_event(event_id), key=lambda r: r.rank)
    
    # ==========================================================================
    # SECTION: RANKINGS
    # ==========================================================================
    
    def calculate_rankings(self) -> Tuple[List[Ranking], List[Ranking]]:
        """
        Calculate final rankings for all participants.
        
        This method computes rankings for both individuals and teams based on
        their total points across all events. Rankings are sorted by points
        in descending order (highest points = rank 1).
        
        Returns:
            Tuple of (individual_rankings, team_rankings)
            - individual_rankings: List of Ranking objects for individuals
            - team_rankings: List of Ranking objects for teams
        
        Example:
            >>> ind_rankings, team_rankings = service.calculate_rankings()
            >>> print(f"Top individual: {ind_rankings[0].participant_name}")
            Top individual: John Doe
        """
        # =========================================================================
        # Calculate individual rankings
        # =========================================================================
        individuals = self.storage.get_all_individuals()
        individual_rankings = []
        
        for ind in individuals:
            # Only include participants who have events
            if ind.events_count > 0:
                ranking = Ranking(
                    rank=0,  # Will be assigned after sorting
                    participant_id=ind.participant_id,
                    participant_name=ind.name,
                    participant_type=ParticipantType.INDIVIDUAL,
                    total_points=ind.total_points,
                    events_participated=ind.events_count
                )
                individual_rankings.append(ranking)
        
        # =========================================================================
        # Calculate team rankings
        # =========================================================================
        teams = self.storage.get_all_teams()
        team_rankings = []
        
        for team in teams:
            # Only include teams that have events
            if team.events_count > 0:
                ranking = Ranking(
                    rank=0,  # Will be assigned after sorting
                    participant_id=team.team_id,
                    participant_name=team.name,
                    participant_type=ParticipantType.TEAM,
                    total_points=team.total_points,
                    events_participated=team.events_count
                )
                team_rankings.append(ranking)
        
        # Sort by points (descending)
        individual_rankings.sort(key=lambda r: r.total_points, reverse=True)
        team_rankings.sort(key=lambda r: r.total_points, reverse=True)
        
        # Assign ranks
        for i, ranking in enumerate(individual_rankings, 1):
            ranking.rank = i
        
        for i, ranking in enumerate(team_rankings, 1):
            ranking.rank = i
        
        return individual_rankings, team_rankings
    
    def get_winner(self) -> Tuple[Optional[Ranking], Optional[Ranking]]:
        """
        Get the winners (top-ranked participants).
        
        Returns:
            Tuple of (individual_winner, team_winner)
            - individual_winner: Top Individual Ranking or None
            - team_winner: Top Team Ranking or None
        """
        # Calculate rankings
        individual_rankings, team_rankings = self.calculate_rankings()
        
        # Get winners
        individual_winner = individual_rankings[0] if individual_rankings else None
        team_winner = team_rankings[0] if team_rankings else None
        
        return individual_winner, team_winner
    
    # ==========================================================================
    # SECTION: REPORTS
    # ==========================================================================
    
    def generate_event_report(self, event_id: str) -> Dict:
        """
        Generate a detailed report for a specific event.
        
        Args:
            event_id: Event ID
            
        Returns:
            Dictionary containing event details, registrations, and results
        """
        # Get event
        event = self.storage.get_event(event_id)
        if not event:
            return {}
        
        # Get related data
        registrations = self.storage.get_registrations_by_event(event_id)
        results = self.storage.get_results_by_event(event_id)
        
        return {
            "event": event,
            "total_registrations": len(registrations),
            "results": sorted(results, key=lambda r: r.rank),
            "status": "Completed" if event.status == EventStatus.COMPLETED else "Open"
        }
    
    def generate_full_report(self) -> Dict:
        """
        Generate a comprehensive tournament report.
        
        Returns:
            Dictionary containing statistics, rankings, and winners
        """
        # Get statistics
        stats = self.storage.get_statistics()
        
        # Calculate rankings
        individual_rankings, team_rankings = self.calculate_rankings()
        
        return {
            "statistics": stats,
            "individual_rankings": individual_rankings,
            "team_rankings": team_rankings,
            "winner_individual": individual_rankings[0] if individual_rankings else None,
            "winner_team": team_rankings[0] if team_rankings else None
        }
    
    def get_uncompleted_events(self) -> List[Event]:
        """
        Get all events that are not completed.
        
        Returns:
            List of open Event objects
        """
        return [e for e in self.storage.get_all_events() if e.status != EventStatus.COMPLETED]
    
    def get_unregistered_participants(self) -> List[Dict]:
        """
        Get participants not registered in any event.
        
        Returns:
            List of dictionaries with participant information
        """
        unregistered = []
        
        # Check individuals
        for ind in self.storage.get_all_individuals():
            if self.storage.get_participant_event_count(ind.participant_id) == 0:
                unregistered.append({
                    "type": "Individual", 
                    "id": ind.participant_id, 
                    "name": ind.name
                })
        
        # Check teams
        for team in self.storage.get_all_teams():
            if self.storage.get_participant_event_count(team.team_id) == 0:
                unregistered.append({
                    "type": "Team", 
                    "id": team.team_id, 
                    "name": team.name
                })
        
        return unregistered


# ==============================================================================
# END OF MODULE
# ==============================================================================

