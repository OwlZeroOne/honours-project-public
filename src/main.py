import sys
import pandas as pd

from configurations import Config
from map_elites import MapElites
from statistics import Statistics
from timer import Timer
from csv_handler import CsvHandler

def save_runtime_stats(config: Config, stats: Statistics, elapsed_time: float) -> None:
    """
    Save runtime statistics to a CSV file.
    :param config: `Config` - Configurations object.
    :param stats: `Statistics` - Statistics object.
    :param elapsed_time: `float` - Algorithm's execution time in seconds.
    """
    total_evals = config.total_evaluations()
    directory = "./../results/runtime-experiment/"
    filename = f"{total_evals}_evals.csv"
    csv_handler = CsvHandler(
        "./../results/runtime_stats/",
        f"{total_evals}_evals.csv",
        ["solutions_count", "execution_t", "fitness_mean", "fitness_std", "met_mean", "met_std"]
    )
    data = [
        stats.count_solutions(),
        elapsed_time,
        stats.mean_quality(),
        stats.std_quality(),
        stats.mean_met(),
        stats.std_met()
    ]
    csv_handler.append(data)
    print(f"Runtime saved to {directory}{filename}.")

def save_json(config: Config, map_e: MapElites) -> None:
    """
    Save output schedules to a JSON file, acceptable for HTTP communications.
    :param config: `config` - Configurations object that stores user parameters.
    :param map_e: `MapElites` - For schedule retrieval.
    """
    solutions = map_e.solutions()
    data = []
    path = f"./../results/schedules_{config.initial_weight()}_{config.target_weight()}_{config.period()}.json"

    for i in range(len(solutions)):
        s = solutions[i]
        es = s.exercises()
        row = [
            s.features(),
            s.fitness(),
            [(e.name(), e.duration(), e.exercise_days()) for e in es],
        ]
        data.append(row)

    data_df = pd.DataFrame(data, columns=["features", "fitness", "exercises"])
    data_df.to_json(path, orient="records", indent=4)
    print(f"Schedules saved to {path}.")

def main(initial_weight, target_weight, period) -> None:
    """
    Entry point for the MAP-Elites algorithm. Sets up the variables and instances, runs the algorithm, times it, and
    saves the results.
    :param initial_weight: `int` - User's initial weight.
    :param target_weight: `int` - User's target weight.
    :param period: `int` - Period in weeks by which target weight should be achieved.
    """
    # Initialise Timer, Config, MapElites, and CsvHandler instances
    t = Timer()
    config = Config(initial_weight, target_weight, period)
    map_elites: MapElites = MapElites(config)

    # Run MAP-Elites algorithm
    t.start()
    map_elites.run()
    t.stop()

    # Save Results
    elapsed_time = t.result()
    stats: Statistics = Statistics(map_elites)

    # Print Results
    print("----------------------------------------")
    print(f"Elapsed time:       {f"{elapsed_time} seconds" if elapsed_time < 60 else f"{round(elapsed_time / 60, 2)} minutes"}")
    print(f"Map Shape:          {map_elites.performances().shape}")
    print(f"Solutions Found:    {len(map_elites.solutions())}")
    print(f"Best Fitness:       {map_elites.performances().min()}")

    # Output Results
    print("----------------------------------------")
    save_runtime_stats(config, stats, elapsed_time)
    save_json(config, map_elites)
    print("========================================\n")

def runtime_experiment(w0, wt, P) -> None:
    """
    Conduct a runtime experiment that runs the algorithm 5 times for evaluations of 5,000 to 1,000,000 in steps of
    5,000 and 50,000. Results are saved to a CSV file inside the `results/runtime_stats/` directory.
    :param w0: `float` - User's initial weight.
    :param wt: `float` - User's target weight.
    :param P: `int` - Period in weeks by which target weight should be achieved.
    """
    def save_results(map_e: MapElites, config: Config, t_elapsed: float):
        statistics = Statistics(map_e)
        directory = "./../results/runtime_stats/"
        filename = f"{config.total_evaluations()}_evals.csv"

        csv_handler = CsvHandler(
            directory,
            filename,
            ["solutions", "execution_t", "fitness_mean", "fitness_std", "met_mean", "met_std"],
        )

        data = [
            statistics.count_solutions(),
            t_elapsed,
            statistics.mean_quality(),
            statistics.std_quality(),
            statistics.mean_met(),
            statistics.std_met()
        ]

        csv_handler.append(data)
        print(f"Results saved to {directory}{filename}.")
    # =================================================================
    config = Config(w0, wt, P)
    t = Timer()

    evals = 800000
    step = 5000

    while evals <= 1000000:
        if evals >= 100000:
            step = 50000

        for _ in range(5):
            config.set_total_evaluations(evals)
            t.start()
            new_m = MapElites(config)
            new_m.run()
            t.stop()
            save_results(new_m, config, t.result())

        evals += step

if __name__ == "__main__":
    initial_weight = target_weight = period= 0

    try:
        if len(sys.argv) != 4:
            print(f"Unexpected number of arguments ({len(sys.argv) - 1}). 3 are expected: initial weight, target weight, period in weeks.")
            sys.exit(1)
        try:
            initial_weight = float(sys.argv[1])
            target_weight = float(sys.argv[2])
            period = int(sys.argv[3])
        except Exception:
            raise TypeError

        if initial_weight <= 0 or target_weight <= 0 or period <= 0:
            print(f"Initial weight, target weight, and period must be greater than zero.")
            sys.exit(1)

        if initial_weight <= target_weight:
            print(f"Initial weight must be greater than target weight.")
            sys.exit(1)

    except TypeError:
        print(f"Unexpected argument type(s). Expecting int | float, int | float, int.")
    except Exception as e:
        print("Unexpected Error: " + str(e))

    # ==== COMMENT ONE TO UNCOMMENT THE OTHER ====
    main(initial_weight, target_weight, period)
    # runtime_experiment(initial_weight, target_weight, period)