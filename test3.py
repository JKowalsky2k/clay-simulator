import copy
class A:
    def __init__(self, b) -> None:
        self.a = copy.copy(b)

    def get(self):
        return self.a.get()

    def inc(self):
        self.a.b += 1

class B:
    def __init__(self) -> None:
        self.b = 0

    def set(self, bb):
        self.b = bb
    
    def get(self):
        return self.b
    
    def inc(self):
        self.b += 1

b = B()
a = A(b)

print(f"{b.get() = }")
print(f"{a.get() = }")

b.inc()

print(f"{b.get() = }")
print(f"{a.get() = }")

a.inc()

print(f"{b.get() = }")
print(f"{a.get() = }")

b.set(b.get()+1)
print(f"{b.get() = }")
print(f"{a.get() = }")