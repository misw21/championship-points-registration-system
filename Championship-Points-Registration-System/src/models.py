"""
================================================================================
Championship Points Registration System - Data Models (VERSION 2.0)
================================================================================

Module Overview:
----------------
This module defines all data structures, enumerations, and models used in the
Championship Points Registration System. It provides comprehensive data 
validation, serialization, and type safety for the entire application.

Author: Development Team
Version: 2.0
Year: 2026

Key Features:
-------------
- Individual and Team participant management
- Event creation with multiple categories
- Registration tracking system
- Results and ranking computation
- Settings management with themes and languages

Individual Responsibility:
--------------------------
- Each model has clear validation rules enforced in __post_init__
- Self-documenting with comprehensive docstrings
- Type hints for better code understanding and IDE support
- Serialization methods for JSON persistence

Creativity:
-----------
- Flexible design allowing future extensions
- Configurable points system
- Support for different event types and categories
- Multiple color themes for accessibility
- Multi-language support (English/Arabic)

Self-Management:
----------------
- Automatic ID generation support
- Data validation on creation
- Serialization methods for persistence
- Settings persistence across sessions
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


# ==============================================================================
# SECTION: ENUMERATIONS
# ==============================================================================
"""
Enumeration classes define fixed sets of constants used throughout the system.
Each enumeration provides type safety and clear semantic meaning for values.
"""

class ParticipantType(Enum):
    """
    Enumeration for participant type classification.
    
    Values:
        INDIVIDUAL: Single participant competing alone
        TEAM: Group of participants competing together
    
    Usage:
        Used to distinguish between single participants and teams in 
        registrations, results, and rankings.
    """
    INDIVIDUAL = "individual"
    TEAM = "team"


class EventType(Enum):
    """
    Enumeration for event type classification.
    
    Values:
        INDIVIDUAL: Event for individual participants only
        GROUP: Event for teams/groups only
    
    Usage:
        Determines what type of participant can register for an event.
        Individual events accept INDIVIDUAL participants only.
        Group events accept TEAM participants only.
    """
    INDIVIDUAL = "individual"
    GROUP = "group"


class EventCategory(Enum):
    """
    Enumeration for event category classification.
    
    Values:
        SPORTS: Athletic/sporting events
        ACADEMIC: Educational/academic competitions
    
    Usage:
        Used for filtering and organizing events by type.
        Helps in generating category-specific reports.
    """
    SPORTS = "sports"
    ACADEMIC = "academic"


class EventStatus(Enum):
    """
    Enumeration for event status tracking.
    
    Values:
        OPEN: Event is accepting registrations
        COMPLETED: Event has finished and results are final
    
    Usage:
        Controls registration eligibility and result entry.
        Open events allow new registrations and result updates.
    """
    OPEN = "open"
    COMPLETED = "completed"


class RegistrationStatus(Enum):
    """
    Enumeration for registration status tracking.
    
    Values:
        PENDING: Registration submitted, awaiting confirmation
        CONFIRMED: Registration approved
        CANCELLED: Registration cancelled
    
    Usage:
        Tracks the lifecycle of participant registrations.
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Language(Enum):
    """
    Enumeration for language selection.
    
    Values:
        ENGLISH: English language (default)
        ARABIC: Arabic language (RTL support)
    
    Usage:
        Controls UI text and layout direction.
    """
    ENGLISH = "english"
    ARABIC = "arabic"


class ColorTheme(Enum):
    """
    Enumeration for color theme selection.
    
    Values:
        DEFAULT: Standard color scheme
        HIGH_CONTRAST: High contrast for visibility
        PROTANOPIA: Red-green color blindness (protanopia)
        DEUTERANOPIA: Red-green color blindness (deuteranopia)
        TRITANOPIA: Blue-yellow color blindness (tritanopia)
    
    Usage:
        Provides accessibility options for users with color vision deficiencies.
        Each theme uses colors distinguishable for specific types of color blindness.
    """
    DEFAULT = "default"
    HIGH_CONTRAST = "high_contrast"
    PROTANOPIA = "protanopia"
    DEUTERANOPIA = "deuteranopia"
    TRITANOPIA = "tritanopia"


# ==============================================================================
# SECTION: POINTS SYSTEM
# ==============================================================================
"""
The PointsSystem class manages the allocation of points for competition rankings.
It provides a flexible, configurable points structure that can be customized
for different tournament types.
"""

class PointsSystem:
    """
    Points allocation system for competition rankings.
    
    This class manages the default points awarded for each rank position
    in a competition. The default system awards:
        - 1st place: 10 points
        - 2nd place: 8 points
        - 3rd place: 6 points
        - 4th place: 4 points
        - 5th place: 2 points
        - Others: 0 points
    
    The points can be customized by rank using the set_points method.
    
    Class Methods:
        get_points(rank): Returns points for a given rank
        set_points(rank, points): Sets custom points for a rank
    
    Example:
        >>> PointsSystem.get_points(1)
        10
        >>> PointsSystem.set_points(1, 15)  # First place now worth 15 points
        >>> PointsSystem.get_points(1)
        15
    """
    
    # Default points allocation by rank position
    # Key: rank (int), Value: points (int)
    DEFAULT_POINTS = {
        1: 10,   # First place - Gold medal
        2: 8,    # Second place - Silver medal
        3: 6,    # Third place - Bronze medal
        4: 4,    # Fourth place
        5: 2,    # Fifth place
    }
    
    @classmethod
    def get_points(cls, rank: int) -> int:
        """
        Get points awarded for a given rank position.
        
        Args:
            rank: The rank/position in the competition (1-based)
            
        Returns:
            The number of points awarded for that rank
            
        Note:
            Ranks not in the DEFAULT_POINTS dictionary return 0 points.
        """
        return cls.DEFAULT_POINTS.get(rank, 0)
    
    @classmethod
    def set_points(cls, rank: int, points: int):
        """
        Set custom points for a specific rank.
        
        Args:
            rank: The rank/position to customize
            points: The number of points to award
            
        Note:
            This modifies the class-level DEFAULT_POINTS dictionary,
            affecting all future point calculations.
        """
        cls.DEFAULT_POINTS[rank] = points


# ==============================================================================
# SECTION: DATA MODELS
# ==============================================================================
"""
Data model classes define the structure and behavior of core business entities.
Each model includes validation, serialization, and utility methods.
"""

@dataclass
class IndividualParticipant:
    """
    Individual participant model representing a single competitor.
    
    Attributes:
        participant_id: Unique identifier (auto-generated, format: IND0001)
        name: Full name of the participant (required)
        age: Optional age in years (for categorization)
        level: Optional skill/education level (e.g., "Beginner", "Advanced")
        total_points: Accumulated points from all completed events
        events_count: Number of events participated in
    
    Validation Rules:
        - Name cannot be empty or whitespace-only
        - Age must be non-negative if provided
        - Total points and events count start at 0
    
    Example:
        >>> participant = IndividualParticipant(
        ...     participant_id="IND0001",
        ...     name="John Doe",
        ...     age=25,
        ...     level="Advanced"
        ... )
        >>> print(participant.name)
        John Doe
    """
    
    # Required fields
    participant_id: str
    name: str
    
    # Optional fields with defaults
    age: Optional[int] = None
    level: Optional[str] = None
    total_points: int = 0
    events_count: int = 0
    
    def __post_init__(self):
        """
        Validate data after initialization.
        
        This method runs automatically after the object is created.
        It ensures data integrity by validating all fields.
        
        Raises:
            ValueError: If name is empty or age is negative
        """
        # Validate name is not empty
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        
        # Validate age is non-negative if provided
        if self.age is not None and self.age < 0:
            raise ValueError("Age cannot be negative")
    
    def to_dict(self) -> dict:
        """
        Convert participant to dictionary for serialization.
        
        Returns:
            Dictionary containing all participant attributes
            
        Note:
            Used for JSON persistence and data export
        """
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
        """
        Create participant instance from dictionary.
        
        Args:
            data: Dictionary containing participant data
            
        Returns:
            New IndividualParticipant instance
        """
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
    Team member model representing a single member within a team.
    
    Attributes:
        name: Name of the team member (required)
        role: Optional role (e.g., "Captain", "Coach", "Member")
    
    Validation Rules:
        - Name cannot be empty
    
    Example:
        >>> member = TeamMember(name="Alice", role="Captain")
        >>> print(member.name, member.role)
        Alice Captain
    """
    
    name: str
    role: Optional[str] = None
    
    def to_dict(self) -> dict:
        """
        Convert team member to dictionary.
        
        Returns:
            Dictionary with name and role
        """
        return {"name": self.name, "role": self.role}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TeamMember':
        """
        Create team member from dictionary.
        
        Args:
            data: Dictionary containing member data
            
        Returns:
            New TeamMember instance
        """
        return cls(
            name=data["name"],
            role=data.get("role")
        )


@dataclass
class Team:
    """
    Team model representing a group of participants competing together.
    
    Attributes:
        team_id: Unique identifier (auto-generated, format: TEAM0001)
        name: Team name (required, unique)
        members: List of TeamMember objects
        total_points: Accumulated points from all completed events
        events_count: Number of events participated in
    
    Validation Rules:
        - Team name cannot be empty
        - Must have at least 5 members
        - Cannot exceed 10 members
    
    Example:
        >>> team = Team(
        ...     team_id="TEAM0001",
        ...     name="The Champions",
        ...     members=[TeamMember("Alice"), TeamMember("Bob")]
        ... )
    """
    
    # Required fields
    team_id: str
    name: str
    members: List[TeamMember] = field(default_factory=list)
    
    # Computed fields
    total_points: int = 0
    events_count: int = 0
    
    def __post_init__(self):
        """
        Validate team data after initialization.
        
        Raises:
            ValueError: If team name is empty or member count is invalid
        """
        # Validate team name
        if not self.name.strip():
            raise ValueError("Team name cannot be empty")
        
        # Validate minimum members
        if len(self.members) < 5:
            raise ValueError("Team must have at least 5 members")
        
        # Validate maximum members
        if len(self.members) > 10:
            raise ValueError("Team cannot have more than 10 members")
    
    def add_member(self, member: TeamMember):
        """
        Add a new member to the team.
        
        Args:
            member: TeamMember object to add
            
        Raises:
            ValueError: If team already has 10 members
        """
        if len(self.members) >= 10:
            raise ValueError("Team has reached maximum members (10)")
        self.members.append(member)
    
    def remove_member(self, member_name: str) -> bool:
        """
        Remove a member from the team by name.
        
        Args:
            member_name: Name of the member to remove
            
        Returns:
            True if member was found and removed, False otherwise
        """
        for i, member in enumerate(self.members):
            if member.name == member_name:
                self.members.pop(i)
                return True
        return False
    
    def update_member_name(self, old_name: str, new_name: str) -> bool:
        """
        Update a team member's name.
        
        Args:
            old_name: Current name of the member
            new_name: New name for the member
            
        Returns:
            True if member was found and updated, False otherwise
        """
        for member in self.members:
            if member.name == old_name:
                member.name = new_name
                return True
        return False
    
    def to_dict(self) -> dict:
        """
        Convert team to dictionary for serialization.
        
        Returns:
            Dictionary containing all team attributes
        """
        return {
            "team_id": self.team_id,
            "name": self.name,
            "members": [m.to_dict() for m in self.members],
            "total_points": self.total_points,
            "events_count": self.events_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Team':
        """
        Create team instance from dictionary.
        
        Args:
            data: Dictionary containing team data
            
        Returns:
            New Team instance
        """
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
    Event/Competition model representing a single tournament event.
    
    Attributes:
        event_id: Unique identifier (auto-generated, format: EVENT0001)
        name: Event name (required, unique)
        event_type: INDIVIDUAL or GROUP
        category: SPORTS or ACADEMIC
        max_participants: Maximum number of participants allowed
        single_event_only: If True, participants can only join this event
        status: OPEN or COMPLETED
    
    Validation Rules:
        - Event name cannot be empty
        - Max participants must be at least 1
    
    Example:
        >>> event = Event(
        ...     event_id="EVENT0001",
        ...     name="100m Sprint",
        ...     event_type=EventType.INDIVIDUAL,
        ...     category=EventCategory.SPORTS,
        ...     max_participants=20
        ... )
    """
    
    # Required fields
    event_id: str
    name: str
    event_type: EventType
    category: EventCategory
    
    # Optional fields with defaults
    max_participants: int = 100
    single_event_only: bool = False
    status: EventStatus = EventStatus.OPEN
    
    def __post_init__(self):
        """
        Validate event data after initialization.
        
        Raises:
            ValueError: If event name is empty or max participants is invalid
        """
        # Validate event name
        if not self.name.strip():
            raise ValueError("Event name cannot be empty")
        
        # Validate max participants
        if self.max_participants < 1:
            raise ValueError("Max participants must be at least 1")
    
    def is_full(self, current_count: int) -> bool:
        """
        Check if event has reached maximum capacity.
        
        Args:
            current_count: Current number of registered participants
            
        Returns:
            True if event is full, False otherwise
        """
        return current_count >= self.max_participants
    
    def to_dict(self) -> dict:
        """
        Convert event to dictionary for serialization.
        
        Returns:
            Dictionary containing all event attributes
        """
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
        """
        Create event instance from dictionary.
        
        Args:
            data: Dictionary containing event data
            
        Returns:
            New Event instance
        """
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
    Registration model tracking participant enrollment in events.
    
    Attributes:
        registration_id: Unique identifier (auto-generated, format: REG0001)
        participant_id: ID of the registered participant
        participant_type: INDIVIDUAL or TEAM
        event_id: ID of the event
        status: PENDING, CONFIRMED, or CANCELLED
        registration_date: Date and time of registration
    
    Example:
        >>> registration = Registration(
        ...     registration_id="REG0001",
        ...     participant_id="IND0001",
        ...     participant_type=ParticipantType.INDIVIDUAL,
        ...     event_id="EVENT0001"
        ... )
    """
    
    # Required fields
    registration_id: str
    participant_id: str
    participant_type: ParticipantType
    event_id: str
    
    # Optional fields with defaults
    status: RegistrationStatus = RegistrationStatus.PENDING
    registration_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> dict:
        """
        Convert registration to dictionary for serialization.
        
        Returns:
            Dictionary containing all registration attributes
        """
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
        """
        Create registration instance from dictionary.
        
        Args:
            data: Dictionary containing registration data
            
        Returns:
            New Registration instance
        """
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
    Result model storing competition outcome for a participant.
    
    Attributes:
        event_id: ID of the event
        participant_id: ID of the participant
        participant_type: INDIVIDUAL or TEAM
        rank: Final rank/position (1 = first place)
        points: Points earned (auto-calculated if not provided)
    
    Validation Rules:
        - Rank must be 1 or higher
        - Points cannot be negative
        - Points are auto-calculated if not provided
    
    Example:
        >>> result = Result(
        ...     event_id="EVENT0001",
        ...     participant_id="IND0001",
        ...     participant_type=ParticipantType.INDIVIDUAL,
        ...     rank=1
        ... )
        >>> print(result.points)
        10
    """
    
    # Required fields
    event_id: str
    participant_id: str
    participant_type: ParticipantType
    rank: int
    
    # Optional field with auto-calculation
    points: int = 0
    
    def __post_init__(self):
        """
        Validate result data and calculate points.
        
        This method automatically calculates points based on rank
        if points were not explicitly provided.
        
        Raises:
            ValueError: If rank is less than 1 or points are negative
        """
        # Validate rank
        if self.rank < 1:
            raise ValueError("Rank must be 1 or higher")
        
        # Validate points
        if self.points < 0:
            raise ValueError("Points cannot be negative")
        
        # Auto-calculate points if not provided
        if self.points == 0:
            self.points = PointsSystem.get_points(self.rank)
    
    def to_dict(self) -> dict:
        """
        Convert result to dictionary for serialization.
        
        Returns:
            Dictionary containing all result attributes
        """
        return {
            "event_id": self.event_id,
            "participant_id": self.participant_id,
            "participant_type": self.participant_type.value,
            "rank": self.rank,
            "points": self.points
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Result':
        """
        Create result instance from dictionary.
        
        Args:
            data: Dictionary containing result data
            
        Returns:
            New Result instance
        """
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
    Ranking model representing a participant's standing in the competition.
    
    Attributes:
        rank: Final rank position (1 = first place)
        participant_id: ID of the participant
        participant_name: Display name of the participant
        participant_type: INDIVIDUAL or TEAM
        total_points: Total points earned across all events
        events_participated: Number of events participated in
    
    Example:
        >>> ranking = Ranking(
        ...     rank=1,
        ...     participant_id="IND0001",
        ...     participant_name="John Doe",
        ...     participant_type=ParticipantType.INDIVIDUAL,
        ...     total_points=50,
        ...     events_participated=5
        ... )
    """
    
    # Required fields
    rank: int
    participant_id: str
    participant_name: str
    participant_type: ParticipantType
    total_points: int
    events_participated: int
    
    def to_dict(self) -> dict:
        """
        Convert ranking to dictionary for serialization.
        
        Returns:
            Dictionary containing all ranking attributes
        """
        return {
            "rank": self.rank,
            "participant_id": self.participant_id,
            "participant_name": self.participant_name,
            "participant_type": self.participant_type.value,
            "total_points": self.total_points,
            "events_participated": self.events_participated
        }


# ==============================================================================
# SECTION: SETTINGS MODEL
# ==============================================================================
"""
Settings model for application configuration and user preferences.
Stores user-customizable options like volume, theme, and language.
"""

class FontSize(Enum):
    """
    Enumeration for font size selection.
    
    Values:
        SMALL: Small font size (9pt)
        MEDIUM: Medium font size (11pt) - default
        LARGE: Large font size (14pt)
        EXTRA_LARGE: Extra large font size (16pt)
    
    Usage:
        Provides accessibility options for users with visual impairments.
    """
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


@dataclass
class AppSettings:
    """
    Application settings model for user preferences and configuration.
    
    This class stores all customizable settings including:
    - Audio settings (volume)
    - Visual settings (theme, colors, font size)
    - Language preferences
    - UI preferences
    - Custom window title
    
    Attributes:
        volume: Sound volume level (0.0 to 1.0)
        theme: Color theme selection
        language: UI language (English/Arabic)
        logo_path: Custom logo image path (optional)
        sound_enabled: Enable/disable sound effects
        video_guide_watched: Track if user has watched tutorial
        font_size: UI font size for accessibility
        custom_title: Custom window title (optional)
        video_path: Custom video tutorial path (optional)
    
    Default Values:
        - Volume: 0.5 (50%)
        - Theme: DEFAULT
        - Language: ENGLISH
        - Sound Enabled: True
        - Font Size: MEDIUM
    
    Example:
        >>> settings = AppSettings(
        ...     volume=0.8,
        ...     theme=ColorTheme.HIGH_CONTRAST,
        ...     language=Language.ARABIC,
        ...     font_size=FontSize.LARGE,
        ...     custom_title="My Tournament"
        ... )
    """
    
    # Audio settings
    volume: float = 0.5
    sound_enabled: bool = True
    
    # Visual settings
    theme: ColorTheme = ColorTheme.DEFAULT
    font_size: FontSize = FontSize.MEDIUM
    
    # Language settings
    language: Language = Language.ENGLISH
    
    # Customization
    logo_path: Optional[str] = None
    custom_title: Optional[str] = None
    video_path: Optional[str] = None
    
    # Progress tracking
    video_guide_watched: bool = False
    
    def __post_init__(self):
        """
        Validate settings after initialization.
        
        Raises:
            ValueError: If volume is outside valid range [0.0, 1.0]
        """
        # Validate volume range
        if not 0.0 <= self.volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
    
    def set_volume(self, volume: float):
        """
        Set the volume level.
        
        Args:
            volume: Volume level between 0.0 (mute) and 1.0 (max)
            
        Raises:
            ValueError: If volume is outside valid range
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        self.volume = volume
    
    def increase_volume(self, amount: float = 0.1):
        """
        Increase volume by specified amount.
        
        Args:
            amount: Amount to increase (default: 0.1 = 10%)
        """
        self.volume = min(1.0, self.volume + amount)
    
    def decrease_volume(self, amount: float = 0.1):
        """
        Decrease volume by specified amount.
        
        Args:
            amount: Amount to decrease (default: 0.1 = 10%)
        """
        self.volume = max(0.0, self.volume - amount)
    
    def toggle_sound(self):
        """
        Toggle sound effects on/off.
        
        Returns:
            New sound enabled state
        """
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def set_language(self, language: Language):
        """
        Set the UI language.
        
        Args:
            language: Language enumeration value
        """
        self.language = language
    
    def set_theme(self, theme: ColorTheme):
        """
        Set the color theme.
        
        Args:
            theme: ColorTheme enumeration value
        """
        self.theme = theme
    
    def to_dict(self) -> dict:
        """
        Convert settings to dictionary for serialization.
        
        Returns:
            Dictionary containing all settings
        """
        return {
            "volume": self.volume,
            "sound_enabled": self.sound_enabled,
            "theme": self.theme.value,
            "font_size": self.font_size.value,
            "language": self.language.value,
            "logo_path": self.logo_path,
            "custom_title": self.custom_title,
            "video_path": self.video_path,
            "video_guide_watched": self.video_guide_watched
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppSettings':
        """
        Create settings instance from dictionary.
        
        Args:
            data: Dictionary containing settings data
            
        Returns:
            New AppSettings instance
        """
        return cls(
            volume=data.get("volume", 0.5),
            sound_enabled=data.get("sound_enabled", True),
            theme=ColorTheme(data.get("theme", "default")),
            font_size=FontSize(data.get("font_size", "medium")),
            language=Language(data.get("language", "english")),
            logo_path=data.get("logo_path"),
            custom_title=data.get("custom_title"),
            video_path=data.get("video_path"),
            video_guide_watched=data.get("video_guide_watched", False)
        )
    
    def get_text_direction(self) -> str:
        """
        Get the text direction based on current language.
        
        Returns:
            "ltr" for English, "rtl" for Arabic
        """
        return "rtl" if self.language == Language.ARABIC else "ltr"


# ==============================================================================
# SECTION: COLOR THEMES
# ==============================================================================
"""
Color theme definitions for accessibility and visual preferences.
Each theme provides a complete color scheme for the application.
"""

class ColorThemes:
    """
    Color theme definitions for the application.
    
    This class provides color schemes for different accessibility needs:
    - DEFAULT: Standard blue theme
    - HIGH_CONTRAST: High contrast for visibility
    - PROTANOPIA: Colors safe for protanopia (red-blind)
    - DEUTERANOPIA: Colors safe for deuteranopia (green-blind)
    - TRITANOPIA: Colors safe for tritanopia (blue-blind)
    
    Each theme includes:
    - Primary colors for buttons and headers
    - Secondary colors for accents
    - Background colors
    - Text colors
    - Status colors (success, warning, error)
    """
    
    # Default theme - Blue professional
    DEFAULT = {
        "primary": "#3498db",       # Blue
        "secondary": "#2c3e50",      # Dark blue-gray
        "success": "#27ae60",        # Green
        "warning": "#f39c12",        # Orange
        "danger": "#e74c3c",         # Red
        "background": "#ecf0f1",    # Light gray
        "text": "#2c3e50",          # Dark text
        "text_light": "#ffffff",     # White text
        "accent": "#9b59b6",        # Purple
    }
    
    # High contrast theme
    HIGH_CONTRAST = {
        "primary": "#000000",       # Black
        "secondary": "#ffffff",     # White
        "success": "#00ff00",       # Bright green
        "warning": "#ffff00",       # Yellow
        "danger": "#ff0000",        # Red
        "background": "#ffffff",    # White
        "text": "#000000",          # Black
        "text_light": "#ffffff",    # White
        "accent": "#0000ff",       # Blue
    }
    
    # Protanopia-friendly (red-blind)
    PROTANOPIA = {
        "primary": "#0077bb",       # Blue-orange (safe)
        "secondary": "#ee7733",     # Orange
        "success": "#009988",       # Teal
        "warning": "#ee7733",       # Orange
        "danger": "#cc3311",        # Dark red
        "background": "#f0f0f0",    # Light gray
        "text": "#333333",          # Dark gray
        "text_light": "#ffffff",    # White
        "accent": "#33bbee",       # Cyan
    }
    
    # Deuteranopia-friendly (green-blind)
    DEUTERANOPIA = {
        "primary": "#0077bb",       # Blue
        "secondary": "#ee7733",    # Orange
        "success": "#009988",      # Teal
        "warning": "#ee7733",      # Orange
        "danger": "#cc3311",       # Dark red
        "background": "#f0f0f0",   # Light gray
        "text": "#333333",         # Dark gray
        "text_light": "#ffffff",   # White
        "accent": "#33bbee",       # Cyan
    }
    
    # Tritanopia-friendly (blue-blind)
    TRITANOPIA = {
        "primary": "#ee77aa",      # Pink
        "secondary": "#aa55aa",    # Purple
        "success": "#ddAA33",      # Gold
        "warning": "#ddAA33",      # Gold
        "danger": "#bb5566",       # Rose
        "background": "#f5f5f5",   # Light gray
        "text": "#222222",         # Dark gray
        "text_light": "#ffffff",   # White
        "accent": "#7799cc",       # Light blue
    }
    
    @classmethod
    def get_colors(cls, theme: ColorTheme) -> dict:
        """
        Get color dictionary for a specific theme.
        
        Args:
            theme: ColorTheme enumeration value
            
        Returns:
            Dictionary of color values
        """
        theme_map = {
            ColorTheme.DEFAULT: cls.DEFAULT,
            ColorTheme.HIGH_CONTRAST: cls.HIGH_CONTRAST,
            ColorTheme.PROTANOPIA: cls.PROTANOPIA,
            ColorTheme.DEUTERANOPIA: cls.DEUTERANOPIA,
            ColorTheme.TRITANOPIA: cls.TRITANOPIA,
        }
        return theme_map.get(theme, cls.DEFAULT)


# ==============================================================================
# END OF MODULE
# ==============================================================================

