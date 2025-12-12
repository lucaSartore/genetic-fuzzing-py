from __future__ import annotations
from coverage_strategy import CoverageTester
from inspyred_individual import InspyredIndividual
from strategy.strategy import SettingsBaseClass, Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
from random import Random
from inspyred import ec
from util.mutable_probability import MutableProbability


# in parity in term of execution time with novelty search
# @dataclass
# class InputBagSettings(SettingsBaseClass):
#     num_inputs: int = 100
#     num_individuals: int = 50
#     num_generations: int = 800
#     num_selected: int = 10


# in parity in term of number of function calls with novelty search
@dataclass
class InputBagSettings(SettingsBaseClass):
    num_inputs: int = 20
    num_individuals: int = 20
    num_generations: int = 25
    num_selected: int = 10

class Individual:
    def __init__(self, args_dispatchers: list[ArgsDispatcher], mutation_probability = MutableProbability(0.1, 0.01)) -> None:
        self.args_dispatchers = args_dispatchers
        self.mutation_probability = mutation_probability

    def get_test_result(self, tester: CoverageTester):
        args = [d.get_args() for d in self.args_dispatchers]
        return tester.run_test(args)

    def evaluate(self, tester: CoverageTester):
        result = self.get_test_result(tester)
        return result.fraction_covered()

    def mutate(self, random: Random):
        self.mutation_probability.mutate(random)
        for dispatcher in self.args_dispatchers:
            if self.mutation_probability.event(random):
                dispatcher.mutate(random)

    def get_args(self) -> list[tuple]:
        return [x.get_args() for x in self.args_dispatchers]

    @staticmethod
    def crossover(random, a: Individual, b: Individual):
        mp = MutableProbability.crossover(random, a.mutation_probability, b.mutation_probability)
        return Individual([
            ArgsDispatcher.crossover(random, da, db)
            for (da,db) in zip(a.args_dispatchers, b.args_dispatchers)
        ], mp)

class InputBag(Strategy[InputBagSettings]):
    @classmethod
    def default_settings(cls) -> InputBagSettings:
        return InputBagSettings()

    def __init__(self, function: FunctionType, settings: InputBagSettings, log_dir: str):
        super().__init__(function, settings, log_dir)

    def run(self) -> list[tuple]:
        rand = Random()
        rand.seed(2347)
        new_individual_probability = MutableProbability(0.1, 0.01)

        def generate_individual(random: Random, args):
            return Individual([
                ArgsDispatcher.initialize(random, self.function)
                for _ in range(self.settings.num_inputs)
            ])

        def evaluate_individual(candidates: list[Individual], args):
            return [ c.evaluate(self.tester) for c in candidates]

        def mutate_operator(random: Random, candidates: list[Individual], args):
            for i,_ in enumerate(candidates):
                if new_individual_probability.event(random):
                    candidates[i] = generate_individual(random, args)
                candidates[i].mutate(random)
                while random.random() > 0.5:
                    candidates[i].mutate(random)
            return candidates

        # def crossover_operator(random, parents: list[Tuple[Individual, Individual]], args):
        def crossover_operator(random: Random, candidates: list[Individual], args):
            print(len(candidates))
            to_return = []
            for _ in range(len(candidates)):
                a = random.choice(candidates)
                b = random.choice(candidates)
                to_return.append(Individual.crossover(random,a,b))
            return to_return

        def observer(population: list[InspyredIndividual[Individual, float]], num_generations, num_evaluations, args):
            best_score = max([x.fitness for x in population])
            self.log(best_score)

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
        final_pop: list[InspyredIndividual[Individual, float]] = ea.evolve(
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
        return args
