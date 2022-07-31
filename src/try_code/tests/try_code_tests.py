
from try_code.employe import Employe
from pytest import MonkeyPatch
import pytest


def test_set_employe_by_console( monkeypatch: MonkeyPatch) -> None:
    employe = Employe('Rulo', 'leader', 'rulo@be.com')

    inputs = ['Ruben', 'programmer', 'ruben@gmail.com']
    monkeypatch.setattr( 'builtins.input',lambda _: inputs.pop(0) )
                                    
    employe.set_attributes_by_console()

    assert employe.name == 'Ruben' and  employe.role == 'programmer' and employe.email == 'ruben@gmail.com'






