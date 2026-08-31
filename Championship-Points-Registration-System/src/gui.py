"""
================================================================================
Championship Points Registration System - GUI Version (VERSION 2.0)
================================================================================

Module Overview:
----------------
This module provides the graphical user interface (GUI) for the Championship
Points Registration System. It uses tkinter to create a modern, user-friendly
interface with comprehensive features.

Author: Development Team
Version: 2.0
Year: 2026

Features:
-------------
- Individual and Team Management
- Event Creation and Management
- Participant Registration System
- Results Entry and Tracking
- Ranking Calculation and Display
- Data Export (JSON/CSV)
- Settings System (Volume, Theme, Language)
- Sound Effects
- Custom Logo Support
- Video Tutorial Guide
- Enhanced Visual Design

Individual Responsibility:
-------------------------
- Each module has clear ownership and responsibilities
- Comprehensive error handling and validation
- Self-documenting code with detailed docstrings
- Result review mechanisms for data integrity

Creativity:
-----------
- Flexible points system
- Multiple event types and categories
- Customizable participant limits
- Modern UI with smooth interactions
- Accessibility features (color themes)

Self-Management:
---------------
- Automatic data persistence
- Version tracking
- Result validation and review
- Statistics and reporting
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import tkinter.font as tkfont
import os
import webbrowser
from typing import Optional
from datetime import datetime
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import models and enums
from models import (
    IndividualParticipant,
    Team,
    Event,
    Result,
    Ranking,
    ParticipantType,
    EventType,
    EventCategory,
    EventStatus,
    AppSettings,
    ColorTheme,
    Language,
    FontSize,
    ColorThemes
)

# Import services
from services import TournamentService

# Import storage
from storage import Storage

# Import winsound for Windows sound effects (will fallback for other OS)
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


# ==============================================================================
# SECTION: APPLICATION CONSTANTS
# ==============================================================================

# Application identification
APP_VERSION = "2.0"
APP_YEAR = 2026
APP_NAME = "Championship Points Registration System"
APP_SHORT_NAME = "CPRS"

# Data directory - separate folder for VERSION_2.0 to avoid conflicts
DATA_DIR = "tournament_data_v2"

# Default window dimensions
DEFAULT_WIDTH = 1100
DEFAULT_HEIGHT = 750


# ==============================================================================
# SECTION: TRANSLATION SYSTEM
# ==============================================================================

class Translations:
    """
    Translation system for multi-language support.
    
    This class provides translations for all UI text elements
    in both English and Arabic.
    """
    
    # English translations
    ENGLISH = {
        # Main window
        "app_title": "Championship Points Registration System",
        "ready": "Ready",
        
        # Menu
        "file": "File",
        "save_data": "Save Data",
        "load_data": "Load Data",
        "export_csv": "Export CSV",
        "exit": "Exit",
        "settings": "Settings",
        "volume": "Volume",
        "increase_volume": "Increase Volume",
        "decrease_volume": "Decrease Volume",
        "sound_enabled": "Sound Enabled",
        "color_theme": "Color Theme",
        "default_blue": "Default (Blue)",
        "high_contrast": "High Contrast",
        "protanopia": "Protanopia (Red-blind)",
        "deuteranopia": "Deuteranopia (Green-blind)",
        "tritanopia": "Tritanopia (Blue-blind)",
        "language": "Language",
        "set_logo": "Set Logo Image...",
        "help": "Help",
        "video_tutorial": "Video Tutorial",
        "about": "About",
        
        # Main buttons
        "manage_individuals": "Manage Individuals",
        "manage_teams": "Manage Teams",
        "manage_events": "Manage Events",
        "register_participants": "Register Participants",
        "enter_results": "Enter Results",
        "view_rankings": "View Rankings",
        "reports": "Reports",
        "settings_btn": "Settings",
        
        # Individual management
        "manage_individual_participants": "Manage Individual Participants",
        "add_new": "Add New",
        "edit": "Edit",
        "delete": "Delete",
        "refresh": "Refresh",
        "id": "ID",
        "name": "Name",
        "age": "Age",
        "level": "Level",
        "points": "Points",
        "events": "Events",
        "add_individual_participant": "Add Individual Participant",
        "edit_participant": "Edit Participant",
        "name_required": "Name is required",
        "age_must_be_number": "Age must be a number",
        "updated_successfully": "Updated successfully",
        "deleted_successfully": "Deleted successfully",
        "select_participant_to_edit": "Select a participant to edit",
        "select_participant_to_delete": "Select a participant to delete",
        "confirm_delete": "Are you sure you want to delete this participant?",
        "participant_not_found": "Participant not found",
        
        # Team management
        "manage_teams_title": "Manage Teams",
        "add_team": "Add Team",
        "edit_name": "Edit Name",
        "view_members": "View Members",
        "team_name": "Team Name",
        "members": "Members",
        "add_new_team": "Add New Team",
        "member_names_one_per_line": "Member Names (one per line):",
        "enter_at_least_5": "(Enter at least 5 members, max 10)",
        "team_name_required": "Team name is required",
        "must_enter_5_members": "Must enter at least 5 members",
        "edit_team_name": "Edit Team Name",
        "team_name_updated": "Team name updated successfully",
        "team_not_found": "Team not found",
        "select_team_to_edit": "Select a team to edit",
        "select_team_to_view": "Select a team to view members",
        "team_members": "Team Members",
        "total_members": "Total Members:",
        
        # Event management
        "manage_events_title": "Manage Events",
        "add_event": "Add Event",
        "event_name": "Event Name",
        "event_type": "Event Type",
        "individual": "Individual",
        "group_team": "Group (Team)",
        "category": "Category",
        "sports": "Sports",
        "academic": "Academic",
        "max_participants": "Max Participants:",
        "single_event_only": "Single event only (one event per participant)",
        "add_new_event": "Add New Event",
        "event_name_required": "Event name is required",
        "edit_event_name": "Edit Event Name",
        "event_name_updated": "Event name updated successfully",
        "select_event_to_edit": "Select an event to edit",
        
        # Registration
        "register_participants_title": "Register Participants",
        "select_registration_type": "Select Registration Type:",
        "register_individual_event": "Register Individual in Individual Event",
        "register_team_group": "Register Team in Group Event",
        "select_individual": "Select Individual:",
        "select_event_individual": "Select Event (Individual):",
        "select_team": "Select Team:",
        "select_event_group": "Select Event (Group):",
        "no_individuals_registered": "No individuals registered",
        "no_individual_events": "No individual events available",
        "no_teams_registered": "No teams registered",
        "no_group_events": "No group events available",
        "select_individual_and_event": "Select individual and event",
        "select_team_and_event": "Select team and event",
        "registration_successful": "Registration successful",
        
        # Results
        "enter_results_title": "Enter Results",
        "select_event": "Select Event:",
        "no_events_available": "No events available",
        "continue": "Continue",
        "enter_rank_for": "Enter rank for each participant in:",
        "no_participants_registered": "No participants registered",
        "results_saved": "Results saved:",
        "entries": "entries",
        
        # Rankings
        "view_rankings_title": "View Rankings",
        "individual_rankings": "Individual Rankings",
        "team_rankings": "Team Rankings",
        "rank": "Rank",
        
        # Reports
        "reports_title": "Reports",
        "overall_statistics": "Overall Statistics",
        "total_individuals": "Total Individuals:",
        "total_teams": "Total Teams:",
        "total_events": "Total Events:",
        "total_registrations": "Total Registrations:",
        "total_results": "Total Results:",
        "completed_events": "Completed Events:",
        "open_events": "Open Events:",
        
        # Settings dialog
        "settings_title": "Settings",
        "application_settings": "Application Settings",
        "volume_control": "Volume Control",
        "volume_percent": "Volume %",
        "enable_sound_effects": "Enable Sound Effects",
        "color_theme_title": "Color Theme",
        "language_title": "Language",
        "logo_title": "Logo",
        "choose_logo_image": "Choose Logo Image...",
        "font_size_title": "Font Size",
        "font_small": "Small",
        "font_medium": "Medium",
        "font_large": "Large",
        "font_extra_large": "Extra Large",
        "custom_title_title": "Custom Title",
        "set_custom_title": "Set Custom Title...",
        "current": "Current:",
        "close": "Close",
        
        # Video guide
        "video_tutorial_guide": "Video Tutorial Guide",
        "video_path": "Video Path",
        "set_video_path": "Set Video Path...",
        
        # Dialogs
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "confirm": "Confirm",
        "load_data_title": "Load Data",
        "would_load_last_saved": "Would you like to load the last saved data?",
        "data_loaded_successfully": "Data loaded successfully",
        "welcome": "Welcome!",
        "welcome_message": "Welcome to Championship Points Registration System v2.0!\n\nWould you like to watch a video tutorial on how to use this program?",
        "language_changed": "Language Changed",
        "language_changed_message": "Language changed to {}.\nSome UI elements may require restart to update fully.",
        "logo_updated": "Logo updated successfully!",
        "exit_title": "Exit",
        "save_before_exit": "Would you like to save data before exiting?",
        
        # About
        "about_title": "About",
        "about_text": "A professional tournament points registration and management system with graphical user interface.",
        "features": "Features:",
        "thank_you": "Thank you for using our application!",
    }
    
    # Arabic translations
    ARABIC = {
        # Main window
        "app_title": "نظام تسجيل نقاط البطولات",
        "ready": "جاهز",

        # Menu
        "file": "ملف",
        "save_data": "حفظ البيانات",
        "load_data": "تحميل البيانات",
        "export_csv": "تصدير CSV",
        "exit": "خروج",
        "settings": "الإعدادات",
        "volume": "مستوى الصوت",
        "increase_volume": "رفع الصوت",
        "decrease_volume": "خفض الصوت",
        "sound_enabled": "تفعيل المؤثرات الصوتية",
        "color_theme": "لون المظهر",
        "default_blue": "الافتراضي (أزرق)",
        "high_contrast": "تباين عالٍ",
        "protanopia": "عمى الأحمر",
        "deuteranopia": "عمى الأخضر",
        "tritanopia": "عمى الأزرق",
        "language": "اللغة",
        "set_logo": "اختيار صورة الشعار...",
        "help": "مساعدة",
        "video_tutorial": "شرح فيديو",
        "about": "حول",

        # Main buttons
        "manage_individuals": "إدارة الأفراد",
        "manage_teams": "إدارة الفرق",
        "manage_events": "إدارة الفعاليات",
        "register_participants": "تسجيل المشاركين",
        "enter_results": "إدخال النتائج",
        "view_rankings": "عرض الترتيب",
        "reports": "التقارير",
        "settings_btn": "الإعدادات",

        # Individual management
        "manage_individual_participants": "إدارة المشاركين الأفراد",
        "add_new": "إضافة جديد",
        "edit": "تعديل",
        "delete": "حذف",
        "refresh": "تحديث",
        "id": "المعرّف",
        "name": "الاسم",
        "age": "العمر",
        "level": "المستوى",
        "points": "النقاط",
        "events": "الفعاليات",
        "add_individual_participant": "إضافة مشارك فردي",
        "edit_participant": "تعديل المشارك",
        "name_required": "الاسم مطلوب",
        "age_must_be_number": "العمر يجب أن يكون رقمًا",
        "updated_successfully": "تم التحديث بنجاح",
        "deleted_successfully": "تم الحذف بنجاح",
        "select_participant_to_edit": "اختر مشاركًا للتعديل",
        "select_participant_to_delete": "اختر مشاركًا للحذف",
        "confirm_delete": "هل أنت متأكد من حذف هذا المشارك؟",
        "participant_not_found": "المشارك غير موجود",

        # Team management
        "manage_teams_title": "إدارة الفرق",
        "add_team": "إضافة فريق",
        "edit_name": "تعديل الاسم",
        "view_members": "عرض الأعضاء",
        "team_name": "اسم الفريق",
        "members": "الأعضاء",
        "add_new_team": "إضافة فريق جديد",
        "member_names_one_per_line": "أسماء الأعضاء (اسم واحد في كل سطر):",
        "enter_at_least_5": "(أدخل 5 أعضاء على الأقل، والحد الأقصى 10)",
        "team_name_required": "اسم الفريق مطلوب",
        "must_enter_5_members": "يجب إدخال 5 أعضاء على الأقل",
        "edit_team_name": "تعديل اسم الفريق",
        "team_name_updated": "تم تحديث اسم الفريق بنجاح",
        "team_not_found": "الفريق غير موجود",
        "select_team_to_edit": "اختر فريقًا للتعديل",
        "select_team_to_view": "اختر فريقًا لعرض الأعضاء",
        "team_members": "أعضاء الفريق",
        "total_members": "إجمالي الأعضاء:",

        # Event management
        "manage_events_title": "إدارة الفعاليات",
        "add_event": "إضافة فعالية",
        "event_name": "اسم الفعالية",
        "event_type": "نوع الفعالية",
        "individual": "فردي",
        "group_team": "جماعي (فريق)",
        "category": "الفئة",
        "sports": "رياضية",
        "academic": "أكاديمية",
        "max_participants": "الحد الأقصى للمشاركين:",
        "single_event_only": "فعالية واحدة فقط (مشاركة واحدة لكل مشارك)",
        "add_new_event": "إضافة فعالية جديدة",
        "event_name_required": "اسم الفعالية مطلوب",
        "edit_event_name": "تعديل اسم الفعالية",
        "event_name_updated": "تم تحديث اسم الفعالية بنجاح",
        "select_event_to_edit": "اختر فعالية للتعديل",

        # Registration
        "register_participants_title": "تسجيل المشاركين",
        "select_registration_type": "اختر نوع التسجيل:",
        "register_individual_event": "تسجيل فرد في فعالية فردية",
        "register_team_group": "تسجيل فريق في فعالية جماعية",
        "select_individual": "اختر الفرد:",
        "select_event_individual": "اختر الفعالية (فردية):",
        "select_team": "اختر الفريق:",
        "select_event_group": "اختر الفعالية (جماعية):",
        "no_individuals_registered": "لا يوجد أفراد مسجلون",
        "no_individual_events": "لا توجد فعاليات فردية",
        "no_teams_registered": "لا توجد فرق مسجلة",
        "no_group_events": "لا توجد فعاليات جماعية",
        "select_individual_and_event": "اختر الفرد والفعالية",
        "select_team_and_event": "اختر الفريق والفعالية",
        "registration_successful": "تم التسجيل بنجاح",

        # Results
        "enter_results_title": "إدخال النتائج",
        "select_event": "اختر الفعالية:",
        "no_events_available": "لا توجد فعاليات",
        "continue": "متابعة",
        "enter_rank_for": "أدخل الترتيب لكل مشارك في:",
        "no_participants_registered": "لا يوجد مشاركون مسجلون",
        "results_saved": "تم حفظ النتائج:",
        "entries": "إدخالات",

        # Rankings
        "view_rankings_title": "عرض الترتيب",
        "individual_rankings": "ترتيب الأفراد",
        "team_rankings": "ترتيب الفرق",
        "rank": "الترتيب",

        # Reports
        "reports_title": "التقارير",
        "overall_statistics": "الإحصائيات العامة",
        "total_individuals": "إجمالي الأفراد:",
        "total_teams": "إجمالي الفرق:",
        "total_events": "إجمالي الفعاليات:",
        "total_registrations": "إجمالي التسجيلات:",
        "total_results": "إجمالي النتائج:",
        "completed_events": "الفعاليات المكتملة:",
        "open_events": "الفعاليات المفتوحة:",

        # Settings dialog
        "settings_title": "الإعدادات",
        "application_settings": "إعدادات التطبيق",
        "volume_control": "التحكم بالصوت",
        "volume_percent": "نسبة الصوت %",
        "enable_sound_effects": "تفعيل المؤثرات الصوتية",
        "color_theme_title": "لون المظهر",
        "language_title": "اللغة",
        "logo_title": "الشعار",
        "choose_logo_image": "اختيار صورة الشعار...",
        "font_size_title": "حجم الخط",
        "font_small": "صغير",
        "font_medium": "متوسط",
        "font_large": "كبير",
        "font_extra_large": "كبير جدًا",
        "custom_title_title": "عنوان التطبيق",
        "set_custom_title": "تعديل عنوان التطبيق...",
        "current": "الحالي:",
        "close": "إغلاق",

        # Video guide
        "video_tutorial_guide": "دليل الشرح بالفيديو",
        "video_path": "مسار الفيديو",
        "set_video_path": "تحديد مسار الفيديو...",

        # Dialogs
        "success": "نجاح",
        "error": "خطأ",
        "warning": "تحذير",
        "confirm": "تأكيد",
        "load_data_title": "تحميل البيانات",
        "would_load_last_saved": "هل تريد تحميل آخر بيانات محفوظة؟",
        "data_loaded_successfully": "تم تحميل البيانات بنجاح",
        "welcome": "مرحبًا!",
        "welcome_message": "مرحبًا بك في نظام تسجيل نقاط البطولات الإصدار 2.0!\n\nهل تريد مشاهدة شرح فيديو عن كيفية استخدام البرنامج؟",
        "language_changed": "تم تغيير اللغة",
        "language_changed_message": "تم تغيير اللغة إلى {}.\nقد تحتاج بعض عناصر الواجهة إلى إعادة تشغيل للتحديث الكامل.",
        "logo_updated": "تم تحديث الشعار بنجاح!",
        "exit_title": "خروج",
        "save_before_exit": "هل تريد حفظ البيانات قبل الخروج؟",

        # About
        "about_title": "حول",
        "about_text": "نظام احترافي لتسجيل وإدارة نقاط البطولات بواجهة رسومية.",
        "features": "المميزات:",
        "thank_you": "شكرًا لاستخدامك تطبيقنا!",

        # Load Data
        "load_specific": "تحميل ملف محدد...",
        "no_files": "لا توجد ملفات حفظ",
    }
    @classmethod
    def get_text(cls, key: str, language: str = "english") -> str:
        """
        Get translated text for a key.
        
        Args:
            key: Translation key
            language: Language code ('english' or 'arabic')
            
        Returns:
            Translated text or key if not found
        """
        translations = cls.ARABIC if language == "arabic" else cls.ENGLISH
        return translations.get(key, key)
    
    @classmethod
    def is_rtl(cls, language: str) -> bool:
        """
        Check if language is right-to-left.
        
        Args:
            language: Language code
            
        Returns:
            True if RTL language
        """
        return language == "arabic"


# Global translation instance
translations = Translations()


# ==============================================================================
# SECTION: SOUND MANAGER
# ==============================================================================

class SoundManager:
    """
    Manages sound effects for the application.
    
    This class handles playing sound effects based on user actions
    and current volume settings. It supports button click sounds,
    success sounds, and other audio feedback.
    
    Attributes:
        enabled: Whether sound effects are enabled
        volume: Volume level (0.0 to 1.0)
    """
    
    def __init__(self):
        """Initialize sound manager with default settings."""
        self.enabled = True
        self.volume = 0.5
    
    def set_enabled(self, enabled: bool):
        """Enable or disable sound effects."""
        self.enabled = enabled
    
    def set_volume(self, volume: float):
        """Set the volume level."""
        self.volume = max(0.0, min(1.0, volume))
    
    def play_click(self):
        """
        Play button click sound.
        
        This sound is played when users click buttons.
        """
        if not self.enabled or not SOUND_AVAILABLE:
            return
        
        try:
            # Use system beep with frequency based on volume
            freq = int(800 + (self.volume * 400))
            winsound.Beep(freq, 50)
        except:
            pass
    
    def play_success(self):
        """
        Play success/result sound.
        
        This sound is played when results are entered or
        when operations complete successfully.
        """
        if not self.enabled or not SOUND_AVAILABLE:
            return
        
        try:
            # Play a pleasant success tone
            freq = int(600 + (self.volume * 200))
            winsound.Beep(freq, 100)
            winsound.Beep(freq + 200, 100)
        except:
            pass
    
    def play_notification(self):
        """
        Play notification sound.
        
        This sound is played for important notifications.
        """
        if not self.enabled or not SOUND_AVAILABLE:
            return
        
        try:
            freq = int(500 + (self.volume * 300))
            winsound.Beep(freq, 150)
        except:
            pass


# ==============================================================================
# SECTION: GUI APPLICATION CLASS
# ==============================================================================

class TournamentGUI:
    """
    Main GUI Application Class for Tournament Management.
    
    This class manages the entire graphical user interface, including:
    - Main window and navigation
    - Individual/Team/Event management
    - Registration and results
    - Rankings and reports
    - Settings dialog
    
    Responsibilities:
    ----------------
    - Initialize and manage the main application window
    - Handle all user interactions through the GUI
    - Coordinate with services layer for business logic
    - Manage data persistence through storage layer
    
    Individual Accountability:
    -------------------------
    - All UI operations are self-contained and validated
    - Clear error messages for user feedback
    - Proper state management for data integrity
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application with all components.
        
        Args:
            root: Tkinter root window
        """
        # =========================================================================
        # SECTION: INITIALIZATION
        # =========================================================================
        
        # Store root window reference
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
        self.root.resizable(True, True)
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Store tree references for management windows
        self.teams_tree = None
        self.events_tree = None
        
        # =========================================================================
        # SECTION: COMPONENT INITIALIZATION
        # =========================================================================
        
        # Initialize storage
        self.storage = Storage()
        
        # Initialize service
        self.service = TournamentService(self.storage)
        
        # Load settings
        self.settings = self.service.get_settings()
        self._update_window_title()
        self._apply_font_size()
        self.root.bind_all("<Map>", self._on_widget_map, add="+")
        
        # Apply settings to sound manager
        self.sound_manager.set_enabled(self.settings.sound_enabled)
        self.sound_manager.set_volume(self.settings.volume)
        
        # Load last saved data
        self._load_last_data()
        
        # =========================================================================
        # SECTION: GUI CREATION
        # =========================================================================
        
        # Create styles
        self._create_styles()
        
        # Create menu
        self._create_menu()
        
        # Create main frame
        self._create_main_frame()
        
        # Log initialization
        self._log_event("Application started successfully")
        
        # Show video guide if not watched
        if not self.settings.video_guide_watched:
            self.root.after(500, self._prompt_video_guide)

    def _update_window_title(self):
        """Update window title based on selected language and custom title."""
        lang = self.settings.language.value
        title = self.settings.custom_title if self.settings.custom_title else Translations.get_text("app_title", lang)
        self.root.title(f"{title} v{APP_VERSION}")

    def _get_font_size_value(self) -> int:
        """Return the configured base font size."""
        size_map = {
            FontSize.SMALL: 9,
            FontSize.MEDIUM: 11,
            FontSize.LARGE: 13,
            FontSize.EXTRA_LARGE: 15,
        }
        return size_map.get(self.settings.font_size, 11)

    def _get_font_scale_factor(self) -> float:
        """Return scale factor relative to the default medium size."""
        return self._get_font_size_value() / 11

    def _scale_font_size(self, size: int) -> int:
        """Scale a font size while keeping a reasonable minimum."""
        return max(7, int(round(size * self._get_font_scale_factor())))

    def _apply_widget_font(self, widget):
        """Apply the configured font scaling to a widget if it has a font option."""
        try:
            current_font = widget.cget("font")
        except tk.TclError:
            return

        if not current_font:
            return

        if not hasattr(widget, "_base_font_spec"):
            font_obj = tkfont.Font(font=current_font)
            widget._base_font_spec = {
                "family": font_obj.actual("family") or "Tahoma",
                "size": abs(font_obj.actual("size")) or 11,
                "weight": font_obj.actual("weight"),
                "slant": font_obj.actual("slant"),
            }

        spec = widget._base_font_spec
        font_parts = [spec["family"], self._scale_font_size(spec["size"])]
        if spec["weight"] == "bold":
            font_parts.append("bold")
        if spec["slant"] == "italic":
            font_parts.append("italic")

        try:
            widget.configure(font=tuple(font_parts))
        except tk.TclError:
            return

    def _apply_font_to_widget_tree(self, widget):
        """Apply font scaling to a widget and all of its children."""
        self._apply_widget_font(widget)
        for child in widget.winfo_children():
            self._apply_font_to_widget_tree(child)

    def _on_widget_map(self, event):
        """Scale fonts for widgets as they are displayed."""
        self._apply_widget_font(event.widget)

    def _apply_font_size(self):
        """Apply the configured font size to Tk named fonts and live widgets."""
        base_size = self._get_font_size_value()
        named_fonts = {
            "TkDefaultFont": base_size,
            "TkTextFont": base_size,
            "TkMenuFont": max(base_size - 1, 8),
            "TkHeadingFont": base_size,
            "TkCaptionFont": max(base_size - 1, 8),
            "TkSmallCaptionFont": max(base_size - 2, 7),
            "TkIconFont": base_size,
            "TkTooltipFont": max(base_size - 1, 8),
            "TkFixedFont": base_size,
        }

        for font_name, size in named_fonts.items():
            try:
                tkfont.nametofont(font_name).configure(size=size, family='Tahoma')
            except tk.TclError:
                continue

        self.root.option_add("*Font", ("Tahoma", base_size))
        self._apply_font_to_widget_tree(self.root)
    
    # ==========================================================================
    # SECTION: STYLING
    # ==========================================================================
    
    def _create_styles(self):
        """
        Configure application-wide styling with theme support.
        
        This method sets up ttk styles for consistent appearance
        across all widgets. It applies the current color theme.
        """
        # Get colors based on theme
        colors = ColorThemes.get_colors(self.settings.theme)
        
        # Create style object
        style = ttk.Style()
        
        # Try to use clam theme (more customizable)
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # =========================================================================
        # Button Styles
        # =========================================================================
        
        # Primary button style (main actions)
        style.configure(
            'Primary.TButton',
            font=('Tahoma', self._scale_font_size(11), 'bold'),
            padding=10,
            background=colors['primary'],
            foreground=colors['text_light']
        )
        
        # Secondary button style
        style.configure(
            'Secondary.TButton',
            font=('Tahoma', self._scale_font_size(10)),
            padding=8,
            background=colors['secondary'],
            foreground=colors['text_light']
        )
        
        # =========================================================================
        # Label Styles
        # =========================================================================
        
        # Title style
        style.configure(
            'Title.TLabel',
            font=('Tahoma', self._scale_font_size(18), 'bold'),
            foreground=colors['primary'],
            background=colors['background']
        )
        
        # Subtitle style
        style.configure(
            'Subtitle.TLabel',
            font=('Tahoma', self._scale_font_size(13), 'bold'),
            foreground=colors['secondary'],
            background=colors['background']
        )
        
        # =========================================================================
        # Treeview Styles
        # =========================================================================
        
        # Treeview style
        style.configure(
            'Treeview',
            font=('Tahoma', self._scale_font_size(10)),
            rowheight=max(22, self._scale_font_size(28)),
            background=colors['background'],
            foreground=colors['text']
        )
        
        # Treeview heading style
        style.configure(
            'Treeview.Heading',
            font=('Tahoma', self._scale_font_size(10), 'bold'),
            background=colors['primary'],
            foreground=colors['text_light']
        )
        
        # Store colors for dynamic updates
        self.colors = colors
    
    def _get_colors(self):
        """Get current theme colors."""
        return ColorThemes.get_colors(self.settings.theme)
    
    # ==========================================================================
    # SECTION: MENU
    # ==========================================================================
    
    def _create_menu(self):
        """
        Create the application menu bar.
        
        The menu includes:
        - File: Save/Load data, Exit
        - Settings: Volume, Theme, Language
        - Help: About, Video Guide
        """
        # Get current language
        lang = self.settings.language.value
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # =========================================================================
        # File Menu
        # =========================================================================
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=Translations.get_text("file", lang), menu=file_menu, font=('Tahoma', 10))
        file_menu.add_command(label=Translations.get_text("save_data", lang), command=self.save_data, font=('Tahoma', 10))
        file_menu.add_command(label=Translations.get_text("load_data", lang), command=self.load_data, font=('Tahoma', 10))
        file_menu.add_separator()
        file_menu.add_command(label=Translations.get_text("export_csv", lang), command=self.export_csv, font=('Tahoma', 10))
        file_menu.add_separator()
        file_menu.add_command(label=Translations.get_text("exit", lang), command=self.exit_app, font=('Tahoma', 10))
        
        # =========================================================================
        # Settings Menu
        # =========================================================================
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=Translations.get_text("settings", lang), menu=settings_menu, font=('Tahoma', 10))
        
        # Volume submenu
        volume_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=Translations.get_text("volume", lang), menu=volume_menu, font=('Tahoma', 10))
        volume_menu.add_command(label=Translations.get_text("increase_volume", lang), command=self.increase_volume)
        volume_menu.add_command(label=Translations.get_text("decrease_volume", lang), command=self.decrease_volume)
        volume_menu.add_separator()
        volume_menu.add_checkbutton(
            label=Translations.get_text("sound_enabled", lang),
            variable=tk.BooleanVar(value=self.settings.sound_enabled),
            command=self.toggle_sound
        )
        
        # Theme submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=Translations.get_text("color_theme", lang), menu=theme_menu, font=('Tahoma', 10))
        theme_menu.add_command(label=Translations.get_text("default_blue", lang), command=lambda: self.set_theme(ColorTheme.DEFAULT))
        theme_menu.add_command(label=Translations.get_text("high_contrast", lang), command=lambda: self.set_theme(ColorTheme.HIGH_CONTRAST))
        theme_menu.add_command(label=Translations.get_text("protanopia", lang), command=lambda: self.set_theme(ColorTheme.PROTANOPIA))
        theme_menu.add_command(label=Translations.get_text("deuteranopia", lang), command=lambda: self.set_theme(ColorTheme.DEUTERANOPIA))
        theme_menu.add_command(label=Translations.get_text("tritanopia", lang), command=lambda: self.set_theme(ColorTheme.TRITANOPIA))
        
        # Language submenu
        lang_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=Translations.get_text("language", lang), menu=lang_menu, font=('Tahoma', 10))
        lang_menu.add_command(label="English", command=lambda: self.set_language(Language.ENGLISH))
        lang_menu.add_command(label="العربية (Arabic)", command=lambda: self.set_language(Language.ARABIC))
        
        settings_menu.add_separator()
        settings_menu.add_command(label=Translations.get_text("set_logo", lang), command=self.set_logo)
        
        # =========================================================================
        # Help Menu
        # =========================================================================
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=Translations.get_text("help", lang), menu=help_menu, font=('Tahoma', 10))
        help_menu.add_command(label=Translations.get_text("video_tutorial", lang), command=self.show_video_guide)
        help_menu.add_separator()
        help_menu.add_command(label=Translations.get_text("about", lang), command=self.show_about)
    
    # ==========================================================================
    # SECTION: MAIN FRAME
    # ==========================================================================
    
    def _create_main_frame(self):
        """
        Create the main application frame with navigation buttons.
        
        The main frame includes:
        - Title header with logo
        - Navigation button grid
        - Status bar
        """
        colors = self._get_colors()
        lang = self.settings.language.value

        title_frame = tk.Frame(self.root, bg=colors['primary'], height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_text = self.settings.custom_title if self.settings.custom_title else Translations.get_text("app_title", lang)
        if self.settings.logo_path and os.path.exists(self.settings.logo_path):
            header_frame = tk.Frame(title_frame, bg=colors['primary'])
            header_frame.pack(expand=True)

            logo_shown = False
            if PIL_AVAILABLE:
                try:
                    img = Image.open(self.settings.logo_path)
                    img = img.resize((60, 60), Image.Resampling.LANCZOS)
                    self.logo_photo = ImageTk.PhotoImage(img)
                    logo_label = tk.Label(header_frame, image=self.logo_photo, bg=colors['primary'])
                    logo_label.pack(side=tk.LEFT, padx=(0, 12))
                    logo_shown = True
                except Exception:
                    logo_shown = False
            else:
                try:
                    # Tk fallback (works best with PNG/GIF when Pillow is unavailable)
                    self.logo_photo = tk.PhotoImage(file=self.settings.logo_path)
                    logo_label = tk.Label(header_frame, image=self.logo_photo, bg=colors['primary'])
                    logo_label.pack(side=tk.LEFT, padx=(0, 12))
                    logo_shown = True
                except Exception:
                    logo_shown = False

            title_label = tk.Label(
                header_frame,
                text=title_text,
                font=('Tahoma', 22, 'bold'),
                bg=colors['primary'],
                fg=colors['text_light']
            )
            title_label.pack(side=tk.LEFT)

            if not logo_shown:
                print("[LOG] Logo file exists but could not be rendered")
        else:
            title_label = tk.Label(
                title_frame,
                text=title_text,
                font=('Tahoma', 22, 'bold'),
                bg=colors['primary'],
                fg=colors['text_light']
            )
            title_label.pack(pady=25)

        buttons_frame = tk.Frame(self.root, bg=colors['background'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        buttons = [
            (Translations.get_text("manage_individuals", lang), self.individual_management, colors['danger']),
            (Translations.get_text("manage_teams", lang), self.team_management, colors['accent']),
            (Translations.get_text("manage_events", lang), self.event_management, colors['primary']),
            (Translations.get_text("register_participants", lang), self.registration_management, '#1abc9c'),
            (Translations.get_text("enter_results", lang), self.results_management, colors['warning']),
            (Translations.get_text("view_rankings", lang), self.rankings_view, colors['success']),
            (Translations.get_text("reports", lang), self.reports_view, colors['secondary']),
            (Translations.get_text("settings_btn", lang), self.settings_dialog, '#95a5a6'),
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=('Tahoma', 13, 'bold'),
                bg=color,
                fg=colors['text_light'],
                activebackground=color,
                activeforeground=colors['text_light'],
                relief=tk.FLAT,
                cursor='hand2',
                command=command,
                height=2
            )
            btn.grid(row=i//4, column=i%4, sticky='nsew', padx=8, pady=8)

        for col in range(4):
            buttons_frame.grid_columnconfigure(col, weight=1)
        for row in range(2):
            buttons_frame.grid_rowconfigure(row, weight=1)

        status_frame = tk.Frame(self.root, bg=colors['secondary'], height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text=Translations.get_text("ready", lang),
            font=('Tahoma', 9),
            bg=colors['secondary'],
            fg=colors['text_light']
        )
        self.status_label.pack(pady=5)

    # ==========================================================================
    # SECTION: UTILITY METHODS
    # ==========================================================================
    def _update_status(self, message: str):
        """
        Update the status bar message.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
        self.root.update()
    
    def _log_event(self, message: str):
        """
        Internal logging for audit trail and review.
        
        Args:
            message: Log message
        """
        print(f"[LOG] {message}")
        self._update_status(message)
    
    def _play_click_sound(self):
        """Play button click sound."""
        self.sound_manager.play_click()
    
    def _play_success_sound(self):
        """Play success sound."""
        self.sound_manager.play_success()
    
    def _load_last_data(self):
        """Load the most recently saved data if available."""
        latest_file = self.storage.get_latest_save_file()
        if latest_file:
            if messagebox.askyesno("Load Data", "Would you like to load the last saved data?"):
                if self.storage.load_from_json(latest_file):
                    messagebox.showinfo("Success", "Data loaded successfully")
                    self._log_event(f"Loaded data from: {latest_file}")
    
    def _prompt_video_guide(self):
        """Prompt user to watch video guide on first run."""
        if messagebox.askyesno(
            "Welcome!", 
            "Welcome to Championship Points Registration System v2.0!\n\n"
            "Would you like to watch a video tutorial on how to use this program?"
        ):
            self.show_video_guide()
    
    # ==========================================================================
    # SECTION: SETTINGS METHODS
    # ==========================================================================
    
    def increase_volume(self):
        """Increase volume by 10%."""
        self._play_click_sound()
        success, msg = self.service.increase_volume()
        self.settings = self.service.get_settings()
        self.sound_manager.set_volume(self.settings.volume)
        self._log_event(msg)
    
    def decrease_volume(self):
        """Decrease volume by 10%."""
        self._play_click_sound()
        success, msg = self.service.decrease_volume()
        self.settings = self.service.get_settings()
        self.sound_manager.set_volume(self.settings.volume)
        self._log_event(msg)
    
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self._play_click_sound()
        success, msg = self.service.toggle_sound()
        self.settings = self.service.get_settings()
        self.sound_manager.set_enabled(self.settings.sound_enabled)
        self._log_event(msg)
    
    def set_theme(self, theme: ColorTheme):
        """
        Set the color theme.
        
        Args:
            theme: ColorTheme to apply
        """
        self._play_click_sound()
        success, msg = self.service.set_theme(theme)
        if success:
            self.settings = self.service.get_settings()
            # Recreate styles with new theme
            self._create_styles()
            # Recreate main frame with new colors
            for widget in self.root.winfo_children():
                widget.destroy()
            self._create_menu()
            self._create_main_frame()
        self._log_event(msg)
    
    def set_language(self, language: Language):
        """
        Set the UI language and refresh the interface.
        
        Args:
            language: Language to apply
        """
        self._play_click_sound()
        success, msg = self.service.set_language(language)
        if success:
            self.settings = self.service.get_settings()
            
            # Get current language
            current_lang = self.settings.language.value
            
            # Show message about language change
            lang_name = "العربية" if current_lang == "arabic" else "English"
            messagebox.showinfo(
                Translations.get_text("language_changed", current_lang),
                Translations.get_text("language_changed_message", current_lang).format(lang_name)
            )
            
            # Refresh the entire UI with new language
            self._refresh_ui()
            
        self._log_event(msg)
    
    def _refresh_ui(self):
        """
        Refresh the entire UI with current language and theme.
        
        This method rebuilds the main window to apply language changes.
        """
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Update title after language/theme changes
        self._update_window_title()
        self._apply_font_size()
        
        # Recreate styles
        self._create_styles()
        
        # Recreate menu
        self._create_menu()
        
        # Recreate main frame
        self._create_main_frame()
        
        # Log the refresh
        self._log_event(f"UI refreshed with language: {self.settings.language.value}")
    
    def set_logo(self):
        """
        Set custom logo image.
        
        Opens file dialog to select an image file.
        """
        self._play_click_sound()
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            success, msg = self.service.set_logo_path(file_path)
            if success:
                self.settings = self.service.get_settings()
                messagebox.showinfo("Success", "Logo updated successfully!")
                if not PIL_AVAILABLE and not file_path.lower().endswith((".png", ".gif")):
                    messagebox.showwarning(
                        "Warning",
                        "This image type may not display without Pillow. Use PNG/GIF or install Pillow."
                    )
                self._refresh_ui()
            else:
                messagebox.showerror("Error", msg)

    def set_video(self):
        """Set custom video tutorial path."""
        self._play_click_sound()
        lang = self.settings.language.value
        file_path = filedialog.askopenfilename(
            title=Translations.get_text("set_video_path", lang),
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            success, msg = self.service.set_video_path(file_path)
            if success:
                self.settings = self.service.get_settings()
                messagebox.showinfo(Translations.get_text("success", lang), msg)
            else:
                messagebox.showerror(Translations.get_text("error", lang), msg)

    def set_font_size(self, font_size: FontSize):
        """Update the application font size and refresh the UI."""
        self._play_click_sound()
        success, msg = self.service.set_font_size(font_size)
        if success:
            self.settings = self.service.get_settings()
            self._refresh_ui()
        self._log_event(msg)

    def set_custom_title(self):
        """Prompt for a custom window title and apply it immediately."""
        self._play_click_sound()
        lang = self.settings.language.value
        value = simpledialog.askstring(
            Translations.get_text("custom_title_title", lang),
            Translations.get_text("set_custom_title", lang),
            initialvalue=self.settings.custom_title or "",
            parent=self.root
        )
        if value is None:
            return

        success, msg = self.service.set_custom_title(value)
        if success:
            self.settings = self.service.get_settings()
            self._update_window_title()
            self._refresh_ui()
        self._log_event(msg)
    
    def show_video_guide(self):
        """
        Show video tutorial/guide dialog.
        
        This displays a dialog with instructions on how to use
        the program. It marks the video as watched.
        """
        self._play_click_sound()
        
        # Mark as watched
        self.service.mark_video_watched()
        self.settings = self.service.get_settings()

        # Play configured video if available
        video_path = self.settings.video_path
        if video_path and os.path.exists(video_path):
            try:
                webbrowser.open(f"file://{os.path.abspath(video_path)}")
            except Exception:
                pass
        
        # Show video guide dialog
        guide_text = """
VIDEO TUTORIAL GUIDE
Championship Points Registration System

GETTING STARTED:
   1. Add individual participants (Name, Age, Level)
   2. Add teams (minimum 5 members, maximum 10)
   3. Create events (Individual or Group type)
   4. Register participants in events
   5. Enter competition results
   6. View rankings and reports

SETTINGS:
   - Volume: Control sound effects
   - Theme: Choose color theme for accessibility
   - Language: Switch between English and Arabic
   - Logo: Set custom logo image
   - Video: Set a custom tutorial video file

TIPS:
   - Save your data regularly
   - Use high contrast theme if you have vision issues
   - Export data to CSV for external analysis
   - Check reports for tournament statistics

For more help, contact support.
        """
        
        # Create guide window
        guide_win = tk.Toplevel(self.root)
        guide_win.title("Video Tutorial Guide")
        guide_win.geometry("600x500")
        
        # Guide text
        text_widget = tk.Text(
            guide_win,
            font=('Courier New', 10),
            wrap=tk.WORD,
            bg='#f5f5f5'
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', guide_text)
        text_widget.config(state='disabled')
        
        # Close button
        tk.Button(
            guide_win,
            text="Close",
            font=('Tahoma', 11),
            command=guide_win.destroy
        ).pack(pady=10)
    
    def settings_dialog(self):
        """
        Open settings dialog.

        This is a comprehensive settings window where users can
        adjust all application settings in one place.
        """
        self._play_click_sound()
        lang = self.settings.language.value

        win = tk.Toplevel(self.root)
        win.title(Translations.get_text("settings_title", lang))
        win.geometry("520x620")

        colors = self._get_colors()

        # Scrollable layout for settings content
        container = tk.Frame(win, bg=colors['background'])
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        content = tk.Frame(canvas, bg=colors['background'])

        canvas.create_window((0, 0), window=content, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_content_configure(_event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_wheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif getattr(event, 'num', None) == 4:
                canvas.yview_scroll(-1, "units")
            elif getattr(event, 'num', None) == 5:
                canvas.yview_scroll(1, "units")

        content.bind("<Configure>", on_content_configure)
        canvas.bind_all("<MouseWheel>", on_wheel)
        canvas.bind_all("<Button-4>", on_wheel)
        canvas.bind_all("<Button-5>", on_wheel)
        win.bind("<Destroy>", lambda _e: (canvas.unbind_all("<MouseWheel>"), canvas.unbind_all("<Button-4>"), canvas.unbind_all("<Button-5>")))

        tk.Label(
            content,
            text=Translations.get_text("application_settings", lang),
            font=('Tahoma', 16, 'bold'),
            fg=colors['primary'],
            bg=colors['background']
        ).pack(pady=20)

        volume_frame = tk.LabelFrame(content, text=Translations.get_text("volume_control", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        volume_frame.pack(fill=tk.X, padx=20, pady=10)

        volume_var = tk.DoubleVar(value=self.settings.volume * 100)

        def on_volume_change(val):
            vol = float(val) / 100
            self.service.set_volume(vol)
            self.settings = self.service.get_settings()
            self.sound_manager.set_volume(vol)

        tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=volume_var,
            command=on_volume_change,
            label=Translations.get_text("volume_percent", lang),
            font=('Tahoma', 10)
        ).pack(fill=tk.X, pady=5)

        sound_var = tk.BooleanVar(value=self.settings.sound_enabled)

        def on_sound_toggle():
            self.service.toggle_sound()
            self.settings = self.service.get_settings()
            self.sound_manager.set_enabled(self.settings.sound_enabled)

        tk.Checkbutton(
            volume_frame,
            text=Translations.get_text("enable_sound_effects", lang),
            variable=sound_var,
            command=on_sound_toggle,
            font=('Tahoma', 10)
        ).pack(pady=5)

        theme_frame = tk.LabelFrame(content, text=Translations.get_text("color_theme_title", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        theme_frame.pack(fill=tk.X, padx=20, pady=10)

        theme_var = tk.StringVar(value=self.settings.theme.value)
        themes = [
            (Translations.get_text("default_blue", lang), "default"),
            (Translations.get_text("high_contrast", lang), "high_contrast"),
            (Translations.get_text("protanopia", lang), "protanopia"),
            (Translations.get_text("deuteranopia", lang), "deuteranopia"),
            (Translations.get_text("tritanopia", lang), "tritanopia")
        ]

        for text, value in themes:
            tk.Radiobutton(
                theme_frame,
                text=text,
                variable=theme_var,
                value=value,
                font=('Tahoma', 10),
                command=lambda v=value: self.set_theme(ColorTheme(v))
            ).pack(anchor=tk.W, pady=2)

        lang_frame = tk.LabelFrame(content, text=Translations.get_text("language_title", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        lang_frame.pack(fill=tk.X, padx=20, pady=10)

        lang_var = tk.StringVar(value=self.settings.language.value)

        tk.Radiobutton(
            lang_frame,
            text="English",
            variable=lang_var,
            value="english",
            font=('Tahoma', 10),
            command=lambda: self.set_language(Language.ENGLISH)
        ).pack(anchor=tk.W, pady=2)

        tk.Radiobutton(
            lang_frame,
            text="العربية",
            variable=lang_var,
            value="arabic",
            font=('Tahoma', 10),
            command=lambda: self.set_language(Language.ARABIC)
        ).pack(anchor=tk.W, pady=2)

        logo_frame = tk.LabelFrame(content, text=Translations.get_text("logo_title", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        logo_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            logo_frame,
            text=Translations.get_text("choose_logo_image", lang),
            command=self.set_logo,
            font=('Tahoma', 10)
        ).pack(pady=5)

        if self.settings.logo_path:
            tk.Label(
                logo_frame,
                text=f"{Translations.get_text('current', lang)} {os.path.basename(self.settings.logo_path)}",
                font=('Tahoma', 9),
                fg='gray'
            ).pack()

        font_frame = tk.LabelFrame(content, text=Translations.get_text("font_size_title", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        font_frame.pack(fill=tk.X, padx=20, pady=10)

        font_size_var = tk.StringVar(value=self.settings.font_size.value)
        font_options = [
            (Translations.get_text("font_small", lang), FontSize.SMALL),
            (Translations.get_text("font_medium", lang), FontSize.MEDIUM),
            (Translations.get_text("font_large", lang), FontSize.LARGE),
            (Translations.get_text("font_extra_large", lang), FontSize.EXTRA_LARGE),
        ]

        for label, value in font_options:
            tk.Radiobutton(
                font_frame,
                text=label,
                variable=font_size_var,
                value=value.value,
                font=('Tahoma', 10),
                command=lambda v=value: self.set_font_size(v)
            ).pack(anchor=tk.W, pady=2)

        title_frame = tk.LabelFrame(content, text=Translations.get_text("custom_title_title", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        title_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            title_frame,
            text=Translations.get_text("set_custom_title", lang),
            command=self.set_custom_title,
            font=('Tahoma', 10)
        ).pack(pady=5)

        current_title = self.settings.custom_title or Translations.get_text("app_title", lang)
        tk.Label(
            title_frame,
            text=f"{Translations.get_text('current', lang)} {current_title}",
            font=('Tahoma', 9),
            fg='gray'
        ).pack()

        video_frame = tk.LabelFrame(content, text=Translations.get_text("video_path", lang), font=('Tahoma', 12, 'bold'), padx=10, pady=10)
        video_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            video_frame,
            text=Translations.get_text("set_video_path", lang),
            command=self.set_video,
            font=('Tahoma', 10)
        ).pack(pady=5)

        if self.settings.video_path:
            tk.Label(
                video_frame,
                text=f"{Translations.get_text('current', lang)} {os.path.basename(self.settings.video_path)}",
                font=('Tahoma', 9),
                fg='gray'
            ).pack()

        tk.Button(
            content,
            text=Translations.get_text("close", lang),
            font=('Tahoma', 11, 'bold'),
            command=win.destroy,
            bg=colors['primary'],
            fg='white'
        ).pack(pady=20)
    def individual_management(self):
        """
        Open individual participant management window.
        
        This window allows users to:
        - Add new individual participants
        - Edit existing participants
        - Delete participants
        - View participant list
        """
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Manage Individual Participants")
        win.geometry("900x550")
        
        colors = self._get_colors()
        
        # Top buttons frame
        top_frame = tk.Frame(win, bg=colors['background'])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Action buttons
        tk.Button(
            top_frame,
            text="Add New",
            font=('Tahoma', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            command=lambda: self.add_individual(win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Edit",
            font=('Tahoma', 11),
            bg=colors['primary'],
            fg='white',
            command=lambda: self.edit_individual(tree, win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Delete",
            font=('Tahoma', 11),
            bg=colors['danger'],
            fg='white',
            command=lambda: self.delete_individual(tree, win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Refresh",
            font=('Tahoma', 11),
            command=lambda: self.refresh_individuals(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        # Data table
        columns = ('ID', 'Name', 'Age', 'Level', 'Points', 'Events')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=18)
        
        # Configure columns
        tree.column('ID', width=80)
        tree.column('Name', width=180)
        tree.column('Age', width=60)
        tree.column('Level', width=100)
        tree.column('Points', width=80)
        tree.column('Events', width=60)
        
        for col in columns:
            tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0,10))
        
        # Load data
        self.refresh_individuals(tree)
    
    def refresh_individuals(self, tree):
        """Refresh the individuals list in the table."""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Get all individuals
        individuals = self.service.get_all_individuals()
        
        # Populate table
        for ind in individuals:
            tree.insert('', tk.END, values=(
                ind.participant_id,
                ind.name,
                ind.age or '-',
                ind.level or '-',
                ind.total_points,
                ind.events_count
            ))
        
        self._log_event(f"Refreshed individuals list: {len(individuals)} entries")
    
    def add_individual(self, parent):
        """
        Add a new individual participant.
        
        Opens a dialog to enter participant details.
        """
        # Create dialog
        win = tk.Toplevel(parent)
        win.title("Add Individual Participant")
        win.geometry("400x320")
        
        colors = self._get_colors()
        
        # Form fields
        tk.Label(win, text="Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.pack(pady=5)
        name_entry.focus()
        
        tk.Label(win, text="Age:", font=('Tahoma', 11)).pack(pady=5)
        age_entry = tk.Entry(win, font=('Tahoma', 12))
        age_entry.pack(pady=5)
        
        tk.Label(win, text="Level:", font=('Tahoma', 11)).pack(pady=5)
        level_entry = tk.Entry(win, font=('Tahoma', 12))
        level_entry.pack(pady=5)
        
        def save():
            """Save the new individual."""
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            # Parse age
            age = None
            if age_entry.get().strip():
                try:
                    age = int(age_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Error", "Age must be a number")
                    return
            
            # Get level
            level = level_entry.get().strip() or None
            
            # Add individual
            success, message, _ = self.service.add_individual(name, age, level)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", message)
                self._log_event(f"Added individual: {name}")
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Save button
        tk.Button(
            win,
            text="Save",
            font=('Tahoma', 12, 'bold'),
            bg=colors['success'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    def edit_individual(self, tree, parent):
        """
        Edit an existing individual participant.
        
        Opens a dialog to edit participant details.
        """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a participant to edit")
            return
        
        # Get selected item
        item = tree.item(selected[0])
        participant_id = item['values'][0]
        
        # Get individual data
        individuals = self.service.get_all_individuals()
        ind = next((i for i in individuals if i.participant_id == participant_id), None)
        
        if not ind:
            messagebox.showerror("Error", "Participant not found")
            return
        
        # Edit window
        win = tk.Toplevel(parent)
        win.title("Edit Participant")
        win.geometry("400x280")
        
        colors = self._get_colors()
        
        # Form fields
        tk.Label(win, text="Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.insert(0, ind.name)
        name_entry.pack(pady=5)
        
        tk.Label(win, text="Age:", font=('Tahoma', 11)).pack(pady=5)
        age_entry = tk.Entry(win, font=('Tahoma', 12))
        age_entry.insert(0, str(ind.age) if ind.age else '')
        age_entry.pack(pady=5)
        
        tk.Label(win, text="Level:", font=('Tahoma', 11)).pack(pady=5)
        level_entry = tk.Entry(win, font=('Tahoma', 12))
        level_entry.insert(0, ind.level or '')
        level_entry.pack(pady=5)
        
        def save():
            """Save changes."""
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            # Parse age
            age = None
            if age_entry.get().strip():
                try:
                    age = int(age_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Error", "Age must be a number")
                    return
            
            # Get level
            level = level_entry.get().strip() or None
            
            # Update individual
            success, message = self.service.update_individual(
                ind.participant_id, name, age, level
            )
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", "Updated successfully")
                self._log_event(f"Edited individual: {name}")
                self.refresh_individuals(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Save button
        tk.Button(
            win,
            text="Save Changes",
            font=('Tahoma', 12, 'bold'),
            bg=colors['primary'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    def delete_individual(self, tree, parent):
        """
        Delete an individual participant.
        
        Confirms deletion and removes the participant.
        """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a participant to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this participant?"):
            item = tree.item(selected[0])
            participant_id = item['values'][0]
            
            success, message = self.service.delete_individual(participant_id, confirm=True)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", "Deleted successfully")
                self._log_event("Deleted individual participant")
                self.refresh_individuals(tree)
            else:
                messagebox.showerror("Error", message)
    
    # ==========================================================================
    # SECTION: TEAM MANAGEMENT
    # ==========================================================================
    
    def team_management(self):
        """
        Open team management window.
        
        This window allows users to:
        - Add new teams
        - Edit team names
        - View team members
        - Delete teams
        """
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Manage Teams")
        win.geometry("900x550")
        
        colors = self._get_colors()
        
        # Buttons frame
        top_frame = tk.Frame(win, bg=colors['background'])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            top_frame,
            text="Add Team",
            font=('Tahoma', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            command=lambda: self.add_team(win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Edit Name",
            font=('Tahoma', 11),
            bg=colors['primary'],
            fg='white',
            command=lambda: self.edit_team_name(self.teams_tree, win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="View Members",
            font=('Tahoma', 11),
            command=lambda: self.show_team_members()
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Delete",
            font=('Tahoma', 11),
            bg=colors['danger'],
            fg='white',
            command=lambda: self.delete_team(self.teams_tree, win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Refresh",
            font=('Tahoma', 11),
            command=lambda: self.refresh_teams(self.teams_tree)
        ).pack(side=tk.LEFT, padx=5)
        
        # Table
        columns = ('ID', 'Team Name', 'Members', 'Points', 'Events')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=18)
        
        tree.column('ID', width=80)
        tree.column('Team Name', width=200)
        tree.column('Members', width=80)
        tree.column('Points', width=80)
        tree.column('Events', width=60)
        
        for col in columns:
            tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0,10))
        
        # Store tree reference
        self.teams_tree = tree
        
        self.refresh_teams(tree)
    
    def refresh_teams(self, tree):
        """Refresh the teams list."""
        for item in tree.get_children():
            tree.delete(item)
        
        teams = self.service.get_all_teams()
        for team in teams:
            tree.insert('', tk.END, values=(
                team.team_id,
                team.name,
                len(team.members),
                team.total_points,
                team.events_count
            ))
        self._log_event(f"Refreshed teams list: {len(teams)} entries")
    
    def add_team(self, parent):
        """Add a new team."""
        win = tk.Toplevel(parent)
        win.title("Add New Team")
        win.geometry("450x420")
        
        colors = self._get_colors()
        
        tk.Label(win, text="Team Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.pack(pady=5)
        name_entry.focus()
        
        tk.Label(win, text="Member Names (one per line):", font=('Tahoma', 11)).pack(pady=5)
        members_text = tk.Text(win, font=('Tahoma', 11), height=12, width=40)
        members_text.pack(pady=5)
        
        tk.Label(win, text="(Enter at least 5 members, max 10)", font=('Tahoma', 9), fg='gray').pack()
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Team name is required")
                return
            
            members = members_text.get('1.0', tk.END).strip().split('\n')
            members = [m.strip() for m in members if m.strip()]
            
            if len(members) < 5:
                messagebox.showerror("Error", "Must enter at least 5 members")
                return
            
            success, message, _ = self.service.add_team(name, members)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", message)
                self._log_event(f"Added team: {name} with {len(members)} members")
                if self.teams_tree:
                    self.refresh_teams(self.teams_tree)
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Save Team",
            font=('Tahoma', 12, 'bold'),
            bg=colors['success'],
            fg='white',
            command=save
        ).pack(pady=15)
    
    def edit_team_name(self, tree, parent):
        """
        Edit a team's name.
        
        This is the new feature requested - editing team names.
        """
        if not tree:
            messagebox.showerror("Error", "Teams list not available")
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a team to edit")
            return
        
        item = tree.item(selected[0])
        team_id = item['values'][0]
        current_name = item['values'][1]
        
        # Get team
        team = self.service.get_team_details(team_id)
        if not team:
            messagebox.showerror("Error", "Team not found")
            return
        
        # Edit window
        win = tk.Toplevel(parent)
        win.title("Edit Team Name")
        win.geometry("400x180")
        
        colors = self._get_colors()
        
        tk.Label(win, text="Team Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.insert(0, current_name)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def save():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Team name is required")
                return
            
            success, message = self.service.update_team_name(team_id, new_name)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", "Team name updated successfully")
                self._log_event(f"Updated team name: {current_name} -> {new_name}")
                self.refresh_teams(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Save Changes",
            font=('Tahoma', 12, 'bold'),
            bg=colors['primary'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    def show_team_members(self):
        """Display team members."""
        tree = self.teams_tree
        if not tree:
            messagebox.showerror("Error", "Teams list not available")
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a team to view members")
            return
        
        item = tree.item(selected[0])
        team_name = item['values'][1]
        
        # Find team
        teams = self.service.get_all_teams()
        team = None
        for t in teams:
            if t.name == team_name:
                team = t
                break
        
        if not team:
            messagebox.showerror("Error", "Team not found")
            return
        
        if not team.members or len(team.members) == 0:
            messagebox.showerror("Error", f"Team '{team.name}' has no members")
            return
        
        # Display members window
        win = tk.Toplevel(self.root)
        win.title(f"Team {team.name} Members")
        win.geometry("350x450")
        
        colors = self._get_colors()
        
        tk.Label(
            win,
            text=f"Team: {team.name}",
            font=('Tahoma', 14, 'bold'),
            fg=colors['primary']
        ).pack(pady=10)
        
        tk.Label(
            win,
            text=f"Total Members: {len(team.members)}",
            font=('Tahoma', 10),
            fg='gray'
        ).pack()
        
        # Members list
        members_frame = tk.Frame(win)
        members_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for i, member in enumerate(team.members, 1):
            tk.Label(
                members_frame,
                text=f"{i}. {member.name}" + (f" ({member.role})" if member.role else ""),
                font=('Tahoma', 12)
            ).pack(anchor=tk.W, pady=3)
        
        tk.Button(
            win,
            text="Close",
            font=('Tahoma', 11),
            command=win.destroy
        ).pack(pady=10)
        
        self._log_event(f"Viewed members for team: {team.name}")
    
    def delete_team(self, tree, parent):
        """Delete a team."""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a team to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this team?"):
            item = tree.item(selected[0])
            team_id = item['values'][0]
            
            success, message = self.service.delete_team(team_id, confirm=True)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", "Deleted successfully")
                self._log_event("Deleted team")
                self.refresh_teams(tree)
            else:
                messagebox.showerror("Error", message)
    
    # ==========================================================================
    # SECTION: EVENT MANAGEMENT
    # ==========================================================================
    
    def event_management(self):
        """
        Open event management window.
        
        This window allows users to:
        - Add new events
        - Edit event names
        - Delete events
        - View event list
        """
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Manage Events")
        win.geometry("900x550")
        
        colors = self._get_colors()
        
        # Buttons frame
        top_frame = tk.Frame(win, bg=colors['background'])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            top_frame,
            text="Add Event",
            font=('Tahoma', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            command=lambda: self.add_event(win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Edit Name",
            font=('Tahoma', 11),
            bg=colors['primary'],
            fg='white',
            command=lambda: self.edit_event_name(self.events_tree, win)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            top_frame,
            text="Refresh",
            font=('Tahoma', 11),
            command=lambda: self.refresh_events(self.events_tree)
        ).pack(side=tk.LEFT, padx=5)
        
        # Table
        columns = ('ID', 'Name', 'Type', 'Category', 'Status', 'Max')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=18)
        
        tree.column('ID', width=80)
        tree.column('Name', width=200)
        tree.column('Type', width=80)
        tree.column('Category', width=100)
        tree.column('Status', width=80)
        tree.column('Max', width=60)
        
        for col in columns:
            tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0,10))
        
        # Store tree reference
        self.events_tree = tree
        
        self.refresh_events(tree)
    
    def refresh_events(self, tree):
        """Refresh the events list."""
        for item in tree.get_children():
            tree.delete(item)
        
        events = self.service.get_all_events()
        for event in events:
            event_type = "Individual" if event.event_type == EventType.INDIVIDUAL else "Group"
            category = "Sports" if event.category == EventCategory.SPORTS else "Academic"
            status = "Open" if event.status == EventStatus.OPEN else "Completed"
            
            tree.insert('', tk.END, values=(
                event.event_id,
                event.name,
                event_type,
                category,
                status,
                event.max_participants
            ))
        self._log_event(f"Refreshed events list: {len(events)} entries")
    
    def add_event(self, parent):
        """Add a new event."""
        win = tk.Toplevel(parent)
        win.title("Add New Event")
        win.geometry("420x400")
        
        colors = self._get_colors()
        
        tk.Label(win, text="Event Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.pack(pady=5)
        name_entry.focus()
        
        tk.Label(win, text="Event Type:", font=('Tahoma', 11)).pack(pady=5)
        type_var = tk.StringVar(value="individual")
        tk.Radiobutton(win, text="Individual", variable=type_var, value="individual").pack()
        tk.Radiobutton(win, text="Group (Team)", variable=type_var, value="group").pack()
        
        tk.Label(win, text="Category:", font=('Tahoma', 11)).pack(pady=5)
        cat_var = tk.StringVar(value="sports")
        tk.Radiobutton(win, text="Sports", variable=cat_var, value="sports").pack()
        tk.Radiobutton(win, text="Academic", variable=cat_var, value="academic").pack()
        
        tk.Label(win, text="Max Participants:", font=('Tahoma', 11)).pack(pady=5)
        max_entry = tk.Entry(win, font=('Tahoma', 12))
        max_entry.insert(0, "20")
        max_entry.pack(pady=5)
        
        single_var = tk.BooleanVar(value=False)
        tk.Checkbutton(win, text="Single event only (one event per participant)", variable=single_var).pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Event name is required")
                return
            
            event_type = EventType.INDIVIDUAL if type_var.get() == "individual" else EventType.GROUP
            category = EventCategory.SPORTS if cat_var.get() == "sports" else EventCategory.ACADEMIC
            
            try:
                max_part = int(max_entry.get().strip()) if max_entry.get().strip() else 20
            except ValueError:
                max_part = 20
            
            success, message, _ = self.service.add_event(
                name, event_type, category, max_part, single_var.get()
            )
            
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", message)
                self._log_event(f"Added event: {name}")
                if self.events_tree:
                    self.refresh_events(self.events_tree)
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Save",
            font=('Tahoma', 12, 'bold'),
            bg=colors['success'],
            fg='white',
            command=save
        ).pack(pady=15)
    
    def edit_event_name(self, tree, parent):
        """
        Edit an event's name.
        
        This is the new feature requested - editing event names.
        """
        if not tree:
            messagebox.showerror("Error", "Events list not available")
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an event to edit")
            return
        
        item = tree.item(selected[0])
        event_id = item['values'][0]
        current_name = item['values'][1]
        
        # Edit window
        win = tk.Toplevel(parent)
        win.title("Edit Event Name")
        win.geometry("400x180")
        
        colors = self._get_colors()
        
        tk.Label(win, text="Event Name:", font=('Tahoma', 11)).pack(pady=5)
        name_entry = tk.Entry(win, font=('Tahoma', 12))
        name_entry.insert(0, current_name)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def save():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Event name is required")
                return
            
            success, message = self.service.update_event_name(event_id, new_name)
            if success:
                self._play_success_sound()
                messagebox.showinfo("Success", "Event name updated successfully")
                self._log_event(f"Updated event name: {current_name} -> {new_name}")
                self.refresh_events(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Save Changes",
            font=('Tahoma', 12, 'bold'),
            bg=colors['primary'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    # ==========================================================================
    # SECTION: REGISTRATION MANAGEMENT
    # ==========================================================================
    
    def registration_management(self):
        """Open participant registration window."""
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Register Participants")
        win.geometry("650x450")
        
        colors = self._get_colors()
        
        # Title
        tk.Label(
            win,
            text="Select Registration Type:",
            font=('Tahoma', 14, 'bold'),
            fg=colors['primary']
        ).pack(pady=30)
        
        # Registration buttons
        tk.Button(
            win,
            text="Register Individual in Individual Event",
            font=('Tahoma', 12),
            bg=colors['danger'],
            fg='white',
            height=2,
            command=lambda: self.register_individual(win)
        ).pack(fill=tk.X, padx=50, pady=10)
        
        tk.Button(
            win,
            text="Register Team in Group Event",
            font=('Tahoma', 12),
            bg=colors['accent'],
            fg='white',
            height=2,
            command=lambda: self.register_team(win)
        ).pack(fill=tk.X, padx=50, pady=10)
    
    def register_individual(self, parent):
        """Register an individual participant in an event."""
        win = tk.Toplevel(parent)
        win.title("Register Individual")
        win.geometry("500x350")
        
        colors = self._get_colors()
        
        # Select individual
        tk.Label(win, text="Select Individual:", font=('Tahoma', 11)).pack(pady=5)
        
        individuals = self.service.get_all_individuals()
        ind_names = [ind.name for ind in individuals]
        
        if not ind_names:
            messagebox.showwarning("Warning", "No individuals registered")
            win.destroy()
            return
        
        ind_var = tk.StringVar()
        ind_combo = ttk.Combobox(win, textvariable=ind_var, values=ind_names, font=('Tahoma', 11))
        ind_combo.pack(pady=5)
        
        # Select event
        tk.Label(win, text="Select Event (Individual):", font=('Tahoma', 11)).pack(pady=5)
        
        events = self.service.get_events_by_type(EventType.INDIVIDUAL)
        event_names = [e.name for e in events]
        
        if not event_names:
            messagebox.showwarning("Warning", "No individual events available")
            win.destroy()
            return
        
        event_var = tk.StringVar()
        event_combo = ttk.Combobox(win, textvariable=event_var, values=event_names, font=('Tahoma', 11))
        event_combo.pack(pady=5)
        
        def save():
            ind_name = ind_var.get()
            event_name = event_var.get()
            
            if not ind_name or not event_name:
                messagebox.showerror("Error", "Select individual and event")
                return
            
            # Find IDs
            ind = next((i for i in individuals if i.name == ind_name), None)
            event = next((e for e in events if e.name == event_name), None)
            
            if ind and event:
                success, message = self.service.register_participant(
                    ind.participant_id, ParticipantType.INDIVIDUAL, event.event_id
                )
                if success:
                    self._play_success_sound()
                    messagebox.showinfo("Success", message)
                    self._log_event(f"Registered {ind_name} in {event_name}")
                    win.destroy()
                else:
                    messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Register",
            font=('Tahoma', 12, 'bold'),
            bg=colors['success'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    def register_team(self, parent):
        """Register a team in a group event."""
        win = tk.Toplevel(parent)
        win.title("Register Team")
        win.geometry("500x350")
        
        colors = self._get_colors()
        
        # Select team
        tk.Label(win, text="Select Team:", font=('Tahoma', 11)).pack(pady=5)
        
        teams = self.service.get_all_teams()
        team_names = [t.name for t in teams]
        
        if not team_names:
            messagebox.showwarning("Warning", "No teams registered")
            win.destroy()
            return
        
        team_var = tk.StringVar()
        team_combo = ttk.Combobox(win, textvariable=team_var, values=team_names, font=('Tahoma', 11))
        team_combo.pack(pady=5)
        
        # Select group event
        tk.Label(win, text="Select Event (Group):", font=('Tahoma', 11)).pack(pady=5)
        
        events = self.service.get_events_by_type(EventType.GROUP)
        event_names = [e.name for e in events]
        
        if not event_names:
            messagebox.showwarning("Warning", "No group events available")
            win.destroy()
            return
        
        event_var = tk.StringVar()
        event_combo = ttk.Combobox(win, textvariable=event_var, values=event_names, font=('Tahoma', 11))
        event_combo.pack(pady=5)
        
        def save():
            team_name = team_var.get()
            event_name = event_var.get()
            
            if not team_name or not event_name:
                messagebox.showerror("Error", "Select team and event")
                return
            
            team = next((t for t in teams if t.name == team_name), None)
            event = next((e for e in events if e.name == event_name), None)
            
            if team and event:
                success, message = self.service.register_participant(
                    team.team_id, ParticipantType.TEAM, event.event_id
                )
                if success:
                    self._play_success_sound()
                    messagebox.showinfo("Success", message)
                    self._log_event(f"Registered team {team_name} in {event_name}")
                    win.destroy()
                else:
                    messagebox.showerror("Error", message)
        
        tk.Button(
            win,
            text="Register",
            font=('Tahoma', 12, 'bold'),
            bg=colors['success'],
            fg='white',
            command=save
        ).pack(pady=20)
    
    # ==========================================================================
    # SECTION: RESULTS MANAGEMENT
    # ==========================================================================
    
    def results_management(self):
        """Open results entry window."""
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Enter Results")
        win.geometry("650x450")
        
        colors = self._get_colors()
        
        tk.Label(
            win,
            text="Select Event:",
            font=('Tahoma', 12, 'bold')
        ).pack(pady=15)
        
        events = self.service.get_all_events()
        event_names = [e.name for e in events]
        
        if not event_names:
            messagebox.showwarning("Warning", "No events available")
            win.destroy()
            return
        
        event_var = tk.StringVar()
        event_combo = ttk.Combobox(
            win,
            textvariable=event_var,
            values=event_names,
            font=('Tahoma', 11),
            width=35
        )
        event_combo.pack(pady=10)
        
        def show_registrations():
            event_name = event_var.get()
            if not event_name:
                return
            
            event = next((e for e in events if e.name == event_name), None)
            if not event:
                return
            
            # Results entry window
            win2 = tk.Toplevel(win)
            win2.title(f"Results: {event.name}")
            win2.geometry("550x450")
            
            regs = self.service.get_event_registrations(event.event_id)
            
            if not regs:
                messagebox.showwarning("Warning", "No participants registered")
                return
            
            tk.Label(
                win2,
                text=f"Enter rank for each participant in: {event.name}",
                font=('Tahoma', 11)
            ).pack(pady=10)
            
            for reg in regs:
                frame = tk.Frame(win2)
                frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Get participant name
                if reg.participant_type == ParticipantType.INDIVIDUAL:
                    ind = self.storage.get_individual(reg.participant_id)
                    name = ind.name if ind else "Unknown"
                else:
                    team = self.storage.get_team(reg.participant_id)
                    name = team.name if team else "Unknown"
                
                tk.Label(frame, text=name, font=('Tahoma', 10), width=28).pack(side=tk.LEFT)
                
                rank_entry = tk.Entry(frame, font=('Tahoma', 10), width=10)
                rank_entry.pack(side=tk.LEFT, padx=5)
                
                # Store entry references
                frame.rank_entry = rank_entry
                frame.participant_id = reg.participant_id
                frame.participant_type = reg.participant_type
            
            def save_results():
                results_count = 0
                for child in win2.winfo_children():
                    if isinstance(child, tk.Frame) and hasattr(child, 'rank_entry'):
                        try:
                            rank = int(child.rank_entry.get())
                            success, msg = self.service.enter_result(
                                event.event_id,
                                child.participant_id,
                                child.participant_type,
                                rank
                            )
                            if success:
                                results_count += 1
                        except ValueError:
                            pass
                
                if results_count > 0:
                    self._play_success_sound()
                messagebox.showinfo("Success", f"Results saved: {results_count} entries")
                self._log_event(f"Entered results for event: {event.name}")
                win2.destroy()
            
            tk.Button(
                win2,
                text="Save Results",
                font=('Tahoma', 11, 'bold'),
                bg=colors['success'],
                fg='white',
                command=save_results
            ).pack(pady=15)
        
        tk.Button(
            win,
            text="Continue",
            font=('Tahoma', 11),
            command=show_registrations
        ).pack(pady=10)
    
    # ==========================================================================
    # SECTION: RANKINGS VIEW
    # ==========================================================================
    
    def rankings_view(self):
        """Open rankings display window."""
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("View Rankings")
        win.geometry("850x550")
        
        colors = self._get_colors()
        
        # Individual rankings section
        tk.Label(
            win,
            text="Individual Rankings",
            font=('Tahoma', 14, 'bold'),
            fg=colors['danger']
        ).pack(pady=10)
        
        columns = ('Rank', 'Name', 'Points', 'Events')
        tree1 = ttk.Treeview(win, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree1.heading(col, text=col, anchor=tk.CENTER)
            tree1.column(col, width=150)
        
        tree1.pack(fill=tk.X, padx=20, pady=5)
        
        # Team rankings section
        tk.Label(
            win,
            text="Team Rankings",
            font=('Tahoma', 14, 'bold'),
            fg=colors['accent']
        ).pack(pady=10)
        
        tree2 = ttk.Treeview(win, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree2.heading(col, text=col, anchor=tk.CENTER)
            tree2.column(col, width=150)
        
        tree2.pack(fill=tk.X, padx=20, pady=5)
        
        # Load data
        ind_rankings, team_rankings = self.service.calculate_rankings()
        
        for r in ind_rankings:
            tree1.insert('', tk.END, values=(
                r.rank,
                r.participant_name,
                r.total_points,
                r.events_participated
            ))
        
        for r in team_rankings:
            tree2.insert('', tk.END, values=(
                r.rank,
                r.participant_name,
                r.total_points,
                r.events_participated
            ))
        
        self._log_event("Viewed rankings")
    
    # ==========================================================================
    # SECTION: REPORTS
    # ==========================================================================
    
    def reports_view(self):
        """Open reports window."""
        self._play_click_sound()
        
        win = tk.Toplevel(self.root)
        win.title("Reports")
        win.geometry("750x550")
        
        colors = self._get_colors()
        
        stats = self.storage.get_statistics()
        
        # Statistics title
        tk.Label(
            win,
            text="Overall Statistics",
            font=('Tahoma', 16, 'bold'),
            fg=colors['primary']
        ).pack(pady=20)
        
        # Statistics display
        stats_text = f"""
    Total Individuals: {stats['total_individuals']}
    Total Teams: {stats['total_teams']}
    Total Events: {stats['total_events']}
    Total Registrations: {stats['total_registrations']}
    Total Results: {stats['total_results']}
    
    Completed Events: {stats['completed_events']}
    Open Events: {stats['open_events']}
        """
        
        tk.Label(
            win,
            text=stats_text,
            font=('Tahoma', 12),
            justify=tk.LEFT
        ).pack(pady=10)
        
        # Action buttons
        button_frame = tk.Frame(win)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Save Data",
            font=('Tahoma', 11),
            bg=colors['primary'],
            fg='white',
            command=self.save_data
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Export CSV",
            font=('Tahoma', 11),
            bg=colors['success'],
            fg='white',
            command=self.export_csv
        ).pack(side=tk.LEFT, padx=10)
        
        self._log_event("Viewed reports")
    
    # ==========================================================================
    # SECTION: GENERAL FUNCTIONS
    # ==========================================================================

    def _choose_save_file(self, title: str = "Select Save File") -> Optional[str]:
        """Open a file picker for tournament JSON save files."""
        return filedialog.askopenfilename(
            title=title,
            initialdir=self.storage.data_dir,
            filetypes=[
                ("JSON save files", "*.json"),
                ("All files", "*.*")
            ]
        )
    
    def save_data(self):
        """Save all data to JSON file."""
        self._play_click_sound()
        filename = self.storage.save_to_json()
        messagebox.showinfo("Success", f"Data saved to:\n{filename}")
        self._log_event(f"Data saved: {filename}")
    
    def load_data(self):
        """Load data from JSON file."""
        self._play_click_sound()

        if not os.path.exists(self.storage.data_dir):
            messagebox.showwarning("Warning", "No save files found")
            return

        file_path = self._choose_save_file("Choose saved file to load")
        if not file_path:
            return

        if self.storage.load_from_json(file_path):
            self._play_success_sound()
            messagebox.showinfo("Success", "Data loaded successfully")
            self._log_event(f"Data loaded: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Error", "Failed to load data")
    
    def export_csv(self):
        """Export data to CSV format."""
        self._play_click_sound()
        use_current = messagebox.askyesnocancel(
            "Export Source",
            "Export current loaded data?\n\nYes: current data\nNo: choose a saved JSON file\nCancel: stop export"
        )
        if use_current is None:
            return

        export_storage = self.storage
        source_name = "current_data"

        if use_current is False:
            source_file = self._choose_save_file("Choose saved file to export")
            if not source_file:
                return

            export_storage = Storage(self.storage.data_dir)
            if not export_storage.load_from_json(source_file):
                messagebox.showerror("Error", "Failed to load selected source file for export")
                return
            source_name = os.path.splitext(os.path.basename(source_file))[0]

        default_export_dir = os.path.join(self.storage.data_dir, "exports")
        export_dir = filedialog.askdirectory(
            title="Choose folder to save CSV files",
            initialdir=default_export_dir,
            mustexist=False
        )
        if not export_dir:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_prefix = f"{source_name}_{timestamp}"
        file_prefix = simpledialog.askstring(
            "Export File Name",
            "Enter export file prefix (used for all CSV files):",
            initialvalue=default_prefix,
            parent=self.root
        )
        if file_prefix is None:
            return

        safe_prefix = (file_prefix.strip() or default_prefix).replace(" ", "_")
        exported_files = export_storage.export_to_csv(export_dir=export_dir, file_prefix=safe_prefix)

        if exported_files:
            self._play_success_sound()
            messagebox.showinfo(
                "Success",
                f"Exported {len(exported_files)} CSV file(s) to:\n{export_dir}\n\nPrefix: {safe_prefix}"
            )
            self._log_event(f"CSV exported to '{export_dir}' with prefix '{safe_prefix}'")
        else:
            messagebox.showwarning("Warning", "No data to export")
    
    def show_about(self):
        """Display application information dialog."""
        self._play_click_sound()
        
        about_text = f"""
{APP_NAME}
Version {APP_VERSION}
{APP_YEAR}

A professional tournament points registration and
management system with graphical user interface.

Features:
- Individual & Team Management
- Event Registration
- Results Tracking
- Rankings & Reports
- Data Export (JSON/CSV)
- Settings System
- Sound Effects
- Multi-language Support
- Color Themes for Accessibility

Thank you for using our application!
        """
        
        messagebox.showinfo("About", about_text)
    
    def exit_app(self):
        """Exit the application with optional data save."""
        self._play_click_sound()
        
        if messagebox.askyesno("Exit", "Would you like to save data before exiting?"):
            self.save_data()
        
        self._log_event("Application closed")
        self.root.destroy()


# ==============================================================================
# SECTION: MAIN ENTRY POINT
# ==============================================================================

def main():
    """
    Main entry point for the GUI application.
    
    Creates and launches the main application window.
    """
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()


# ==============================================================================
# END OF MODULE
# ==============================================================================

if __name__ == "__main__":
    main()





