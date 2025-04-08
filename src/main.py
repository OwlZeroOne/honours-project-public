import sys

from configurations import Config
from map_elites import MapElites
from parameters import Parameters
from results import Results
from timer import Timer
from calorie_.csv_handler import CsvManager


def main(params: Parameters, total_evals=5000, bins=20) -> None:
    assert not params is None, "Parameters object is null!"
    init_times = 1000
    dims = 3
    t = Timer()


    t.start()
    r:Results = MapElites(params).run(init_times, total_evals)
    elapsed_time = t.stop_and_return()

    data = [
        r.count_solutions(),
        elapsed_time,
        r.mean_quality(),
        r.std_quality(),
        r.mean_met(),
        r.std_met(),
        r.mean_duration(),
        r.std_duration(),
        r.mean_counts(),
        r.std_counts()
    ]

    print(f'Solutions found: {r.count_solutions()}')

    # runtime_stats_output.append(data)
    r.output()



if __name__ == "__main__":
    initial_weight = target_weight = period = total_evals = bins = 0
    params = None

    try:
        if len(sys.argv) < 6:
            raise ValueError
        initial_weight = float(sys.argv[1])
        target_weight = float(sys.argv[2])
        period = int(sys.argv[3])
        total_evals = int(sys.argv[4])
        bins = int(sys.argv[5])
        params = Parameters(initial_weight, target_weight, period)
    except ValueError:
        print("Unexpected number of arguments. 5 are expected: initial weight, target weight, period in weeks, total evaluations, number of bins.")
        sys.exit(1)
    except TypeError:
        print("Failed to parse to required types. Ensure correct arguments are provided.")
        sys.exit(1)

    # params.set_daily_duration_range((1,0),(3,0))
    # params.set_weekly_schedule([1,0,0,1,1,1,0])
    # params.set_weekly_duration_range((30,0),(40,0))
    main(params, total_evals, bins)
