import threading
from solver import Solver
from board import Board
class SolverThread(threading.Thread):
    def __init__(self, lock, move_callback, done_callback, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group=group, target=target, 
			             name=name)
        self.lock = lock
        self.solver = Solver(lock, move_callback, done_callback)

    def run(self):
        print("Start game")
        moves_played = self.solver.solve_recursive(Board())
        print(f"Finished {self.solver.statistics['Games finished']} games! (skipped {self.solver.statistics['Boards skipped']})")
        if moves_played:
            m = '\n'.join([f"{m[0][0]}, {m[0][1]} -> {m[1][0]}, {m[1][1]}" for m in moves_played])
            print(f"Solution found, moves:\n{m}")