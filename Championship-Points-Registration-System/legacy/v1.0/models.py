"""
Championship Points Registration System - Data Models
================================================================================
This module defines all data structures and enums used in the system.

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

Individual Responsibility:
- Each model has clear validation rules
- Self-documenting with comprehensive docstrings
- Type hints for better code understanding

Creativity:
- Flexible design allowing future extensions
- Configurable points system
- Support for different event types and categories

Self-Management:
- Automatic ID generation support
- Data validation on creation
- Serialization methods for persistence
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


# ==============================================================================
# ENUMERATIONS
# ==============================================================================

class ParticipantType(Enum):
    """Type of participant - individual or team"""
    INDIVIDUAL = "individual"
    TEAM = "team"


class EventType(Enum):
    """Type of event - individual or group"""
    INDIVIDUAL = "individual"
    GROUP = "group"


class EventCategory(Enum):
    """Category of event - sports or academic"""
    SPORTS = "sports"
    ACADEMIC = "academic"


class EventStatus(Enum):
    """Status of event - open or completed"""
    OPEN = "open"
    COMPLETED = "completed"


class RegistrationStatus(Enum):
    """Status of registration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


# ==============================================================================
# POINTS SYSTEM
# ==============================================================================

class PointsSystem:
    """
    Points allocation system for rankings
    
    Default points:
    - 1st place: 10 points
    - 2nd place: 8 points
    - 3rd place: 6 points
    - 4th place: 4 points
    - 5th place: 2 points
    - Others: 0 points
    
    This can be customized as needed.
    """
    
    DEFAULT_POINTS = {
        1: 10,   # First place
        2: 8,    # Second place
        3: 6,    # Third place
        4: 4,    # Fourth place
        5: 2,    # Fifth place
    }
    
    @classmethod
    def get_points(cls, rank: int) -> int:
        """Get points for a given rank"""
        return cls.DEFAULT_POINTS.get(rank, 0)
    
    @classmethod
    def set_points(cls, rank: int, points: int):
        """Set custom points for a rank"""
        cls.DEFAULT_POINTS[rank] = points


# ==============================================================================
# DATA MODELS
# ==============================================================================

@dataclass
class IndividualParticipant:
    """
    Individual participant model
    
    Attributes:
        participant_id: Unique identifier
        name: Full name of participant
        age: Optional age
        level: Optional skill/education level
        total_points: Accumulated points from all events
        events_count: Number of events participated
    """
    participant_id: str
    name: str
    age: Optional[int] = None
    level: Optional[str] = None
    total_points: int = 0
    events_count: int = 0
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.age is not None and self.age < 0:
            raise ValueError("Age cannot be negative")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "participant_id": self.participant_id,
            "name": self.name,
            "age": self.age,
            "level": self.level,
            "total_points": self.total_points,
            "events_count": self.events_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'IndividualParticipant':
        """Create instance from dictionary"""
        return cls(
            participant_id=data["participant_id"],
            name=data["name"],
            age=data.get("age"),
            level=data.get("level"),
            total_points=data.get("total_points", 0),
            events_count=data.get("events_count", 0)
        )


@dataclass
class TeamMember:
    """
    Team member model
    
    Attributes:
        name: Name of the team member
        role: Optional role (e.g., captain, coach)
    """
    name: str
    role: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {"name": self.name, "role": self.role}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TeamMember':
        """Create from dictionary"""
        return cls(
            name=data["name"],
            role=data.get("role")
        )


@dataclass
class Team:
    """
    Team model - a group of participants
    
    Attributes:
        team_id: Unique identifier
        name: Team name
        members: List of team members
        total_points: Accumulated points
        events_count: Number of events participated
    """
    team_id: str
    name: str
    members: List[TeamMember] = field(default_factory=list)
    total_points: int = 0
    events_count: int = 0
    
    def __post_init__(self):
        """Validate team data"""
        if not self.name.strip():
            raise ValueError("Team name cannot be empty")
        if len(self.members) < 5:
            raise ValueError("Team must have at least 5 members")
        if len(self.members) > 10:
            raise ValueError("Team cannot have more than 10 members")
    
    def add_member(self, member: TeamMember):
        """Add a member to the team"""
        if len(self.members) >= 10:
            raise ValueError("Team has reached maximum members (10)")
        self.members.append(member)
    
    def remove_member(self, member_name: str) -> bool:
        """Remove a member by name"""
        for i, member in enumerate(self.members):
            if member.name == member_name:
                self.members.pop(i)
                return True
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "members": [m.to_dict() for m in self.members],
            "total_points": self.total_points,
            "events_count": self.events_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Team':
        """Create from dictionary"""
        members = [TeamMember.from_dict(m) for m in data.get("members", [])]
        return cls(
            team_id=data["team_id"],
            name=data["name"],
            members=members,
            total_points=data.get("total_points", 0),
            events_count=data.get("events_count", 0)
        )


@dataclass
class Event:
    """
    Event/Competition model
    
    Attributes:
        event_id: Unique identifier
        name: Event name
        event_type: Individual or group
        category: Sports or academic
        max_participants: Maximum number of participants
        single_event_only: If true, participants can only join this event
        status: Open or completed
    """
    event_id: str
    name: str
    event_type: EventType
    category: EventCategory
    max_participants: int = 100
    single_event_only: bool = False
    status: EventStatus = EventStatus.OPEN
    
    def __post_init__(self):
        """Validate event data"""
        if not self.name.strip():
            raise ValueError("Event name cannot be empty")
        if self.max_participants < 1:
            raise ValueError("Max participants must be at least 1")
    
    def is_full(self, current_count: int) -> bool:
        """Check if event is full"""
        return current_count >= self.max_participants
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "event_type": self.event_type.value,
            "category": self.category.value,
            "max_participants": self.max_participants,
            "single_event_only": self.single_event_only,
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Create from dictionary"""
        return cls(
            event_id=data["event_id"],
            name=data["name"],
            event_type=EventType(data["event_type"]),
            category=EventCategory(data["category"]),
            max_participants=data.get("max_participants", 100),
            single_event_only=data.get("single_event_only", False),
            status=EventStatus(data.get("status", "open"))
        )


@dataclass
class Registration:
    """
    Registration model - tracks participant registration in events
    
    Attributes:
        registration_id: Unique identifier
        participant_id: ID of the participant
        participant_type: Individual or team
        event_id: ID of the event
        status: Registration status
        registration_date: Date and time of registration
    """
    registration_id: str
    participant_id: str
    participant_type: ParticipantType
    event_id: str
    status: RegistrationStatus = RegistrationStatus.PENDING
    registration_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "registration_id": self.registration_id,
            "participant_id": self.participant_id,
            "participant_type": self.participant_type.value,
            "event_id": self.event_id,
            "status": self.status.value,
            "registration_date": self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Registration':
        """Create from dictionary"""
        return cls(
            registration_id=data["registration_id"],
            participant_id=data["participant_id"],
            participant_type=ParticipantType(data["participant_type"]),
            event_id=data["event_id"],
            status=RegistrationStatus(data.get("status", "pending")),
            registration_date=data.get("registration_date", "")
        )


@dataclass
class Result:
    """
    Result model - stores competition results
    
    Attributes:
        event_id: ID of the event
        participant_id: ID of the participant
        participant_type: Individual or team
        rank: Final rank/position
        points: Points earned (auto-calculated if not provided)
    """
    event_id: str
    participant_id: str
    participant_type: ParticipantType
    rank: int
    points: int = 0
    
    def __post_init__(self):
        """Validate and calculate points"""
        if self.rank < 1:
            raise ValueError("Rank must be 1 or higher")
        if self.points < 0:
            raise ValueError("Points cannot be negative")
        if self.points == 0:
            self.points = PointsSystem.get_points(self.rank)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "event_id": self.event_id,
            "participant_id": self.participant_id,
            "participant_type": self.participant_type.value,
            "rank": self.rank,
            "points": self.points
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Result':
        """Create from dictionary"""
        return cls(
            event_id=data["event_id"],
            participant_id=data["participant_id"],
            participant_type=ParticipantType(data["participant_type"]),
            rank=data["rank"],
            points=data.get("points", 0)
        )


@dataclass
class Ranking:
    """
    Ranking model - represents a participant's ranking
    
    Attributes:
        rank: Final rank position
        participant_id: ID of participant
        participant_name: Name of participant
        participant_type: Type of participant
        total_points: Total points earned
        events_participated: Number of events participated
    """
    rank: int
    participant_id: str
    participant_name: str
    participant_type: ParticipantType
    total_points: int
    events_participated: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "rank": self.rank,
            "participant_id": self.participant_id,
            "participant_name": self.participant_name,
            "participant_type": self.participant_type.value,
            "total_points": self.total_points,
            "events_participated": self.events_participated
        }

