class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        #? Note the 'is' operator. While '==' checks for equality, the 'is' operator checks to see if the two operands refer to the same object. Recall that Python references by assignment: in Python, 'x = y' means 'x should refer to whatever value y refers to' and not 'x should refer to y'. That means that if 'y' changes, then 'x' will not change unless also explicitly remapped to 'y'.
        # https://www.geeksforgeeks.org/difference-operator-python/ 
        # https://lerner.co.il/2019/06/18/understanding-python-assignment/
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight