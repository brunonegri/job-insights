from src.pre_built.counter import count_ocurrences


def test_counter():
    path = "data/jobs.csv"

    with open(path) as file:
        data = file.read()
        expected = data.lower().count("python")

        assert expected == count_ocurrences(path, "python")
