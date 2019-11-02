class Node:
    
    def __init__(self):
        self._path = []
        self._f = 0

    def get_path(self):  
        return self._path

    def get_f(self):  
        return self._f

    def add_to_path(self, *data):
        for cur_data in data:
            self._path.append(cur_data)
        self.calculate_f()
        self.cur_state = self._path[-1]

    def __eq__(self, value):
        return self._f == value._f
    
    def __lt__(self, value):
        return self._f < value._f

    def calculate_f(self):
        # Path length
        g = len(self._path)-1
        current_data = self._path[g]
        # Heuristic is the sum of the number of missionaries and cannibles in west side
        h = (current_data[0]+current_data[1])
        self._f = g + h

    