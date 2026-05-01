# Lesson 08: Classes and Object-Oriented Programming
#
# A class is a blueprint for creating objects. An object bundles together
# data (attributes) and behavior (methods) that belong to the same concept.
#
# Example: a "Dog" class defines what every Dog has (name, breed) and
# what every Dog can do (bark, fetch). Each actual dog is an instance.
#
# To run this file:
#   python 08_classes.py

# ============================================================
# DEFINING A CLASS
# ============================================================

class Dog:
    # __init__ is the constructor — Python calls it automatically
    # whenever you create a new Dog. 'self' always refers to the
    # specific instance being created or used.
    def __init__(self, name, breed, age):
        self.name = name      # instance attribute
        self.breed = breed
        self.age = age

    # Methods are functions that belong to the class.
    def bark(self):
        print(f"{self.name} says: Woof!")

    def describe(self):
        print(f"{self.name} is a {self.age}-year-old {self.breed}.")

    def have_birthday(self):
        self.age += 1
        print(f"Happy birthday, {self.name}! You are now {self.age}.")


# --- Creating instances ---
dog1 = Dog("Rex", "German Shepherd", 3)
dog2 = Dog("Bella", "Labrador", 5)

dog1.bark()
dog2.bark()
dog1.describe()
dog2.describe()

dog1.have_birthday()
dog1.describe()

# --- Accessing attributes directly ---
print(dog2.name)    # Bella
print(dog2.age)     # 5

# ============================================================
# A MORE COMPLETE EXAMPLE: BankAccount
# ============================================================

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []      # every instance gets its own empty list

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        self.transactions.append(f"+{amount}")
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= amount
        self.transactions.append(f"-{amount}")
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def show_statement(self):
        print(f"\n--- Statement for {self.owner} ---")
        for t in self.transactions:
            print(f"  {t}")
        print(f"  Balance: ${self.balance:.2f}")


account = BankAccount("Alice", balance=1000)
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)   # should fail
account.show_statement()

# ============================================================
# INHERITANCE
# ============================================================
# A child class can inherit everything from a parent class and then
# add or override behavior. This avoids code duplication.

class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")

    def __str__(self):
        # __str__ controls what print(obj) shows
        return f"Animal(name={self.name})"


class Cat(Animal):              # Cat inherits from Animal
    def __init__(self, name, indoor=True):
        super().__init__(name, "Meow")   # call the parent __init__
        self.indoor = indoor

    def purr(self):             # method unique to Cat
        print(f"{self.name} purrs contentedly.")


class Parrot(Animal):
    def __init__(self, name, phrase):
        super().__init__(name, phrase)
        self.phrase = phrase

    def speak(self):            # override the parent method
        print(f"{self.name} squawks: '{self.phrase}!'")


generic = Animal("Generic", "...")
cat = Cat("Whiskers")
parrot = Parrot("Polly", "Polly wants a cracker")

generic.speak()
cat.speak()          # inherited from Animal
cat.purr()           # Cat-specific
parrot.speak()       # overridden version

print(cat.indoor)    # True
print(str(generic))  # Animal(name=Generic)

# --- isinstance() checks whether an object is an instance of a class ---
print(isinstance(cat, Cat))     # True
print(isinstance(cat, Animal))  # True — Cat IS an Animal (via inheritance)
print(isinstance(cat, Dog))     # False

# ============================================================
# CLASS ATTRIBUTES (shared by all instances)
# ============================================================

class Counter:
    count = 0           # class attribute — shared across all instances

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count

    def __str__(self):
        return f"Counter #{self.id}"


c1 = Counter()
c2 = Counter()
c3 = Counter()
print(c1, c2, c3)
print(f"Total counters created: {Counter.count}")

# --- Try it yourself ---
# Create a 'Rectangle' class with:
#   - __init__ that takes width and height
#   - an area() method that returns width * height
#   - a perimeter() method that returns 2 * (width + height)
#   - a __str__ method that prints something like "Rectangle(4 x 6)"
# Create two rectangles and print their area and perimeter.
