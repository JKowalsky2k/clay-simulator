class CramerSolver():
    def __init__(self, eq1, eq2, eq3) -> None:
        self.equation1 = {"a" : eq1[0], "b" : eq1[1], "c" : eq1[2]}
        self.equation2 = {"a" : eq2[0], "b" : eq2[1], "c" : eq2[2]}
        self.equation3 = {"a" : eq3[0], "b" : eq3[1], "c" : eq3[2]}
