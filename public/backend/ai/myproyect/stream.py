import json

def parse_stream(stream: str) -> list[dict]:
    events = []
    lines = stream.split('\n')
    for line in lines:
        if line.startswith('data: '):
            json_str = line[6:]  # Remove 'data: ' prefix
            try:
                data = json.loads(json_str)
                events.append(data)
            except json.JSONDecodeError:
                # Handle incomplete or malformed JSON
                print(f"Failed to parse JSON: {json_str}")
                continue
    return events
