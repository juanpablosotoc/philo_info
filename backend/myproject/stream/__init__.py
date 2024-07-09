import json


def clean_str(text: str) -> str:
    return text.replace('data: ', '', 1)


def parse_stream(stream_str: str) -> list[dict]:
    counted_strings = []
    current_str = ''
    opening_curly_braces = 0
    closing_curly_braces = 0
    prev_char_was_esc_backslash = False
    inside_of_string = False
    for char in stream_str:
        current_str += char
        if inside_of_string:
            if prev_char_was_esc_backslash:
                prev_char_was_esc_backslash = False
                continue
            else:
                if char == '\\':
                    prev_char_was_esc_backslash = True
                elif char == '"':
                    inside_of_string = False
        else:
            # Check if json was closed, if so append and reset
            if opening_curly_braces > 0 and opening_curly_braces == closing_curly_braces:
                counted_strings.append({'complete': True, 'data': clean_str(current_str)})
                current_str = ''
                opening_curly_braces = 0
                closing_curly_braces = 0
            # Check if string was opened
            if char == '"': inside_of_string = True
            elif char == '{': opening_curly_braces += 1
            elif char == '}': closing_curly_braces += 1
    if len(current_str) > 0:
        counted_strings.append({'complete': False, 'data': clean_str(current_str)})
    actual_resp = []
    for item in counted_strings:
        if item['complete']:
            actual_resp.append({'complete': True, 'data': json.loads(item['data'])})
        else:
            actual_resp.append({'complete': False, 'data': item['data']})
    return actual_resp