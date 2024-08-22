from datetime import timedelta
# Liste des intervalles à supporter
INTERVALS = {
        "1m": {
            "timedelta": timedelta(minutes=1),
            "interval_ms": 60000
        },
        "2m": {
            "timedelta": timedelta(minutes=2),
            "interval_ms": 120000
        },
        "5m": {
            "timedelta": timedelta(minutes=5),
            "interval_ms": 300000
        },
        "15m": {
            "timedelta": timedelta(minutes=15),
            "interval_ms": 900000
        },
        "30m": {
            "timedelta": timedelta(minutes=30),
            "interval_ms": 1800000
        },
        "1h": {
            "timedelta": timedelta(hours=1),
            "interval_ms": 3600000
        },
        "2h": {
            "timedelta": timedelta(hours=2),
            "interval_ms": 7200000
        },
        "4h": {
            "timedelta": timedelta(hours=4),
            "interval_ms": 14400000
        },
        "12h": {
            "timedelta": timedelta(hours=12),
            "interval_ms": 43200000
        },
        "1d": {
            "timedelta": timedelta(days=1),
            "interval_ms": 86400000
        },
        "1w": {
            "timedelta": timedelta(weeks=1),
            "interval_ms": 604800000
        },
        "1M": {
            "timedelta": timedelta(days=30),
            "interval_ms": 2629746000
        }
    }