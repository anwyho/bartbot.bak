

class User:
    def __init__(self):
        self.fn:Optional[str] = None
        self.ln:Optional[str] = None
        self.locale:Optional[str] = None
        self.history:Optional[List[str]] = None