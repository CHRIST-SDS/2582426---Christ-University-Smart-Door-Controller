import os

def get_door_image(command_or_decision: str) -> str:
    """
    Evaluates the input text and returns the correct image path.
    """
    text_lower = command_or_decision.lower()
    
    # Check for close/lock intent
    if any(word in text_lower for word in ["close", "lock", "shut", "denied", "closed"]):
        return os.path.join("data", "close_door.png")
    
    # Check for open/unlock intent
    if any(word in text_lower for word in ["open", "unlock", "grant", "allow", "opened"]):
        return os.path.join("data", "open_door.png")
        
    # Default fallback
    return os.path.join("data", "close_door.png")