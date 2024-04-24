from project.backend.src.models.models import Tables

tables = {
    "Столик №1": {
        "table_id": 1,
        "place_count": 2,
        "is_reserve": "N"
    },
    "Столик №2": {
        "table_id": 2,
        "place_count": 4,
        "is_reserve": "N"
    },
    "Столик №3": {
        "table_id": 3,
        "place_count": 4,
        "is_reserve": "N"
    },
    "Столик №4": {
        "table_id": 4,
        "place_count": 2,
        "is_reserve": "N"
    },
    "Столик №5": {
        "table_id": 5,
        "place_count": 4,
        "is_reserve": "N"
    },
}

tables_collection = Tables(tables)