schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
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
                        "items": {"type": ["number", "string", "boolean"]}
                    }
                },
                "required": ["name", "type"]
            }
        },
        "procedure": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
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
                "required": ["name", "matrix", "steps"]
            }
        }
    },
    "required": ["name", "nodes", "knobs", "procedure"]
}