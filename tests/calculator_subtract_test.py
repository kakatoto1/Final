from calculator import Calculator

def test_calculator_subtract_method():
    calculator = Calculator()
    assert calculator.subtract(1) == -1
