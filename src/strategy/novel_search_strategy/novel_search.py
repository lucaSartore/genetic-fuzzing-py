from __future__ import annotations
from typing import cast
from rich.pretty import pprint
from coverage_strategy import  ExecutionResult
from inspyred_individual import InspyredIndividual
from strategy.strategy import SettingsBaseClass, Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
from random import Random
from inspyred import ec
from util.mutable_probability import MutableProbability


@dataclass
class NovelSearchSettings(SettingsBaseClass):
    # number of individuals to start the population with
    num_individuals: int = 1
    # number of generations
    num_generations: int = 5_000
    # number of new offspring to generate at each generation
    num_selected: int = 1


class NovelSearch(Strategy[NovelSearchSettings]):
    @classmethod
    def default_settings(cls) -> NovelSearchSettings:
        return NovelSearchSettings()

    def __init__(self, function: FunctionType, settings: NovelSearchSettings, log_dir: str):
        super().__init__(function, settings, log_dir)
        self.current_coverage: ExecutionResult | None = None

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
            for i, _ in enumerate(candidates):
                if new_individual_probability.event(random):
                    candidates[i] = generate_individual(random, args)

                candidates[i].mutate(random)
                while random.random() > 0.5:
                    candidates[i].mutate(random)
            return candidates


        def novelty_replacer(
            random: Random,
            population: list[InspyredIndividual[ArgsDispatcher, ExecutionResult]],
            parents: list[InspyredIndividual[ArgsDispatcher, ExecutionResult]],
            offspring: list[InspyredIndividual[ArgsDispatcher, ExecutionResult]],
            args
        ):
            
            if self.current_coverage is None:
                self.current_coverage = ExecutionResult.merge_list([x.fitness for x in population])

            individuals_to_add = [
                x
                for x in offspring
                if x.fitness.novelty(self.current_coverage) != 0
            ]

            to_return =  population + individuals_to_add
            self.current_coverage = self.current_coverage.merge_all([
                x.fitness
                for x in individuals_to_add
            ])

            return to_return

        def crossover_operator(random: Random, candidates: list[ArgsDispatcher], args):
            to_return = []
            for _ in range(len(candidates)):
                a = random.choice(candidates)
                b = random.choice(candidates)
                to_return.append(ArgsDispatcher.crossover(random,a,b))
            return to_return

        def observer(population: list[InspyredIndividual[ArgsDispatcher, ExecutionResult]], num_generations, num_evaluations, args):
            if self.current_coverage == None:
                return
            self.log(self.current_coverage.fraction_covered())

        # 2. Instantiate the Evolutionary Computation (EC) engine
        ea = ec.EvolutionaryComputation(rand)
        
        # 3. Attach the custom functions (the adapters)
        ea.selector = ec.selectors.rank_selection
        # ea.variator = [crossover_operator, mutate_operator]
        ea.variator = [crossover_operator, mutate_operator] #type: ignore
        # ea.variator = [ec.variators.uniform_crossover, mutate_operator]
        ea.replacer = novelty_replacer
        # ea.replacer = ec.replacers.comma_replacement

        def terminator(population, num_generations, num_evaluations, args):
            return num_generations == self.settings.num_generations

        ea.terminator = terminator
        ea.observer = observer
        
        # 4. Run the evolution
        # Note that we pass the custom generator and evaluator here
        final_pop = cast(list[InspyredIndividual[ArgsDispatcher, ExecutionResult]], ea.evolve(
            # Required parameters
            generator=generate_individual,
            evaluator=evaluate_individual,
            maximize=True,
            
            # Algorithm parameters
            pop_size=self.settings.num_individuals,
            num_selected=self.settings.num_selected, # Number of individuals selected for breeding
        ))
        
        assert self.current_coverage != None, "logical error: final score not calculated"
        print(f'final score: {self.current_coverage.fraction_covered()}')
        final_pop.sort(key= lambda x: x.fitness.fraction_covered(), reverse = True)
        args = [x.candidate.get_args() for x in final_pop]
        print(f"args:")
        pprint(args)
        return args

