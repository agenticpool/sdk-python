import json
import re
from typing import Any, Dict, List, Union


def encode_toon(data: Any) -> str:
    """
    Encode Python data to TOON format.
    
    Args:
        data: Python object to encode
        
    Returns:
        TOON string
    """
    if data is None:
        return "null"
    
    if isinstance(data, bool):
        return "true" if data else "false"
    
    if isinstance(data, (int, float)):
        return str(data)
    
    if isinstance(data, str):
        if re.match(r'^[a-zA-Z0-9_-]+$', data) and len(data) < 50:
            return data
        return f'"{data}"'
    
    if isinstance(data, list):
        if not data:
            return "[]"
        
        first_item = data[0]
        if isinstance(first_item, dict):
            keys = list(first_item.keys())
            header = f"[{len(data)}]{{{','.join(keys)}}}:"
            lines = []
            for item in data:
                values = []
                for key in keys:
                    val = encode_toon(item[key])
                    values.append(val)
                lines.append(",".join(values))
            return header + "\n" + "\n".join(f"  {line}" for line in lines)
        else:
            return f"[{len(data)}]:" + ",".join(encode_toon(item) for item in data)
    
    if isinstance(data, dict):
        if not data:
            return "{}"
        
        lines = []
        for key, value in data.items():
            encoded_value = encode_toon(value)
            lines.append(f"{key}:{encoded_value}")
        return "\n".join(lines)
    
    return str(data)


def decode_toon(toon_str: str) -> Any:
    """
    Decode TOON string to Python data.
    
    Args:
        toon_str: TOON string to decode
        
    Returns:
        Python object
    """
    try:
        return json.loads(toon_str)
    except json.JSONDecodeError:
        pass
    
    lines = toon_str.strip().split('\n')
    
    if not lines:
        return None
    
    first_line = lines[0]
    
    if first_line.startswith('[') and ']{' in first_line:
        match = re.match(r'\[(\d+)\]\{([^}]+)\}:', first_line)
        if match:
            count = int(match.group(1))
            keys = [k.strip() for k in match.group(2).split(',')]
            
            result = []
            for i in range(1, min(count + 1, len(lines))):
                if i < len(lines):
                    values = lines[i].strip().split(',')
                    item = {}
                    for j, key in enumerate(keys):
                        if j < len(values):
                            item[key] = _parse_value(values[j])
                    result.append(item)
            return result
    
    if ':' in first_line:
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = _parse_value(value.strip())
        return result
    
    return toon_str


def _parse_value(value: str) -> Any:
    """Parse a string value to appropriate Python type"""
    if value == 'null':
        return None
    if value == 'true':
        return True
    if value == 'false':
        return False
    
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
    
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    
    return value
