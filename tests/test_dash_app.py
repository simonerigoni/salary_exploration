import dash
import pytest

import dash_app


@pytest.fixture
def project_folder(tmp_path, monkeypatch):
    """Run the test from a project folder with one exploration."""
    monkeypatch.chdir(tmp_path)
    folder = tmp_path / "data" / "20200101T000000Z"
    folder.mkdir(parents=True)
    (folder / "country_job_salary_transformed.csv").write_text(
        "Country,Job,Local Currency Salary,Euro Salary\nItaly,Data Engineer,€1000,1000.0\n",
        encoding="utf-8",
    )
    return tmp_path


def _find(component, component_id):
    """Find a component by id anywhere in the layout."""
    if getattr(component, "id", None) == component_id:
        return component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            found = _find(child, component_id)
            if found is not None:
                return found
    return None


def test_create_app_selects_the_last_exploration(project_folder):
    app = dash_app.create_app()

    assert isinstance(app, dash.Dash)
    dropdown = _find(app.layout, "dropdown")
    assert dropdown.options == ["20200101T000000Z"]
    assert dropdown.value == "20200101T000000Z"


def test_salary_graph_shows_the_selected_exploration(project_folder):
    graph = dash_app.salary_graph("20200101T000000Z")

    assert graph is not None
    figure = graph.to_plotly_json()["props"]["figure"]
    assert list(figure.data[0].x) == ["Data Engineer"]


def test_salary_graph_is_empty_without_a_selection(project_folder):
    assert dash_app.salary_graph(None) is None
