from collections import deque

"""
We will use Kahn's algorithm so set up a DAG for task scheduling in the pipeline.
A description of Kahn's algortithm can be found here:
https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/

"""

class DAG:
    def __init__(self):
        self.graph = {}

    # check how many edges are inbound to each node (function)
    # if a node has 0 in_degrees, then it it a root node
    def in_degrees(self):
        in_degrees = {}
        for node in self.graph:
            if node not in in_degrees:
                in_degrees[node] = 0
            for pointed in self.graph[node]:
                if pointed not in in_degrees:
                    in_degrees[pointed] = 0
                in_degrees[pointed] += 1
        return in_degrees

    # include a method to create and ordered list of root nodes
    def sort(self):
        in_degrees = self.in_degrees()
        #  create a queue to hold the root nodes
        to_visit = deque()
        for node in self.graph:
            if in_degrees[node] == 0:
                to_visit.append(node)
        # create a list of the root nodes ordered by dependencies
        searched = []
        while to_visit:
            node = to_visit.popleft()
            for pointer in self.graph[node]:
                in_degrees[pointer] -= 1
                if in_degrees[pointer] == 0:
                    to_visit.append(pointer)
            searched.append(node)
        return searched


    # create the final method to add nodes to the graph
    def add(self, node, to=None):
        if node not in self.graph:
            self.graph[node] = []
        if to:
            if to not in self.graph:
                self.graph[to] = []
            self.graph[node].append(to)
        if len(self.sort()) != len(self.graph):
            raise Exception

"""
We will now create the Pipeline class, which will use the DAG class above to
to schedule its tasks.

"""

class Pipeline:
    def __init__(self):
        self.tasks = DAG()
    # allow functions to have dependencies
    def task(self, depends_on=None):
        def inner(f):
            self.task.add(f)
            if depends_on:
                self.tasks.add(depends_on, f)
            return f
        return inner

    # Create method to run pipeline in scheduled order
    def run(self):
        scheduled = self.tasks.sort()
        completed = {}

        for task in scheduled:
            for node, values in self.tasks.graph.items():
                if task in values:
                    completed[task] = task(completed[node])
            if task not in completed:
                completed[task] = task()
        return completed
