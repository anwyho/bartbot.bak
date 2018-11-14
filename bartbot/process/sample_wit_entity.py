{
    "datetime": [
        {
            "confidence": 0.950555,
            "values": [
                {
                    "value": "2018-10-30T20:00:00.000-07:00",
                    "grain": "hour",
                    "type": "value"
                },
                {
                    "value": "2018-10-31T20:00:00.000-07:00",
                    "grain": "hour",
                    "type": "value"
                },
                {
                    "value": "2018-11-01T20:00:00.000-07:00",
                    "grain": "hour",
                    "type": "value"
                }
            ],
            # Possibility 1
            "to": "2018-10-30T20:00:00.000-07:00",
            "from": "2018-10-30T21:00:00.000-07:00",
            # Possibility 2
            "value": "2018-10-30T20:00:00.000-07:00",
            "grain": "hour",
            "type": "value",
            "_entity": "datetime",
            "_body": "around 8pm",
            "_start": 33,
            "_end": 43
        }
    ],
    # This COULD be here in place of either 'dest' or 'orig'
    "station": [
        {
            "confidence": 1,
            "value": "DBRK",
            "type": "value",
            "_entity": "station",
            "_body": "dberk",
            "_start": 42,
            "_end": 47
        }
    ],
    "orig": [
        {
            "confidence": 0.99967680726055,
            "value": "ORIN",
            "type": "value",
            "_entity": "station",
            "_role": "orig",
            "_body": "orinda",
            "_start": 49,
            "_end": 55
        }
    ],
    "dest": [
        {
            "confidence": 0.99477028741716,
            "value": "DBRK",
            "type": "value",
            "_entity": "station",
            "_role": "dest",
            "_body": "dberk",
            "_start": 59,
            "_end": 64
        }
    ],
    "intent": [
        {
            "confidence": 0.99999997949261,
            "value": "travel",
            "_entity": "intent"
        },
        {
            "confidence": 1.4472552211224e-08,
            "value": "round-trip-cost",
            "_entity": "intent"
        }
        # ...
        # travel, round-trip-cost, weather, map, help, reset, single-trip-cost
        # TODO: Train wit on more round-trip-costs
    ],
    "greetings": [
        {
            "confidence": 5.5241935881249e-05,
            "value": "true",
            "_entity": "greetings"
        }
    ],
    "thanks": [
        {
            "confidence": 5.1764553844853e-05,
            "value": "true",
            "_entity": "thanks"
        }
    ],
    "bye": [
        {
            "confidence": 1.8766769131525e-05,
            "value": "true",
            "_entity": "bye"
        }
    ]
}
