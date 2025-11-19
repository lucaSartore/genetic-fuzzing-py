from typing import Self, Tuple, final
from coverage_calc_lines import CoverageTester, ExecutionResult
from inspyred_individual import InspyredIndividual
from strategy.strategy import Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from inspyred import ec

@dataclass
class InputBagSettings():
    num_inputs: int = 10
    num_individuals: int = 10
    num_generations: int = 10

class Individual:
    def __init__(self, args_dispatchers: list[ArgsDispatcher]) -> None:
        self.args_dispatchers = args_dispatchers

    def evaluate(self, tester: CoverageTester):
        results: list[ExecutionResult] = []
        for dispatcher in self.args_dispatchers:
            args = dispatcher.get_args()
            result = tester.run_test(args)
            results.append(result)
        merged_result = results[0].merge_all(results[1:])
        return merged_result.fraction_covered()

    def mutate(self):
        for dispatcher in self.args_dispatchers:
            dispatcher.mutate()

    def get_args(self) -> list[tuple]:
        return [x.get_args() for x in self.args_dispatchers]

    @staticmethod
    def corssover(a: Individual, b: Individual):
        return Individual([
            ArgsDispatcher.crossover(da, db)
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
        def generate_individual(random, args):
            return Individual([
                ArgsDispatcher.initialize(self.function)
                for _ in range(self.settings.num_inputs)
            ])

        def evaluate_individual(candidates: list[Individual], args):
            return [ c.evaluate(self.tester) for c in candidates]

        def mutate_operator(random, candidates: list[Individual], args):
            for candidate in candidates:
                candidate.mutate()
            return candidates

        def crossover_operator(random, parents: list[Tuple[Individual, Individual]], args):
            offspring: list[Individual] = []
            for a, b in parents:
                child = Individual.corssover(a,b)
                offspring.append(child)
            return offspring

        rand = random.Random()
        rand.seed(1)

        # 2. Instantiate the Evolutionary Computation (EC) engine
        ea = ec.GA(rand)
        
        # 3. Attach the custom functions (the adapters)
        ea.selector = ec.selectors.tournament_selection
        ea.variator = [mutate_operator, crossover_operator]
        ea.replacer = ec.replacers.generational_replacement
        
        # 4. Run the evolution
        # Note that we pass the custom generator and evaluator here
        final_pop: list[InspyredIndividual[Individual]] = ea.evolve(
            # Required parameters
            generator=generate_individual,
            evaluator=evaluate_individual,
            
            # Algorithm parameters
            pop_size=100,
            num_selected=20, # Number of individuals selected for breeding
            max_generations=100,
            
        )
        
        best = max(final_pop, key = lambda x: x.fitness)
        
        print(f"best score = {best.fitness}")
        args = best.candidate.get_args()
        print(f"args = {args}")
        return args
