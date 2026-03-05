import pytest

from src.services.mesh_analyzer import MeshAnalyzer


def test_calcular_corrientes_returns_expected_shapes():
    I1, I2, I3, A, B = MeshAnalyzer.calcular_corrientes(
        R1=2.0,
        R2=4.0,
        R3=3.0,
        R4=6.0,
        R5=5.0,
        R6=2.0,
        V1=12.0,
        V2=0.0,
        V3=0.0,
    )

    assert isinstance(I1, float)
    assert isinstance(I2, float)
    assert isinstance(I3, float)
    assert A.shape == (3, 3)
    assert B.shape == (3,)


def test_calcular_corrientes_rejects_invalid_voltage_range():
    with pytest.raises(ValueError):
        MeshAnalyzer.calcular_corrientes(
            R1=2.0,
            R2=4.0,
            R3=3.0,
            R4=6.0,
            R5=5.0,
            R6=2.0,
            V1=501.0,
            V2=0.0,
            V3=0.0,
        )


def test_interpretar_corrientes_returns_all_meshes():
    result = MeshAnalyzer.interpretar_corrientes(0.5, -2.0, 12.0)

    assert set(result.keys()) == {"I1", "I2", "I3"}
    assert "Sala/Comedor" in result["I1"]
