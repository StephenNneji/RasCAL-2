import numpy as np
import ratapi.outputs


def check_results_equal(actual_results, expected_results) -> None:
    """Compare two instances of "Results" or "BayesResults" objects for equality.

    We focus here on the fields common to both results objects, and also check the equality of the subclasses
    "CalculationResults" and "ContrastParams".
    """
    contrast_param_fields = [
        "scalefactors",
        "bulkIn",
        "bulkOut",
        "subRoughs",
        "resample",
    ]

    assert (
        isinstance(actual_results, ratapi.outputs.Results) and isinstance(expected_results, ratapi.outputs.Results)
    ) or (
        isinstance(actual_results, ratapi.outputs.BayesResults)
        and isinstance(expected_results, ratapi.outputs.BayesResults)
    )

    # The first set of fields are either 1D or 2D python lists containing numpy arrays.
    # Hence, we need to compare them element-wise.
    for list_field in ratapi.outputs.results_fields["list_fields"]:
        for a, b in zip(getattr(actual_results, list_field), getattr(expected_results, list_field)):
            assert (a == b).all()

    for list_field in ratapi.outputs.results_fields["double_list_fields"]:
        actual_list = getattr(actual_results, list_field)
        expected_list = getattr(expected_results, list_field)
        assert len(actual_list) == len(expected_list)
        for i in range(len(actual_list)):
            for a, b in zip(actual_list[i], expected_list[i]):
                assert (a == b).all()

    # Compare the final fields
    assert (actual_results.fitParams == expected_results.fitParams).all()
    assert actual_results.fitNames == expected_results.fitNames

    # Compare the two subclasses defined within the class
    assert actual_results.calculationResults.sumChi == expected_results.calculationResults.sumChi
    assert (actual_results.calculationResults.chiValues == expected_results.calculationResults.chiValues).all()

    for field in contrast_param_fields:
        assert (getattr(actual_results.contrastParams, field) == getattr(expected_results.contrastParams, field)).all()

    if isinstance(actual_results, ratapi.outputs.BayesResults) and isinstance(
        expected_results, ratapi.outputs.BayesResults
    ):
        check_bayes_fields_equal(actual_results, expected_results)


def check_bayes_fields_equal(actual_results, expected_results) -> None:
    """Compare two instances of the "BayesResults" object for equality.

    We focus here on the fields and subclasses specific to the Bayesian optimisation.
    """
    # The BayesResults object consists of a number of subclasses, each containing fields of differing formats.
    for subclass in ratapi.outputs.bayes_results_subclasses:
        actual_subclass = getattr(actual_results, subclass)
        expected_subclass = getattr(expected_results, subclass)

        for field in ratapi.outputs.bayes_results_fields["param_fields"][subclass]:
            assert getattr(actual_subclass, field) == getattr(expected_subclass, field)

        for field in ratapi.outputs.bayes_results_fields["list_fields"][subclass]:
            for a, b in zip(getattr(actual_subclass, field), getattr(expected_subclass, field)):
                assert (a == b).all()

        for field in ratapi.outputs.bayes_results_fields["double_list_fields"][subclass]:
            actual_list = getattr(actual_subclass, field)
            expected_list = getattr(expected_subclass, field)
            assert len(actual_list) == len(expected_list)
            for i in range(len(actual_list)):
                for a, b in zip(actual_list[i], expected_list[i]):
                    assert (a == b).all()

        # Need to account for the arrays that are initialised as "NaN" in the compiled code
        for array in ratapi.outputs.bayes_results_fields["array_fields"][subclass]:
            actual_array = getattr(actual_subclass, array)
            expected_array = getattr(expected_subclass, array)
            for i in range(len(actual_array)):
                assert (actual_array == expected_array).all() or (
                    ["NaN" if np.isnan(el) else el for el in actual_array[i]]
                    == ["NaN" if np.isnan(el) else el for el in expected_array[i]]
                )

    assert (actual_results.chain == expected_results.chain).all()
