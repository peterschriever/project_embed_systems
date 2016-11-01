unitCommandsConfig = {
# 0xA0 - 0xAF status commands (16 statuscommands)
    # FAILS from 0xA8 - 0xAF (8 failcodes possible)
    0xA8: {
        "response": "FAIL",
        "message": "Generic failure"
    },
    0xA9: {
        "response": "FAIL",
        "message": "Timeout failure"
    },
    0xAA: {
        "response": "FAIL",
        "message": "Unexpected data failure"
    },
    # Successes from 0xA0 - 0xA8 (8 successcodes possible)
    0xA0: {
        "response": "OK",
        "collectMore": False,
    },
    0xA1: {
        "response": "OK",
        "collectMore": True,
    },
}
