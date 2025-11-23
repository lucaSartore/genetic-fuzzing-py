from __future__ import annotations
from functools import total_ordering
from typing import Self

from inspyred.ec.variators import mutator
from numpy import test
from coverage_calc_lines import CoverageTester, ExecutionResult
from inspyred_individual import InspyredIndividual
from strategy.strategy import Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
from random import Random
from inspyred import ec
from util.mutable_probability import MutableProbability


@dataclass
class NovelSearchSettings():
    num_inputs: int = 100
    num_individuals: int = 50
    num_generations: int = 500
    num_selected: int = 10


class NovelSearch(Strategy[NovelSearchSettings]):
    @classmethod
    def initialize(cls, function: FunctionType, settings: NovelSearchSettings | None = None) -> Self:
        if settings is None:
            settings = NovelSearchSettings()
        return cls(function, settings)

    def __init__(self, function: FunctionType, settings: NovelSearchSettings):
        self.tester = CoverageTester(function)
        self.function = self.tester.export_fn
        self.settings = settings

    def run(self) -> list[tuple]:
        rand = Random()
        rand.seed(2347)
        new_individual_probability = MutableProbability(0.1, 0.01)

        def generate_individual(random: Random, args):
            return ArgsDispatcher.initialize(random, self.function)

        def evaluate_individual(candidates: list[ArgsDispatcher], args):
            to_return = list[ExecutionResult]()
            for c in candidates:
                result = self.tester.run_test(c.get_args())
                to_return.append(result)
            return to_return

        def mutate_operator(random: Random, candidates: list[ArgsDispatcher], args):
            for i,candidate in enumerate(candidates):
                if new_individual_probability.event(random):
                    candidates[i] = generate_individual(random, args)
                else:
                    candidate.mutate(random)
            return candidates

        def novelty_replacer(
            random: Random,
            population: list[ArgsDispatcher],
            parents: list[ArgsDispatcher],
            offspring: list[ArgsDispatcher],
            args
        ):
            print("novelty_replacer")
            return population
            pass

        def crossover_operator(random: Random, candidates: list[ArgsDispatcher], args):
            to_return = []
            for _ in range(len(candidates)):
                a = random.choice(candidates)
                b = random.choice(candidates)
                to_return.append(ArgsDispatcher.crossover(random,a,b))
            return to_return

        def observer(population: list[InspyredIndividual[ArgsDispatcher]], num_generations, num_evaluations, args):
            pass
            # best_score = max([x.fitness for x in population])
            # print(f'Gen: {num_generations}, score: {best_score}')

        # 2. Instantiate the Evolutionary Computation (EC) engine
        ea = ec.EvolutionaryComputation(rand)
        
        # 3. Attach the custom functions (the adapters)
        ea.selector = ec.selectors.rank_selection
        # ea.variator = [crossover_operator, mutate_operator]
        ea.variator = [crossover_operator, mutate_operator] #type: ignore
        # ea.variator = [ec.variators.uniform_crossover, mutate_operator]
        ea.replacer = ec.replacers.steady_state_replacement
        def terminator(population, num_generations, num_evaluations, args):
            return num_generations == self.settings.num_generations
        ea.terminator = terminator
        ea.observer = observer
        
        # 4. Run the evolution
        # Note that we pass the custom generator and evaluator here
        final_pop: list[InspyredIndividual[ArgsDispatcher]] = ea.evolve(
            # Required parameters
            generator=generate_individual,
            evaluator=evaluate_individual,
            maximize=True,
            
            # Algorithm parameters
            pop_size=self.settings.num_individuals,
            num_selected=self.settings.num_selected, # Number of individuals selected for breeding
        )
        
        best = max(final_pop, key = lambda x: x.fitness)
        
        print(f"best score = {best.fitness}")
        args = best.candidate.get_args()
        print(f"args = {args}")
        return [args]

