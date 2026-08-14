import subprocess

def process_gate_command(prompt: str) -> str:
    """
    Processes gate commands locally, prioritizing explicit user intent.
    """
    prompt_lower = prompt.lower()
    
    # Enforce fast local decision matching user intent
    if any(word in prompt_lower for word in ["close", "lock", "shut", "deny"]):
        return f"Access DENIED / Action Executed: Door is now CLOSED for request '{prompt}'."
    elif any(word in prompt_lower for word in ["open", "unlock", "grant", "allow"]):
        return f"Access GRANTED / Action Executed: Door is now OPEN for request '{prompt}'."

    # Secondary LLM fallback
    try:
        system_instruction = (
            "You are a campus security gate controller. "
            "If asked to close or lock, state clearly that the door should remain CLOSED. "
            "If asked to open or unlock, state clearly that the door should OPEN."
        )
        full_prompt = f"{system_instruction}\n\nUser Command: {prompt}"
        
        result = subprocess.run(
            ["ollama", "run", "phi3", full_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return f"Command processed: '{prompt}'."