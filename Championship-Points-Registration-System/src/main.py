"""
================================================================================
Championship Points Registration System - Main Entry Point (VERSION 2.0)
================================================================================

Module Overview:
----------------
This is the main entry point for the Championship Points Registration System.
It initializes the application and launches the GUI interface.

Author: Development Team
Version: 2.0
Year: 2026

Key Features:
-------------
- GUI-based interface
- Tournament management
- Participant registration
- Results tracking
- Rankings and reports
- Settings management
- Multi-language support (English/Arabic)
- Color themes for accessibility

Individual Responsibility:
------------------------
- Clear module boundaries
- Self-contained functionality
- Comprehensive error handling

Creativity:
----------
- Flexible points system
- Multiple event types
- Customizable configurations
- Sound effects
- Image/logo support

Self-Management:
----------------
- Automatic data persistence
- Version tracking
- Audit logging
- Result validation
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import tkinter as tk
from gui import TournamentGUI


# ==============================================================================
# SECTION: APPLICATION CONSTANTS
# ==============================================================================

# Application identification
APP_VERSION = "2.0"
APP_YEAR = 2026
APP_NAME = "Championship Points Registration System"

# Short name for display
APP_SHORT_NAME = "CPRS"


# ==============================================================================
# SECTION: MAIN ENTRY POINT
# ==============================================================================

def main():
    """
    Main entry point - Launches the GUI application.
    
    This function initializes the main application window and starts
    the Tkinter event loop. All application components are initialized
    here before the GUI is displayed.
    
    Individual Accountability:
    --------------------------
    - Initializes all system components
    - Sets up error handling
    - Launches the main application loop
    
    Example:
        >>> main()  # Starts the application
        Starting Championship Points Registration System v2.0 (2026)
    """
    # Display startup information
    print(f"Starting {APP_NAME} v{APP_VERSION} ({APP_YEAR})")
    print("=" * 60)
    print(f"Version {APP_VERSION} - Enhanced with new features:")
    print("  - Settings system with volume control")
    print("  - Color themes for accessibility")
    print("  - Multi-language support (English/Arabic)")
    print("  - Sound effects")
    print("  - Custom logo support")
    print("  - Video tutorial guide")
    print("=" * 60)
    
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = TournamentGUI(root)
    
    # Start the main event loop
    # This blocks until the application is closed
    root.mainloop()
    
    # Display closing message
    print(f"\n{APP_NAME} closed. Thank you for using!")


# ==============================================================================
# SECTION: APPLICATION LAUNCHER
# ==============================================================================

if __name__ == "__main__":
    """
    Standard Python entry point check.
    
    This ensures the main() function is only called when the
    script is executed directly (not imported as a module).
    """
    main()


# ==============================================================================
# END OF MODULE
# ==============================================================================

