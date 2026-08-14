import ollama

def process_door_command(prompt: str, block: str) -> str:
    """
    Sends door override and schedule requests to local Llama 3 model via Ollama.
    """
    system_prompt = f"""
    You are the Smart Door Access Controller AI for Christ University.
    You manage entrance door automation for 4 blocks (Block 1, Block 2, Block 3, Block 4).
    The default class attendance window is 10 minutes.
    
    Current Active Block: {block}.

    Your job:
    1. Analyze the incoming user command or schedule override request.
    2. Provide an official security decision log approving or rejecting the door request.
    3. Keep your response clear, structured, and formal.
    """

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to local Ollama LLM: {str(e)}. Make sure Ollama is running and 'llama3' is pulled."