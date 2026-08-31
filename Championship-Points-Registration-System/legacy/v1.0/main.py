"""
Championship Points Registration System - Main Entry Point
================================================================================

Author: Development Team
Version: 1.0
Year: 2026
================================================================================

This is the main entry point for the Championship Points Registration System.
The system provides comprehensive tournament management capabilities including:
- Individual and Team participant management
- Event creation and management
- Participant registration system
- Results entry and tracking
- Ranking calculation and display
- Data export (JSON/CSV)

Individual Responsibility:
- Clear module boundaries
- Self-contained functionality
- Comprehensive error handling

Creativity:
- Flexible points system
- Multiple event types
- Customizable configurations

Self-Management:
- Automatic data persistence
- Version tracking
- Audit logging
- Result validation
"""

import tkinter as tk
from gui import TournamentGUI


# Application constants
APP_VERSION = "1.0"
APP_YEAR = 2026
APP_NAME = "Championship Points Registration System"


def main():
    """
    Main entry point - Launches the GUI application
    
    Individual Accountability:
    - Initializes all system components
    - Sets up error handling
    - Launches the main application loop
    """
    print(f"Starting {APP_NAME} v{APP_VERSION} ({APP_YEAR})")
    print("=" * 60)
    
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()
    
    print(f"\n{APP_NAME} closed. Thank you for using!")


if __name__ == "__main__":
    main()

