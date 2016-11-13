unitCommandsConfig = {
# 0x20 - 0x40 status commands (32 possible)
    # FAILs from 0x20 - 0x30 (16 possible)
    0x20: {
        "title": "Get temperature limit",
        "response": "FAIL",
    },
    0x21: {
        "title": "Timeout failure",
        "response": "FAIL",
    },
    0x22: {
        "title": "Unexpected data failure",
        "response": "FAIL",
    },
    # OKs from 0x30 - 0x40 (16 possible)
    0x30: {
        "title": "OK, no more data bytes",
        "response": "OK",
        "collectMore": 0,
    },
    0x31: {
        "title": "OK, 1 more data byte",
        "response": "OK",
        "collectMore": 1,
    },
    0x32: {
        "title": "OK, 2 more data bytes",
        "response": "OK",
        "collectMore": 2,
    },
    0x33: {
        "title": "OK, 3 more data bytes",
        "response": "OK",
        "collectMore": 3,
    },
    0x34: {
        "title": "OK, 4 more data bytes",
        "response": "OK",
        "collectMore": 4,
    },
    0x35: {
        "title": "State is rolled down",
        "response": "OK",
        "collectMore": 0,
    },
    0x36: {
        "title": "State is rolled up",
        "response": "OK",
        "collectMore": 0,
    },
    0x37: {
        "title": "State is changing",
        "response": "OK",
        "collectMore": 0,
    },
# 0x50 - 0x70 communication commands (32 possible)
    # getters from 0x50 - 0x60 (16 possible)
    0x50: {
        "title": "Get temperature limit",
    },
    0x51: {
        "title": "Get light limit",
    },
    0x52: {
        "title": "Get current temperature",
    },
    0x53: {
        "title": "Get current light-level",
    },
    0x54: {
        "title": "Get max roll down",
    },
    0x55: {
        "title": "Get min roll down",
    },
    0x56: {
        "title": "Get current state",
    },
    # setters from 0x60 - 0x70 (16 possible)
    0x60: {
        "title": "Set temperature limit",
        "sendMore": 1,
    },
    0x61: {
        "title": "Set light limit",
        "sendMore": 2,
    },
    0x62: {
        "title": "Set max roll down in cms",
        "sendMore": 1,
    },
    0x63: {
        "title": "Set min roll down in cms",
        "sendMore": 1,
    },
    0x64: {
        "title": "Manually set state to roll down",
        "sendMore": 0,
    },
    0x65: {
        "title": "Manually set state to roll up",
        "sendMore": 0,
    },
}
