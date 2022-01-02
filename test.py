
class B:
    def __init__(self,b):
        self.b=b

class A:
    def __init__(self):
        self._b = None

    @property
    def B(self):
        if not self._b:
            self._b = B(1)
        return self._b

    @B.setter
    def B(self, b):
        self._b = b

    def __getattr__(self, item):
        return getattr(self.B, item)


if __name__ == "__main__":
    a = A()
    print(a.b)