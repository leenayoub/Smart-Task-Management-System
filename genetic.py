import random


class GeneticAlgorithm:
    def __init__(self, employees, tasks, population_size=6, generations=80, mutation_rate=0.1):
        self.employees = employees
        self.tasks = tasks
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def create_individual(self):
        return [random.choice(self.employees) for _ in self.tasks]

    def calculate_fitness(self, individual):
        temp_hours = {emp.name: 0 for emp in self.employees}
        score = 0
        for task, emp in zip(self.tasks, individual):
            has_skill = task.skill in emp.skills
            has_time = temp_hours[emp.name] + task.hours <= emp.max_hours
            if has_skill and has_time:
                score += 10
                temp_hours[emp.name] += task.hours
            elif has_skill:
                score += 5
        return score

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(individual) - 1)
            individual[idx] = random.choice(self.employees)
        return individual

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    def select_parents(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        if total_fitness <= 0:
            return random.sample(population, 2)
        return random.choices(population, weights=fitnesses, k=2)

    def run(self):
        population = [self.create_individual() for _ in range(self.population_size)]
        best = max(population, key=self.calculate_fitness)
        best_fitness = self.calculate_fitness(best)

        for _ in range(self.generations):
            fitnesses = [self.calculate_fitness(ind) for ind in population]
            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population
            current_best = max(population, key=self.calculate_fitness)
            current_fitness = self.calculate_fitness(current_best)
            if current_fitness > best_fitness:
                best, best_fitness = current_best, current_fitness




        return best
