class Node:
    def __init__(self, uuid, task_name, args, root_id, parent):
        self.uuid = uuid
        self.task_name = task_name
        self.args = args
        self.root_id = root_id
        self.parent = parent
        self.children = set()

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return not self == other

    def add_child(self, child):
        if child in self.children:
            print('child already exist')
            return
        self.children.add(child)
