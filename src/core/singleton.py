class Singleton:
    """
    A Singleton is a class that allows only one instance of itself to be created,
    and provides a global reference to that instance.
    """

    def __init_subclass__(cls):
        cls.instance = None
        super().__init_subclass__()
    
    def __init__(self):
        cls = self.__class__
        if cls.instance is not None:
            raise Exception(f"Error: Attempted to instantiate Singleton class \"{cls.__name__}\" more than once.")
        cls.instance = self