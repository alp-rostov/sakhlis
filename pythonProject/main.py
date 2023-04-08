class User:
    def __init__(self, name1, email):
        self.name2 = name1
        self.email = email

peter = User(name="Peter Robertson", email="peterrobertson@mail.com")
julia = User(name="Julia Donaldson", email="juliadonaldson@mail.com")

print(peter.name2)
print(julia.email)