"""
Championship Points Registration System - Console User Interface
================================================================================

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

Individual Responsibility:
- Clear user interaction handling
- Input validation and sanitization
- User-friendly error messages
- Menu navigation management

Creativity:
- Color-coded output for better UX
- Flexible input handling
- Interactive menus

Self-Management:
- Automatic screen clearing
- Data persistence handling
- Session management
"""

import os
import sys
from typing import Optional
from models import (
    IndividualParticipant, Team, Event, Result, Ranking,
    ParticipantType, EventType, EventCategory, EventStatus
)
from services import TournamentService
from storage import Storage


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def print_header(text):
        """Print formatted header"""
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    @staticmethod
    def print_subheader(text):
        """Print formatted subheader"""
        print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}")
        print("-" * 50)
    
    @staticmethod
    def print_success(text):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    
    @staticmethod
    def print_error(text):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    @staticmethod
    def print_warning(text):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    @staticmethod
    def print_info(text):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")


class TournamentUI:
    """
    Console user interface for tournament management
    
    Individual Accountability:
    - All user interactions are validated
    - Clear feedback for all operations
    - Proper error handling
    """
    
    def __init__(self):
        """Initialize the console UI"""
        self.storage = Storage()
        self.service = TournamentService(self.storage)
        self.running = True
        
        # Try to load last saved data
        self._try_load_latest_data()
    
    def _try_load_latest_data(self):
        """Try to load the most recently saved data"""
        latest_file = self.storage.get_latest_save_file()
        if latest_file:
            Colors.print_info(f"Found save file: {latest_file}")
            choice = input("Would you like to load saved data? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                if self.storage.load_from_json(latest_file):
                    Colors.print_success("Data loaded successfully")
                else:
                    Colors.print_error("Failed to load data")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self):
        """Pause for user to read output"""
        input("\nPress Enter to continue...")
    
    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation"""
        while True:
            value = input(prompt).strip()
            if not value and required:
                Colors.print_error("This field is required")
                continue
            return value if value else None
    
    def get_yes_no(self, prompt: str) -> bool:
        """Get yes/no input from user"""
        while True:
            value = input(f"{prompt} (y/n): ").strip().lower()
            if value in ['y', 'yes']:
                return True
            elif value in ['n', 'no']:
                return False
            Colors.print_error("Please enter y or n")
    
    def get_menu_choice(self, options: list) -> int:
        """Get menu choice from user"""
        while True:
            try:
                choice = int(input("\nEnter number: ").strip())
                if 1 <= choice <= len(options):
                    return choice
                Colors.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                Colors.print_error("Please enter a valid number")
    
    # ============== Main Menu ==============
    
    def main_menu(self):
        """Main menu loop"""
        while self.running:
            self.clear_screen()
            Colors.print_header("Championship Points Registration System")
            
            print("""
    ┌─────────────────────────────────────────────────────┐
    │                    MAIN MENU                         │
    ├─────────────────────────────────────────────────────┤
    │  1. 👤 Manage Individual Participants               │
    │  2. 👥 Manage Teams                                 │
    │  3. 🎯 Manage Events                                │
    │  4. 📝 Register Participants                        │
    │  5. 🏆 Enter Results                               │
    │  6. 📊 View Rankings                               │
    │  7. 📋 Reports                                     │
    │  8. 💾 Save Data                                   │
    │  9. 📂 Load Data                                   │
    │  0. 🚪 Exit                                        │
    └─────────────────────────────────────────────────────┘
            """)
            
            choice = self.get_menu_choice(range(11))
            
            if choice == 1:
                self.individual_management()
            elif choice == 2:
                self.team_management()
            elif choice == 3:
                self.event_management()
            elif choice == 4:
                self.registration_menu()
            elif choice == 5:
                self.results_menu()
            elif choice == 6:
                self.rankings_menu()
            elif choice == 7:
                self.reports_menu()
            elif choice == 8:
                self.save_data()
            elif choice == 9:
                self.load_data()
            elif choice == 0:
                self.exit_program()
    
    # ============== Individual Management ==============
    
    def individual_management(self):
        """Individual participant management menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Individual Participant Management")
            
            print("""
    1. ➕ Add Individual
    2. ✏️  Edit Participant
    3. 🗑️  Delete Participant
    4. 👁️  View All Participants
    5. 🔍 Search Participant
    6. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(7))
            
            if choice == 1:
                self.add_individual()
            elif choice == 2:
                self.edit_individual()
            elif choice == 3:
                self.delete_individual()
            elif choice == 4:
                self.view_all_individuals()
            elif choice == 5:
                self.search_individual()
            elif choice == 6:
                break
    
    def add_individual(self):
        """Add a new individual participant"""
        self.clear_screen()
        Colors.print_subheader("Add New Individual")
        
        name = self.get_input("Name: ")
        if not name:
            return
        
        age_input = input("Age (optional): ").strip()
        age = int(age_input) if age_input else None
        
        level = input("Level (optional): ").strip() or None
        
        success, message, _ = self.service.add_individual(name, age, level)
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def edit_individual(self):
        """Edit an existing participant"""
        individuals = self.service.get_all_individuals()
        if not individuals:
            Colors.print_warning("No participants found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Edit Participant")
        
        print("\nParticipant List:")
        for i, ind in enumerate(individuals, 1):
            print(f"{i}. {ind.name} (ID: {ind.participant_id})")
        
        choice = self.get_menu_choice(range(len(individuals) + 1))
        if choice == len(individuals) + 1:
            return
        
        selected = individuals[choice - 1]
        
        print(f"\nEdit: {selected.name}")
        name = self.get_input(f"New name [{selected.name}]: ", required=False) or selected.name
        
        age_str = input(f"New age [{selected.age or 'not set'}]: ").strip()
        age = selected.age
        if age_str:
            try:
                age = int(age_str)
            except ValueError:
                Colors.print_error("Age must be a number")
        
        level = input(f"New level [{selected.level or 'not set'}]: ").strip() or selected.level
        
        success, message = self.service.update_individual(
            selected.participant_id, name, age, level
        )
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def delete_individual(self):
        """Delete a participant"""
        individuals = self.service.get_all_individuals()
        if not individuals:
            Colors.print_warning("No participants found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Delete Participant")
        
        print("\nParticipant List:")
        for i, ind in enumerate(individuals, 1):
            print(f"{i}. {ind.name} (ID: {ind.participant_id})")
        
        choice = self.get_menu_choice(range(len(individuals) + 1))
        if choice == len(individuals) + 1:
            return
        
        selected = individuals[choice - 1]
        
        # Check for existing results
        results = self.storage.get_results_by_participant(selected.participant_id)
        confirm_msg = ""
        if results:
            confirm_msg = " Warning: Participant has saved results! "
        
        if self.get_yes_no(f"Are you sure you want to delete {selected.name}?{confirm_msg}"):
            confirm_force = False
            if results:
                confirm_force = self.get_yes_no("Results will also be deleted. Continue?")
            
            success, message = self.service.delete_individual(selected.participant_id, confirm_force)
            
            if success:
                Colors.print_success(message)
            else:
                Colors.print_error(message)
        else:
            Colors.print_info("Deletion cancelled")
        
        self.pause()
    
    def view_all_individuals(self):
        """View all individual participants"""
        individuals = self.service.get_all_individuals()
        
        self.clear_screen()
        Colors.print_subheader("All Individual Participants")
        
        if not individuals:
            Colors.print_warning("No participants found")
        else:
            print(f"\n{'ID':<12} {'Name':<25} {'Age':<8} {'Points':<10} {'Events':<10}")
            print("-" * 70)
            for ind in individuals:
                print(f"{ind.participant_id:<12} {ind.name:<25} {ind.age or '-':<8} {ind.total_points:<10} {ind.events_count:<10}")
        
        self.pause()
    
    def search_individual(self):
        """Search for a participant by name"""
        name = self.get_input("Enter search name: ")
        if not name:
            return
        
        results = self.service.search_individual(name)
        
        self.clear_screen()
        Colors.print_subheader(f"Search Results for: {name}")
        
        if not results:
            Colors.print_warning("No results found")
        else:
            print(f"\n{'ID':<12} {'Name':<25} {'Age':<8} {'Points':<10}")
            print("-" * 60)
            for ind in results:
                print(f"{ind.participant_id:<12} {ind.name:<25} {ind.age or '-':<8} {ind.total_points:<10}")
        
        self.pause()
    
    # ============== Team Management ==============
    
    def team_management(self):
        """Team management menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Team Management")
            
            print("""
    1. ➕ Add New Team
    2. ✏️  Edit Team
    3. 🗑️  Delete Team
    4. 👁️  View All Teams
    5. 🔍 Search Team
    6. 👥 View Team Members
    7. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(8))
            
            if choice == 1:
                self.add_team()
            elif choice == 2:
                self.edit_team()
            elif choice == 3:
                self.delete_team()
            elif choice == 4:
                self.view_all_teams()
            elif choice == 5:
                self.search_team()
            elif choice == 6:
                self.view_team_members()
            elif choice == 7:
                break
    
    def add_team(self):
        """Add a new team"""
        self.clear_screen()
        Colors.print_subheader("Add New Team")
        
        name = self.get_input("Team Name: ")
        if not name:
            return
        
        print("\nEnter member names (5-10 members required):")
        print("Enter member name and press Enter. Type 'done' when finished.")
        
        members = []
        while len(members) < 10:
            member = input(f"Member {len(members) + 1}: ").strip()
            if member.lower() == 'done':
                break
            if member:
                members.append(member)
            
            if len(members) >= 5:
                if self.get_yes_no("Add more members?"):
                    continue
                break
        
        if len(members) < 5:
            Colors.print_error("Must have at least 5 members")
            self.pause()
            return
        
        success, message, _ = self.service.add_team(name, members)
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def edit_team(self):
        """Edit a team"""
        teams = self.service.get_all_teams()
        if not teams:
            Colors.print_warning("No teams found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Edit Team")
        
        print("\nTeam List:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name} (ID: {team.team_id}) - {len(team.members)} members")
        
        choice = self.get_menu_choice(range(len(teams) + 1))
        if choice == len(teams) + 1:
            return
        
        selected = teams[choice - 1]
        
        print(f"\nEdit: {selected.name}")
        name = self.get_input(f"New name [{selected.name}]: ", required=False) or selected.name
        
        print("\nCurrent Members:")
        for i, member in enumerate(selected.members, 1):
            print(f"  {i}. {member.name}")
        
        success, message = self.service.update_team(selected.team_id, name=name)
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def delete_team(self):
        """Delete a team"""
        teams = self.service.get_all_teams()
        if not teams:
            Colors.print_warning("No teams found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Delete Team")
        
        print("\nTeam List:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name} (ID: {team.team_id})")
        
        choice = self.get_menu_choice(range(len(teams) + 1))
        if choice == len(teams) + 1:
            return
        
        selected = teams[choice - 1]
        
        results = self.storage.get_results_by_participant(selected.team_id)
        confirm_msg = ""
        if results:
            confirm_msg = " Warning: Team has saved results! "
        
        if self.get_yes_no(f"Are you sure you want to delete team {selected.name}?{confirm_msg}"):
            confirm_force = False
            if results:
                confirm_force = self.get_yes_no("Results will also be deleted. Continue?")
            
            success, message = self.service.delete_team(selected.team_id, confirm_force)
            
            if success:
                Colors.print_success(message)
            else:
                Colors.print_error(message)
        else:
            Colors.print_info("Deletion cancelled")
        
        self.pause()
    
    def view_all_teams(self):
        """View all teams"""
        teams = self.service.get_all_teams()
        
        self.clear_screen()
        Colors.print_subheader("All Teams")
        
        if not teams:
            Colors.print_warning("No teams found")
        else:
            print(f"\n{'ID':<12} {'Team Name':<20} {'Members':<10} {'Points':<10} {'Events':<10}")
            print("-" * 70)
            for team in teams:
                print(f"{team.team_id:<12} {team.name:<20} {len(team.members):<10} {team.total_points:<10} {team.events_count:<10}")
        
        self.pause()
    
    def search_team(self):
        """Search for a team"""
        name = self.get_input("Enter search name: ")
        if not name:
            return
        
        results = self.service.search_team(name)
        
        self.clear_screen()
        Colors.print_subheader(f"Search Results for: {name}")
        
        if not results:
            Colors.print_warning("No results found")
        else:
            print(f"\n{'ID':<12} {'Team Name':<20} {'Members':<10} {'Points':<10}")
            print("-" * 60)
            for team in results:
                print(f"{team.team_id:<12} {team.name:<20} {len(team.members):<10} {team.total_points:<10}")
        
        self.pause()
    
    def view_team_members(self):
        """View team members"""
        teams = self.service.get_all_teams()
        if not teams:
            Colors.print_warning("No teams found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("View Team Members")
        
        print("\nTeam List:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name}")
        
        choice = self.get_menu_choice(range(len(teams) + 1))
        if choice == len(teams) + 1:
            return
        
        selected = teams[choice - 1]
        
        print(f"\nTeam {selected.name} Members:")
        print("-" * 40)
        for i, member in enumerate(selected.members, 1):
            print(f"  {i}. {member.name}")
        
        self.pause()
    
    # ============== Event Management ==============
    
    def event_management(self):
        """Event management menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Event Management")
            
            print("""
    1. ➕ Add New Event
    2. ✏️  Edit Event
    3. 🗑️  Delete Event
    4. 👁️  View All Events
    5. 🎯 View Open Events
    6. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(7))
            
            if choice == 1:
                self.add_event()
            elif choice == 2:
                self.edit_event()
            elif choice == 3:
                self.delete_event()
            elif choice == 4:
                self.view_all_events()
            elif choice == 5:
                self.view_open_events()
            elif choice == 6:
                break
    
    def add_event(self):
        """Add a new event"""
        self.clear_screen()
        Colors.print_subheader("Add New Event")
        
        name = self.get_input("Event Name: ")
        if not name:
            return
        
        print("\nEvent Type:")
        print("  1. Individual")
        print("  2. Group")
        event_type_choice = self.get_menu_choice(range(1, 3))
        event_type = EventType.INDIVIDUAL if event_type_choice == 1 else EventType.GROUP
        
        print("\nEvent Category:")
        print("  1. Sports")
        print("  2. Academic")
        category_choice = self.get_menu_choice(range(1, 3))
        category = EventCategory.SPORTS if category_choice == 1 else EventCategory.ACADEMIC
        
        max_str = input("Max Participants [100]: ").strip()
        max_participants = int(max_str) if max_str else 100
        
        single_event = self.get_yes_no("Is participation limited to one event only?")
        
        success, message, _ = self.service.add_event(
            name, event_type, category, max_participants, single_event
        )
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def edit_event(self):
        """Edit an event"""
        events = self.service.get_all_events()
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Edit Event")
        
        print("\nEvent List:")
        for i, event in enumerate(events, 1):
            status = "Open" if event.status == EventStatus.OPEN else "Completed"
            event_type = "Individual" if event.event_type == EventType.INDIVIDUAL else "Group"
            print(f"{i}. {event.name} (ID: {event.event_id}) - {event_type} - {status}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected = events[choice - 1]
        
        print(f"\nEdit: {selected.name}")
        name = self.get_input(f"New name [{selected.name}]: ", required=False) or selected.name
        
        max_str = input(f"Max participants [{selected.max_participants}]: ").strip()
        max_participants = selected.max_participants
        if max_str:
            try:
                max_participants = int(max_str)
            except ValueError:
                Colors.print_error("Must enter a number")
        
        success, message = self.service.update_event(
            selected.event_id, name=name, max_participants=max_participants
        )
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def delete_event(self):
        """Delete an event"""
        events = self.service.get_all_events()
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Delete Event")
        
        print("\nEvent List:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name} (ID: {event.event_id})")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected = events[choice - 1]
        
        registrations = self.storage.get_registrations_by_event(selected.event_id)
        results = self.storage.get_results_by_event(selected.event_id)
        
        confirm_msg = ""
        if registrations or results:
            confirm_msg = " Warning: Event has registrations or results! "
        
        if self.get_yes_no(f"Are you sure you want to delete event {selected.name}?{confirm_msg}"):
            confirm_force = False
            if registrations or results:
                confirm_force = self.get_yes_no("Registrations and results will also be deleted. Continue?")
            
            success, message = self.service.delete_event(selected.event_id, confirm_force)
            
            if success:
                Colors.print_success(message)
            else:
                Colors.print_error(message)
        else:
            Colors.print_info("Deletion cancelled")
        
        self.pause()
    
    def view_all_events(self):
        """View all events"""
        events = self.service.get_all_events()
        
        self.clear_screen()
        Colors.print_subheader("All Events")
        
        if not events:
            Colors.print_warning("No events found")
        else:
            print(f"\n{'ID':<12} {'Name':<20} {'Type':<10} {'Category':<12} {'Status':<10}")
            print("-" * 70)
            for event in events:
                status = "Open" if event.status == EventStatus.OPEN else "Completed"
                event_type = "Individual" if event.event_type == EventType.INDIVIDUAL else "Group"
                category = "Sports" if event.category == EventCategory.SPORTS else "Academic"
                print(f"{event.event_id:<12} {event.name:<20} {event_type:<10} {category:<12} {status:<10}")
        
        self.pause()
    
    def view_open_events(self):
        """View open events"""
        events = self.service.get_open_events()
        
        self.clear_screen()
        Colors.print_subheader("Open Events")
        
        if not events:
            Colors.print_warning("No open events found")
        else:
            print(f"\n{'ID':<12} {'Name':<20} {'Type':<10} {'Category':<12}")
            print("-" * 60)
            for event in events:
                event_type = "Individual" if event.event_type == EventType.INDIVIDUAL else "Group"
                category = "Sports" if event.category == EventCategory.SPORTS else "Academic"
                print(f"{event.event_id:<12} {event.name:<20} {event_type:<10} {category:<12}")
        
        self.pause()
    
    # ============== Registration ==============
    
    def registration_menu(self):
        """Registration menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Participant Registration")
            
            print("""
    1. 📝 Register Individual in Individual Event
    2. 👥 Register Team in Group Event
    3. 👁️  View Event Registrations
    4. ❌ Cancel Registration
    5. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(6))
            
            if choice == 1:
                self.register_individual()
            elif choice == 2:
                self.register_team()
            elif choice == 3:
                self.view_event_registrations()
            elif choice == 4:
                self.cancel_registration()
            elif choice == 5:
                break
    
    def register_individual(self):
        """Register an individual"""
        individuals = self.service.get_all_individuals()
        events = self.service.get_events_by_type(EventType.INDIVIDUAL)
        
        if not individuals:
            Colors.print_warning("No individuals registered")
            self.pause()
            return
        
        if not events:
            Colors.print_warning("No individual events available")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Register Individual in Individual Event")
        
        print("\nIndividuals:")
        for i, ind in enumerate(individuals, 1):
            print(f"{i}. {ind.name} (Points: {ind.total_points})")
        
        choice = self.get_menu_choice(range(len(individuals) + 1))
        if choice == len(individuals) + 1:
            return
        
        selected_individual = individuals[choice - 1]
        
        print("\nOpen Individual Events:")
        for i, event in enumerate(events, 1):
            regs = len(self.storage.get_registrations_by_event(event.event_id))
            print(f"{i}. {event.name} ({regs}/{event.max_participants})")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        
        success, message = self.service.register_participant(
            selected_individual.participant_id,
            ParticipantType.INDIVIDUAL,
            selected_event.event_id
        )
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def register_team(self):
        """Register a team"""
        teams = self.service.get_all_teams()
        events = self.service.get_events_by_type(EventType.GROUP)
        
        if not teams:
            Colors.print_warning("No teams registered")
            self.pause()
            return
        
        if not events:
            Colors.print_warning("No group events available")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Register Team in Group Event")
        
        print("\nTeams:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name} (Members: {len(team.members)})")
        
        choice = self.get_menu_choice(range(len(teams) + 1))
        if choice == len(teams) + 1:
            return
        
        selected_team = teams[choice - 1]
        
        print("\nOpen Group Events:")
        for i, event in enumerate(events, 1):
            regs = len(self.storage.get_registrations_by_event(event.event_id))
            print(f"{i}. {event.name} ({regs}/{event.max_participants})")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        
        success, message = self.service.register_participant(
            selected_team.team_id,
            ParticipantType.TEAM,
            selected_event.event_id
        )
        
        if success:
            Colors.print_success(message)
        else:
            Colors.print_error(message)
        
        self.pause()
    
    def view_event_registrations(self):
        """View event registrations"""
        events = self.service.get_all_events()
        
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("View Event Registrations")
        
        print("\nEvents:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        registrations = self.service.get_event_registrations(selected_event.event_id)
        
        self.clear_screen()
        print(f"Registrations for: {selected_event.name}")
        print("-" * 50)
        
        if not registrations:
            Colors.print_warning("No registrations")
        else:
            for reg in registrations:
                if reg.participant_type == ParticipantType.INDIVIDUAL:
                    ind = self.storage.get_individual(reg.participant_id)
                    name = ind.name if ind else "Unknown"
                else:
                    team = self.storage.get_team(reg.participant_id)
                    name = team.name if team else "Unknown"
                
                print(f"  - {name} ({reg.participant_type.value})")
        
        self.pause()
    
    def cancel_registration(self):
        """Cancel a registration"""
        Colors.print_info("Registration cancellation feature under development")
        self.pause()
    
    # ============== Results ==============
    
    def results_menu(self):
        """Results menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Enter Results")
            
            print("""
    1. 🏆 Enter Result for Event
    2. 📊 View Event Results
    3. ✅ Close Event (Mark Complete)
    4. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(5))
            
            if choice == 1:
                self.enter_result()
            elif choice == 2:
                self.view_event_results()
            elif choice == 3:
                self.complete_event()
            elif choice == 4:
                break
    
    def enter_result(self):
        """Enter a result"""
        events = self.service.get_all_events()
        
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Enter Result")
        
        print("\nEvents:")
        for i, event in enumerate(events, 1):
            status = "Completed" if event.status == EventStatus.COMPLETED else "Open"
            print(f"{i}. {event.name} - {status}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        
        if selected_event.status == EventStatus.COMPLETED:
            if self.get_yesno("Event is closed. Re-enter results?"):
                pass
            else:
                return
        
        registrations = self.service.get_event_registrations(selected_event.event_id)
        
        if not registrations:
            Colors.print_warning("No registrations in this event")
            self.pause()
            return
        
        self.clear_screen()
        print(f"Enter results: {selected_event.name}")
        print("-" * 50)
        
        current_results = self.service.get_event_results(selected_event.event_id)
        placed_participants = {r.participant_id: r.rank for r in current_results}
        
        for reg in registrations:
            if reg.participant_type == ParticipantType.INDIVIDUAL:
                ind = self.storage.get_individual(reg.participant_id)
                name = ind.name if ind else "Unknown"
            else:
                team = self.storage.get_team(reg.participant_id)
                name = team.name if team else "Unknown"
            
            current_rank = placed_participants.get(reg.participant_id, None)
            if current_rank:
                Colors.print_info(f"{name} - Current rank: {current_rank}")
            
            rank_str = input(f"Rank for {name}: ").strip()
            if not rank_str:
                continue
            
            try:
                rank = int(rank_str)
            except ValueError:
                Colors.print_error("Rank must be a number")
                continue
            
            success, message = self.service.enter_result(
                selected_event.event_id,
                reg.participant_id,
                reg.participant_type,
                rank
            )
            
            if success:
                Colors.print_success(message)
            else:
                Colors.print_error(message)
        
        self.pause()
    
    def view_event_results(self):
        """View event results"""
        events = self.service.get_all_events()
        
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("View Event Results")
        
        print("\nEvents:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        results = self.service.get_event_results(selected_event.event_id)
        
        self.clear_screen()
        print(f"Results: {selected_event.name}")
        print("-" * 50)
        
        if not results:
            Colors.print_warning("No results entered yet")
        else:
            for result in results:
                if result.participant_type == ParticipantType.INDIVIDUAL:
                    ind = self.storage.get_individual(result.participant_id)
                    name = ind.name if ind else "Unknown"
                else:
                    team = self.storage.get_team(result.participant_id)
                    name = team.name if team else "Unknown"
                
                print(f"  Rank {result.rank}: {name} - {result.points} points")
        
        self.pause()
    
    def complete_event(self):
        """Close an event"""
        events = self.service.get_open_events()
        
        if not events:
            Colors.print_warning("No open events")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Close Event")
        
        print("\nOpen Events:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        
        if self.get_yes_no(f"Close event {selected_event.name}?"):
            success, message = self.service.update_event(
                selected_event.event_id, status=EventStatus.COMPLETED
            )
            
            if success:
                Colors.print_success("Event closed successfully")
            else:
                Colors.print_error(message)
        
        self.pause()
    
    # ============== Rankings ==============
    
    def rankings_menu(self):
        """Rankings menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Rankings")
            
            print("""
    1. 🏅 Individual Rankings
    2. 👥 Team Rankings
    3. 🏆 Winners
    4. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(5))
            
            if choice == 1:
                self.view_individual_rankings()
            elif choice == 2:
                self.view_team_rankings()
            elif choice == 3:
                self.view_winners()
            elif choice == 4:
                break
    
    def view_individual_rankings(self):
        """View individual rankings"""
        individual_rankings, _ = self.service.calculate_rankings()
        
        self.clear_screen()
        Colors.print_subheader("Individual Rankings")
        
        if not individual_rankings:
            Colors.print_warning("No rankings available")
        else:
            print(f"\n{'Rank':<10} {'Name':<25} {'Points':<10} {'Events':<10}")
            print("-" * 60)
            for ranking in individual_rankings:
                print(f"{ranking.rank:<10} {ranking.participant_name:<25} {ranking.total_points:<10} {ranking.events_participated:<10}")
        
        self.pause()
    
    def view_team_rankings(self):
        """View team rankings"""
        _, team_rankings = self.service.calculate_rankings()
        
        self.clear_screen()
        Colors.print_subheader("Team Rankings")
        
        if not team_rankings:
            Colors.print_warning("No rankings available")
        else:
            print(f"\n{'Rank':<10} {'Team Name':<25} {'Points':<10} {'Events':<10}")
            print("-" * 60)
            for ranking in team_rankings:
                print(f"{ranking.rank:<10} {ranking.participant_name:<25} {ranking.total_points:<10} {ranking.events_participated:<10}")
        
        self.pause()
    
    def view_winners(self):
        """View winners"""
        individual_winner, team_winner = self.service.get_winner()
        
        self.clear_screen()
        Colors.print_subheader("🏆 Winners")
        
        if individual_winner:
            print(f"\n👤 Winner (Individual): {individual_winner.participant_name}")
            print(f"   Points: {individual_winner.total_points}")
        else:
            print("\n👤 No individual winner yet")
        
        if team_winner:
            print(f"\n👥 Winner (Team): {team_winner.participant_name}")
            print(f"   Points: {team_winner.total_points}")
        else:
            print("\n👥 No team winner yet")
        
        self.pause()
    
    # ============== Reports ==============
    
    def reports_menu(self):
        """Reports menu"""
        while True:
            self.clear_screen()
            Colors.print_subheader("Reports")
            
            print("""
    1. 📊 Overall Statistics
    2. 📋 Event Report
    3. ❌ Incomplete Events
    4. 👤 Unregistered Participants
    5. 📁 Export to CSV
    6. 🔙 Back
            """)
            
            choice = self.get_menu_choice(range(7))
            
            if choice == 1:
                self.view_statistics()
            elif choice == 2:
                self.event_report()
            elif choice == 3:
                self.uncompleted_events()
            elif choice == 4:
                self.unregistered_participants()
            elif choice == 5:
                self.export_csv()
            elif choice == 6:
                break
    
    def view_statistics(self):
        """View statistics"""
        stats = self.storage.get_statistics()
        
        self.clear_screen()
        Colors.print_subheader("Championship Statistics")
        
        print(f"""
    📊 Statistics:
    ─────────────────
    👤 Total Individuals: {stats['total_individuals']}
    👥 Total Teams: {stats['total_teams']}
    🎯 Total Events: {stats['total_events']}
    📝 Total Registrations: {stats['total_registrations']}
    🏆 Total Results: {stats['total_results']}
    
    📈 Event Status:
    ─────────────────
    ✅ Completed Events: {stats['completed_events']}
    ⏳ Open Events: {stats['open_events']}
        """)
        
        self.pause()
    
    def event_report(self):
        """Event report"""
        events = self.service.get_all_events()
        
        if not events:
            Colors.print_warning("No events found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Event Report")
        
        print("\nEvents:")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.name}")
        
        choice = self.get_menu_choice(range(len(events) + 1))
        if choice == len(events) + 1:
            return
        
        selected_event = events[choice - 1]
        report = self.service.generate_event_report(selected_event.event_id)
        
        self.clear_screen()
        print(f"Report: {selected_event.name}")
        print("=" * 50)
        print(f"Type: {'Individual' if selected_event.event_type == EventType.INDIVIDUAL else 'Group'}")
        print(f"Category: {'Sports' if selected_event.category == EventCategory.SPORTS else 'Academic'}")
        print(f"Status: {report.get('status', 'Unknown')}")
        print(f"Registrations: {report.get('total_registrations', 0)}")
        
        results = report.get('results', [])
        if results:
            print("\nResults:")
            for r in results:
                name = "Unknown"
                if r.participant_type == ParticipantType.INDIVIDUAL:
                    ind = self.storage.get_individual(r.participant_id)
                    if ind:
                        name = ind.name
                else:
                    team = self.storage.get_team(r.participant_id)
                    if team:
                        name = team.name
                print(f"  Rank {r.rank}: {name} - {r.points} points")
        
        self.pause()
    
    def uncompleted_events(self):
        """View uncompleted events"""
        events = self.service.get_uncompleted_events()
        
        self.clear_screen()
        Colors.print_subheader("Incomplete Events")
        
        if not events:
            Colors.print_success("All events are complete!")
        else:
            print(f"\n{'Name':<25} {'Type':<12} {'Registrations':<10}")
            print("-" * 50)
            for event in events:
                regs = len(self.storage.get_registrations_by_event(event.event_id))
                event_type = "Individual" if event.event_type == EventType.INDIVIDUAL else "Group"
                print(f"{event.name:<25} {event_type:<12} {regs:<10}")
        
        self.pause()
    
    def unregistered_participants(self):
        """View unregistered participants"""
        unregistered = self.service.get_unregistered_participants()
        
        self.clear_screen()
        Colors.print_subheader("Unregistered Participants")
        
        if not unregistered:
            Colors.print_success("All participants are registered in events!")
        else:
            print(f"\n{'Type':<10} {'Name':<25}")
            print("-" * 40)
            for p in unregistered:
                print(f"{p['type']:<10} {p['name']:<25}")
        
        self.pause()
    
    def export_csv(self):
        """Export to CSV"""
        files = self.storage.export_to_csv()
        
        self.clear_screen()
        Colors.print_subheader("Export to CSV")
        
        if files:
            Colors.print_success("Exported successfully:")
            for f in files:
                print(f"  - {f}")
        else:
            Colors.print_warning("No data to export")
        
        self.pause()
    
    # ============== Data Management ==============
    
    def save_data(self):
        """Save data"""
        filename = self.storage.save_to_json()
        
        Colors.print_success(f"Data saved to: {filename}")
        self.pause()
    
    def load_data(self):
        """Load data"""
        files = []
        data_dir = self.storage.data_dir
        
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
            files.sort(reverse=True)
        
        if not files:
            Colors.print_warning("No save files found")
            self.pause()
            return
        
        self.clear_screen()
        Colors.print_subheader("Load Data")
        
        print("\nAvailable save files:")
        for i, f in enumerate(files[:10], 1):
            print(f"{i}. {f}")
        
        choice = self.get_menu_choice(range(len(files[:10]) + 1))
        if choice == len(files[:10]) + 1:
            return
        
        filename = os.path.join(data_dir, files[choice - 1])
        
        if self.storage.load_from_json(filename):
            Colors.print_success("Data loaded successfully")
        else:
            Colors.print_error("Failed to load data")
        
        self.pause()
    
    # ============== Exit ==============
    
    def exit_program(self):
        """Exit the program"""
        if self.get_yes_no("Would you like to save data before exiting?"):
            self.save_data()
        
        self.running = False
        Colors.print_info("Thank you for using Championship System!")

