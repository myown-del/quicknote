class UnsetType:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UnsetType, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return "Unset"

    def __bool__(self):
        return False


Unset = UnsetType()
