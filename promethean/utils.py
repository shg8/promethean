import re
import unicodedata

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "output": {"type": "string"},
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "ssh": {
                        "type": "object",
                        "properties": {
                            "host": {"type": "string"},
                            "port": {"type": "integer"},
                            "username": {"type": "string"},
                            "password": {"type": "string"}
                        },
                        "required": ["host", "port", "username", "password"]
                    },
                    "variables": {
                        "type": "object",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["name", "ssh", "variables"]
            }
        },
        "knobs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "min": {"type": "number"},
                    "max": {"type": "number"},
                    "interval": {"type": "number"},
                    "values": {
                        "type": "array",
                        "items": {"type": ["number", "string"]}
                    }
                },
                "required": ["name", "type"]
            }
        },
        "matrix": {
            "type": "array",
            "items": {"type": "string"}
        },
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "node": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "script": {"type": "string"},
                    "file": {
                        "oneOf": [
                            {"type": "string"},
                            {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "alias": {"type": "string"},
                                        "path": {"type": "string"}
                                    },
                                    "required": ["alias", "path"]
                                }
                            }
                        ],
                    },
                },
                "required": ["name", "node"]
            }
        }
    },
    "required": ["name", "nodes", "knobs", "steps"]
}

def slugify(value, allow_unicode=False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')