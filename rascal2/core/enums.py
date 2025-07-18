try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum


class UnsavedReply(StrEnum):
    """The responses to the warning of unsaved changes."""

    Save = "Save"
    Discard = "Discard"
    Cancel = "Cancel"
