import random
import copy
import time

class FireflyAlgorithm:
    def __init__(self, employees, tasks, population_size=10, generations=50, alpha=0.5, beta0=1.0, gamma=0.1):
        self.employees = employees
        self.tasks = tasks
        self.population_size = population_size
        self.generations = generations
        self.alpha = alpha
        self.beta0 = beta0
        self.gamma = gamma

    def create_solution(self):
        return [random.choice(self.employees) for _ in self.tasks]

    def fitness(self, solution):
        temp_hours = {e.name: 0 for e in self.employees}
        score = 0
        for task, emp in zip(self.tasks, solution):
            has_skill = task.skill in emp.skills
            has_time = temp_hours[emp.name] + task.hours <= emp.max_hours
            if has_skill and has_time:
                score += 10
                temp_hours[emp.name] += task.hours
            elif has_skill:
                score += 5
        return score

    def distance(self, sol1, sol2):
        return sum(e1 != e2 for e1, e2 in zip(sol1, sol2))

    def move_firefly(self, firefly_i, firefly_j):
        new_solution = []
        for i in range(len(self.tasks)):
            if firefly_i[i] != firefly_j[i] and random.random() < self.beta0 * (1 / (1 + self.gamma * self.distance(firefly_i, firefly_j))):
                new_solution.append(firefly_j[i])
            else:
                if random.random() < self.alpha:
                    new_solution.append(random.choice(self.employees))
                else:
                    new_solution.append(firefly_i[i])
        return new_solution

    def run(self):
        population = [self.create_solution() for _ in range(self.population_size)]
        fitnesses = [self.fitness(sol) for sol in population]

        for _ in range(self.generations):
            for i in range(self.population_size):
                for j in range(self.population_size):
                    if fitnesses[j] > fitnesses[i]:
                        population[i] = self.move_firefly(population[i], population[j])
                        fitnesses[i] = self.fitness(population[i])

        best_index = fitnesses.index(max(fitnesses))
        return population[best_index]
