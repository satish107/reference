"""
Link: https://www.geeksforgeeks.org/builder-method-python-design-patterns/

"""

# Good Practice

class Course:
	def __init__(self):
		self.Fee()
		self.available_batches()

	def Fee(self):
		raise NotImplementedError

	def available_batches(self):
		raise NotImplementedError

	def __repr__(self):
		return "Fee: {0.fee} | Available Batches: {0.batches}".format(self)

class SDE:
	def fee(self):
		self.fee = 1000

	def batches(self):
		self.batches = 5

	def __str__(self):
		return "SDE"

class DSA:
	def fee(self):
		self.fee = 2000

	def batches(self):
		self.batches = 6

	def __str__(self):
		return "DSA"

class STL:
	def fee(self):
		self.fee = 3000

	def batches(self):
		self.batches = 7

	def __str__(self):
		return "STL"

class ComplexCourse:
	def __repr__(self):
		return 'Fee : {0.fee} | available_batches: {0.batches}'.format(self)

class Complexcourse(ComplexCourse):
	def Fee(self):
		self.fee = 1000

	def available_batches(self):
		self.batches = 5

def construct_course(cls):
	course = cls()
	course.Fee()
	course.available_batches()
	return course


complex_course = construct_course(Complexcourse)
print(complex_course)




# Product: Computer
class Computer:
    def __init__(self):
        self.parts = {}

    def add_part(self, part_name, part_spec):
        self.parts[part_name] = part_spec

    def show(self):
        print("Computer Configuration:")
        for part, spec in self.parts.items():
            print(f"{part}: {spec}")


# Builder: Abstract builder class
class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def build_cpu(self):
        raise NotImplementedError

    def build_ram(self):
        raise NotImplementedError

    def build_storage(self):
        raise NotImplementedError

    def build_graphics_card(self):
        raise NotImplementedError

    def get_computer(self):
        return self.computer


# ConcreteBuilder: Specific builder implementation
class HighEndComputerBuilder(ComputerBuilder):
    def build_cpu(self):
        self.computer.add_part("CPU", "High-End CPU")
        return self

    def build_ram(self):
        self.computer.add_part("RAM", "32GB RAM")
        return self

    def build_storage(self):
        self.computer.add_part("Storage", "1TB SSD")
        return self

    def build_graphics_card(self):
        self.computer.add_part("Graphics Card", "NVIDIA RTX 3080")
        return self


# Director: Orchestrates the construction process
class ComputerDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_cpu().build_ram().build_storage().build_graphics_card()


if __name__ == "__main__":
    # Client code
    high_end_builder = HighEndComputerBuilder()
    director = ComputerDirector(high_end_builder)

    # Constructing a high-end computer
    director.construct()
    high_end_computer = high_end_builder.get_computer()
    high_end_computer.show()


"""
When you run the script, it creates a HighEndComputer with a high-end CPU, 32GB RAM, 1TB SSD storage, and an NVIDIA RTX 3080 graphics card. The Builder Pattern allows you to create different configurations of computers by using the same construction process with different builders.

You can extend this example by creating additional concrete builders for different types of computers (e.g., LowEndComputerBuilder, MidRangeComputerBuilder) and use the same director to construct them.
"""
