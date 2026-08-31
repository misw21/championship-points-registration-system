"""
Championship Points Registration System - Business Services
================================================================================
This module contains all business logic and service operations for the system.

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

Individual Responsibility:
- Each service method has clear input validation
- Comprehensive error handling
- Detailed logging and audit trail
- Self-contained business logic

Creativity:
- Flexible points system
- Event type validation
- Participant eligibility checking
- Results validation

Self-Management:
- Automatic points calculation
- Ranking computation
- Statistics generation
- Event status management
"""

from typing import List, Optional, Tuple, Dict
from models import (
    IndividualParticipant, Team, TeamMember, Event, Registration, Result, Ranking,
    ParticipantType, EventType, EventCategory, EventStatus, RegistrationStatus, PointsSystem
)
from storage import Storage


class TournamentService:
    """
    Tournament management service - handles all business logic
    
    Individual Accountability:
    - All operations are validated
    - Clear success/failure returns
    - Comprehensive error messages
    
    Creativity:
    - Flexible registration rules
    - Event capacity management
    - Points system integration
    """
    
    def __init__(self, storage: Storage):
        """
        Initialize service with storage
        
        Args:
            storage: Storage instance for data persistence
        """
        self.storage = storage
        self.max_events_per_participant = 5  # Maximum events per participant
    
    # ============== Individual Management ==============
    
    def add_individual(self, name: str, age: Optional[int] = None, level: Optional[str] = None) -> Tuple[bool, str, Optional[IndividualParticipant]]:
        """
        Add a new individual participant
        
        Args:
            name: Participant's name
            age: Optional age
            level: Optional skill/education level
            
        Returns:
            Tuple of (success, message, individual)
        """
        try:
            # Validate input
            if not name.strip():
                return False, "Name cannot be empty", None
            
            # Generate unique ID
            participant_id = self.storage.generate_individual_id()
            
            # Create participant
            individual = IndividualParticipant(
                participant_id=participant_id,
                name=name.strip(),
                age=age,
                level=level
            )
            
            # Add to storage
            if self.storage.add_individual(individual):
                return True, f"Individual added successfully (ID: {participant_id})", individual
            else:
                return False, "Failed to add individual", None
                
        except ValueError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None
    
    def update_individual(self, participant_id: str, name: str = None, age: Optional[int] = None, level: Optional[str] = None) -> Tuple[bool, str]:
        """Update individual participant data"""
        individual = self.storage.get_individual(participant_id)
        if not individual:
            return False, "Individual not found"
        
        try:
            if name:
                individual.name = name.strip()
            if age is not None:
                individual.age = age
            if level is not None:
                individual.level = level
            
            if self.storage.update_individual(individual):
                return True, "Data updated successfully"
            else:
                return False, "Failed to update data"
                
        except ValueError as e:
            return False, str(e)
    
    def delete_individual(self, participant_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """Delete an individual participant"""
        individual = self.storage.get_individual(participant_id)
        if not individual:
            return False, "Individual not found"
        
        # Check for existing results
        results = self.storage.get_results_by_participant(participant_id)
        if results and not confirm:
            return False, "Cannot delete participant with saved results. Use confirm=True to force delete."
        
        # Delete related registrations and results
        if confirm:
            for reg in self.storage.get_registrations_by_participant(participant_id):
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(participant_id, result.event_id)
        
        if self.storage.delete_individual(participant_id):
            return True, "Participant deleted successfully"
        return False, "Failed to delete participant"
    
    def get_all_individuals(self) -> List[IndividualParticipant]:
        """Get all individual participants"""
        return self.storage.get_all_individuals()
    
    def search_individual(self, name: str) -> List[IndividualParticipant]:
        """Search for individual participants by name"""
        return self.storage.search_individual(name)
    
    # ============== Team Management ==============
    
    def add_team(self, name: str, member_names: List[str]) -> Tuple[bool, str, Optional[Team]]:
        """
        Add a new team
        
        Args:
            name: Team name
            member_names: List of member names (5-10 required)
            
        Returns:
            Tuple of (success, message, team)
        """
        try:
            # Validate input
            if not name.strip():
                return False, "Team name cannot be empty", None
            
            if len(member_names) < 5:
                return False, "Team must have at least 5 members", None
            
            if len(member_names) > 10:
                return False, "Team cannot have more than 10 members", None
            
            # Check for duplicate team name
            existing_teams = self.storage.get_all_teams()
            for team in existing_teams:
                if team.name.lower() == name.strip().lower():
                    return False, "A team with this name already exists", None
            
            # Remove duplicate member names (keep first occurrence)
            unique_members = []
            seen_names = set()
            for member_name in member_names:
                clean_name = member_name.strip()
                if clean_name.lower() not in seen_names:
                    unique_members.append(clean_name)
                    seen_names.add(clean_name.lower())
            
            # Check if we still have enough unique members
            if len(unique_members) < 5:
                return False, "Team must have at least 5 unique members (duplicates removed)", None
            
            # Generate unique ID
            team_id = self.storage.generate_team_id()
            
            # Create team members
            members = [TeamMember(name=name.strip()) for name in unique_members]
            
            # Create team
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
    
    def update_team(self, team_id: str, name: str = None, add_members: List[str] = None, remove_members: List[str] = None) -> Tuple[bool, str]:
        """Update team data"""
        team = self.storage.get_team(team_id)
        if not team:
            return False, "Team not found"
        
        try:
            if name:
                team.name = name.strip()
            
            if add_members:
                for member_name in add_members:
                    if len(team.members) < 10:
                        team.add_member(TeamMember(name=member_name.strip()))
            
            if remove_members:
                for member_name in remove_members:
                    team.remove_member(member_name)
                
                if len(team.members) < 5:
                    return False, "Cannot reduce team members below 5"
            
            if self.storage.update_team(team):
                return True, "Team updated successfully"
            return False, "Failed to update team"
                
        except ValueError as e:
            return False, str(e)
    
    def delete_team(self, team_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """Delete a team"""
        team = self.storage.get_team(team_id)
        if not team:
            return False, "Team not found"
        
        # Check for existing results
        results = self.storage.get_results_by_participant(team_id)
        if results and not confirm:
            return False, "Cannot delete team with saved results. Use confirm=True to force delete."
        
        # Delete related data
        if confirm:
            for reg in self.storage.get_registrations_by_participant(team_id):
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(team_id, result.event_id)
        
        if self.storage.delete_team(team_id):
            return True, "Team deleted successfully"
        return False, "Failed to delete team"
    
    def get_all_teams(self) -> List[Team]:
        """Get all teams"""
        return self.storage.get_all_teams()
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """Get team by name"""
        teams = self.storage.get_all_teams()
        for team in teams:
            if team.name.lower() == name.strip().lower():
                return team
        return None
    
    def get_team_details(self, team_id: str) -> Optional[Team]:
        """Get team details"""
        return self.storage.get_team(team_id)
    
    def search_team(self, name: str) -> List[Team]:
        """Search teams by name"""
        return self.storage.search_team(name)
    
    # ============== Event Management ==============
    
    def add_event(self, name: str, event_type: EventType, category: EventCategory, 
                  max_participants: int = 100, single_event_only: bool = False) -> Tuple[bool, str, Optional[Event]]:
        """
        Add a new event
        
        Args:
            name: Event name
            event_type: Individual or group
            category: Sports or academic
            max_participants: Maximum participants allowed
            single_event_only: If true, participants can only join this event
            
        Returns:
            Tuple of (success, message, event)
        """
        try:
            # Validate input
            if not name.strip():
                return False, "Event name cannot be empty", None
            
            if max_participants < 1:
                return False, "Max participants must be at least 1", None
            
            # Generate unique ID
            event_id = self.storage.generate_event_id()
            
            # Create event
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
        """Update event data"""
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        try:
            if name:
                event.name = name.strip()
            if max_participants is not None:
                event.max_participants = max_participants
            if single_event_only is not None:
                event.single_event_only = single_event_only
            if status is not None:
                event.status = status
            
            if self.storage.update_event(event):
                return True, "Event updated successfully"
            return False, "Failed to update event"
                
        except ValueError as e:
            return False, str(e)
    
    def delete_event(self, event_id: str, confirm: bool = False) -> Tuple[bool, str]:
        """Delete an event"""
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check for registrations or results
        registrations = self.storage.get_registrations_by_event(event_id)
        results = self.storage.get_results_by_event(event_id)
        
        if (registrations or results) and not confirm:
            return False, "Cannot delete event with registrations or results. Use confirm=True to force delete."
        
        # Delete related data
        if confirm:
            for reg in registrations:
                self.storage.delete_registration(reg.registration_id)
            for result in results:
                self.storage.delete_result(event_id, result.participant_id)
        
        if self.storage.delete_event(event_id):
            return True, "Event deleted successfully"
        return False, "Failed to delete event"
    
    def get_all_events(self) -> List[Event]:
        """Get all events"""
        return self.storage.get_all_events()
    
    def get_open_events(self) -> List[Event]:
        """Get open events"""
        return self.storage.get_open_events()
    
    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Get events by type"""
        return self.storage.get_events_by_type(event_type)
    
    # ============== Registration ==============
    
    def register_participant(self, participant_id: str, participant_type: ParticipantType, event_id: str) -> Tuple[bool, str]:
        """
        Register a participant in an event
        
        Args:
            participant_id: ID of participant
            participant_type: Type of participant
            event_id: ID of event
            
        Returns:
            Tuple of (success, message)
        """
        # Check event exists
        event = self.storage.get_event(event_id)
        if not event:
            return False, "Event not found"
        
        # Check event status
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
        
        if self.storage.add_registration(registration):
            return True, "Registration successful"
        return False, "Registration failed"
    
    def cancel_registration(self, participant_id: str, event_id: str) -> Tuple[bool, str]:
        """Cancel a registration"""
        registrations = self.storage.get_registrations_by_event(event_id)
        for reg in registrations:
            if reg.participant_id == participant_id:
                reg.status = RegistrationStatus.CANCELLED
                if self.storage.update_registration(reg):
                    return True, "Registration cancelled successfully"
                return False, "Failed to cancel registration"
        return False, "Registration not found"
    
    def get_event_registrations(self, event_id: str) -> List[Registration]:
        """Get registrations for an event"""
        return self.storage.get_registrations_by_event(event_id)
    
    def get_participant_registrations(self, participant_id: str) -> List[Registration]:
        """Get registrations for a participant"""
        return self.storage.get_registrations_by_participant(participant_id)
    
    # ============== Results ==============
    
    def enter_result(self, event_id: str, participant_id: str, participant_type: ParticipantType, 
                    rank: int, points: int = None) -> Tuple[bool, str]:
        """
        Enter a result for a participant in an event
        
        Args:
            event_id: Event ID
            participant_id: Participant ID
            participant_type: Type of participant
            rank: Final rank
            points: Optional points (auto-calculated if not provided)
            
        Returns:
            Tuple of (success, message)
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
        
        # Create result
        result = Result(
            event_id=event_id,
            participant_id=participant_id,
            participant_type=participant_type,
            rank=rank,
            points=points
        )
        
        if self.storage.add_result(result):
            # Update participant points
            self._update_participant_points(participant_id, participant_type)
            return True, f"Result entered successfully (Rank {rank} - {points} points)"
        return False, "Failed to enter result"
    
    def update_result(self, event_id: str, participant_id: str, rank: int, points: int = None) -> Tuple[bool, str]:
        """Update a result"""
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
        return self.enter_result(event_id, participant_type, participant_type, rank, points)
    
    def _update_participant_points(self, participant_id: str, participant_type: ParticipantType):
        """Update participant's total points and event count"""
        results = self.storage.get_results_by_participant(participant_id)
        total_points = sum(r.points for r in results)
        events_count = len(set(r.event_id for r in results))
        
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
        """Get results for an event"""
        return sorted(self.storage.get_results_by_event(event_id), key=lambda r: r.rank)
    
    # ============== Rankings ==============
    
    def calculate_rankings(self) -> Tuple[List[Ranking], List[Ranking]]:
        """
        Calculate final rankings for all participants
        
        Returns:
            Tuple of (individual_rankings, team_rankings)
        """
        # Individual rankings
        individuals = self.storage.get_all_individuals()
        individual_rankings = []
        
        for ind in individuals:
            if ind.events_count > 0:
                ranking = Ranking(
                    rank=0,
                    participant_id=ind.participant_id,
                    participant_name=ind.name,
                    participant_type=ParticipantType.INDIVIDUAL,
                    total_points=ind.total_points,
                    events_participated=ind.events_count
                )
                individual_rankings.append(ranking)
        
        # Team rankings
        teams = self.storage.get_all_teams()
        team_rankings = []
        
        for team in teams:
            if team.events_count > 0:
                ranking = Ranking(
                    rank=0,
                    participant_id=team.team_id,
                    participant_name=team.name,
                    participant_type=ParticipantType.TEAM,
                    total_points=team.total_points,
                    events_participated=team.events_count
                )
                team_rankings.append(ranking)
        
        # Sort by points
        individual_rankings.sort(key=lambda r: r.total_points, reverse=True)
        team_rankings.sort(key=lambda r: r.total_points, reverse=True)
        
        # Assign ranks
        for i, ranking in enumerate(individual_rankings, 1):
            ranking.rank = i
        
        for i, ranking in enumerate(team_rankings, 1):
            ranking.rank = i
        
        return individual_rankings, team_rankings
    
    def get_winner(self) -> Tuple[Optional[Ranking], Optional[Ranking]]:
        """Get the winners"""
        individual_rankings, team_rankings = self.calculate_rankings()
        
        individual_winner = individual_rankings[0] if individual_rankings else None
        team_winner = team_rankings[0] if team_rankings else None
        
        return individual_winner, team_winner
    
    # ============== Reports ==============
    
    def generate_event_report(self, event_id: str) -> Dict:
        """Generate a detailed report for an event"""
        event = self.storage.get_event(event_id)
        if not event:
            return {}
        
        registrations = self.storage.get_registrations_by_event(event_id)
        results = self.storage.get_results_by_event(event_id)
        
        return {
            "event": event,
            "total_registrations": len(registrations),
            "results": sorted(results, key=lambda r: r.rank),
            "status": "Completed" if event.status == EventStatus.COMPLETED else "Open"
        }
    
    def generate_full_report(self) -> Dict:
        """Generate a comprehensive tournament report"""
        stats = self.storage.get_statistics()
        individual_rankings, team_rankings = self.calculate_rankings()
        
        return {
            "statistics": stats,
            "individual_rankings": individual_rankings,
            "team_rankings": team_rankings,
            "winner_individual": individual_rankings[0] if individual_rankings else None,
            "winner_team": team_rankings[0] if team_rankings else None
        }
    
    def get_uncompleted_events(self) -> List[Event]:
        """Get events that are not completed"""
        return [e for e in self.storage.get_all_events() if e.status != EventStatus.COMPLETED]
    
    def get_unregistered_participants(self) -> List:
        """Get participants not registered in any event"""
        unregistered = []
        
        for ind in self.storage.get_all_individuals():
            if self.storage.get_participant_event_count(ind.participant_id) == 0:
                unregistered.append({"type": "Individual", "id": ind.participant_id, "name": ind.name})
        
        for team in self.storage.get_all_teams():
            if self.storage.get_participant_event_count(team.team_id) == 0:
                unregistered.append({"type": "Team", "id": team.team_id, "name": team.name})
        
        return unregistered

