from __future__ import annotations
from typing import Self
from coverage_calc_lines import CoverageTester, ExecutionResult
from dataset.output.count_and_say import count_and_say
from inspyred_individual import InspyredIndividual
from strategy.strategy import Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from inspyred import ec


@dataclass
class InputBagSettings():
    num_inputs: int = 25
    num_individuals: int = 50
    num_generations: int = 500

class Individual:
    def __init__(self, args_dispatchers: list[ArgsDispatcher]) -> None:
        self.args_dispatchers = args_dispatchers

    def evaluate(self, tester: CoverageTester):
        args = [d.get_args() for d in self.args_dispatchers]
        result = tester.run_test(args)
        return result.fraction_covered()

    def mutate(self, random):
        for dispatcher in self.args_dispatchers:
            dispatcher.mutate(random)

    def get_args(self) -> list[tuple]:
        return [x.get_args() for x in self.args_dispatchers]

    @staticmethod
    def corssover(random, a: Individual, b: Individual):
        return Individual([
            ArgsDispatcher.crossover(random, da, db)
            for (da,db) in zip(a.args_dispatchers, b.args_dispatchers)
        ])

class InputBag(Strategy[InputBagSettings]):
    @classmethod
    def initialize(cls, function: FunctionType, settings: InputBagSettings | None = None) -> Self:
        if settings is None:
            settings = InputBagSettings()
        return cls(function, settings)

    def __init__(self, function: FunctionType, settings: InputBagSettings):
        self.tester = CoverageTester(function)
        self.function = self.tester.export_fn
        self.settings = settings

    def run(self) -> list[tuple]:
        rand = random.Random()
        rand.seed(2347)

        def generate_individual(random, args):
            return Individual([
                ArgsDispatcher.initialize(random, self.function)
                for _ in range(self.settings.num_inputs)
            ])

        def evaluate_individual(candidates: list[Individual], args):
            return [ c.evaluate(self.tester) for c in candidates]
            # return [ 1 for c in candidates]

        def mutate_operator(random, candidates: list[Individual], args):
            print("mutate operator")
            for candidate in candidates:
                candidate.mutate(random)
            return candidates

        # def crossover_operator(random, parents: list[Tuple[Individual, Individual]], args):
        def crossover_operator(random, candidates: list[Individual], args):
            to_return = []
            for _ in range(len(candidates)):
                a = random.choice(candidates)
                b = random.choice(candidates)
                to_return.append(Individual.corssover(random,a,b))
            return to_return

        def observer(population: list[InspyredIndividual[Individual]], num_generations, num_evaluations, args):
            best_score = max([x.fitness for x in population])
            print(f'Gen: {num_generations}, score: {best_score}')

        # 2. Instantiate the Evolutionary Computation (EC) engine
        ea = ec.EvolutionaryComputation(rand)
        
        # 3. Attach the custom functions (the adapters)
        ea.selector = ec.selectors.tournament_selection
        # ea.variator = [crossover_operator, mutate_operator]
        ea.variator = [crossover_operator, mutate_operator] #type: ignore
        # ea.variator = [ec.variators.uniform_crossover, mutate_operator]
        ea.replacer = ec.replacers.generational_replacement
        def terminator(population, num_generations, num_evaluations, args):
            return num_generations == self.settings.num_generations
        ea.terminator = terminator
        ea.observer = observer
        
        # 4. Run the evolution
        # Note that we pass the custom generator and evaluator here
        final_pop: list[InspyredIndividual[Individual]] = ea.evolve(
            # Required parameters
            generator=generate_individual,
            evaluator=evaluate_individual,
            maximize=True,
            
            # Algorithm parameters
            pop_size=self.settings.num_individuals,
            num_selected=5, # Number of individuals selected for breeding
        )
        
        best = max(final_pop, key = lambda x: x.fitness)
        
        print(f"best score = {best.fitness}")
        args = best.candidate.get_args()
        print(f"args = {args}")
        return args
