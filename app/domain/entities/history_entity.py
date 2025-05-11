class HistoryEntity:
    id: int
    full_name: str
    entity_type: str
    action: str
    message: str

    def __init__(
        self, id: int, full_name: str, entity_type: str, action: str, message: str
    ):
        self.id = id
        self.full_name = full_name
        self.entity_type = entity_type
        self.action = action
        self.message = message
