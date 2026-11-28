"""Dash web application to visualize the salary explorations.

Usage: uv run python dash_app.py, then open http://127.0.0.1:8050/
"""

import dash
import dash_bootstrap_components as dbc
import plotly.express as px

from salary_exploration.exploration import (
    get_all_explorations,
    get_country_job_salary_transformed,
)

EXTERNAL_STYLESHEETS = [
    {
        "href": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
        "crossorigin": "anonymous",
    },
    {
        "href": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp",
        "crossorigin": "anonymous",
    },
]


def create_app() -> dash.Dash:
    """Create the app: a navigation bar, an exploration picker and the salary graph."""
    app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
    app.layout = dash.html.Div(
        [_navbar(), _header(get_all_explorations()), dash.html.Div(id="results")],
        className="container",
    )
    app.callback(dash.Output("results", "children"), dash.Input("dropdown", "value"))(salary_graph)
    return app


def salary_graph(date_string: str | None) -> dash.dcc.Graph | None:
    """Bar chart of the euro salaries of one exploration, by job and country."""
    if date_string is None:
        return None
    salaries = get_country_job_salary_transformed(date_string)
    figure = px.bar(salaries, x="Job", y="Euro Salary", color="Country", barmode="group")
    return dash.dcc.Graph(id="salary-country-graph", figure=figure)


def _navbar() -> dbc.Nav:
    links = dash.html.Ul(
        [
            dash.html.Li(
                dash.html.A("Github", href="https://github.com/simonerigoni/salary_exploration")
            ),
            dash.html.Li(dash.html.A("Payscale", href="https://www.payscale.com/")),
        ],
        className="nav navbar-nav",
    )
    brand = dash.html.A("Salary Exploration", href="/", className="navbar-brand")
    return dbc.Nav(
        dash.html.Div(
            [
                dash.html.Div(brand, className="navbar-header"),
                dash.html.Div(links, className="collapse navbar-collapse"),
            ],
            className="container",
        ),
        className="navbar navbar-inverse navbar-fixed-top",
    )


def _header(explorations: list[str]) -> dash.html.Div:
    """Title and a dropdown to pick the exploration, the newest selected."""
    newest = explorations[-1] if explorations else None
    return dash.html.Div(
        dash.html.Div(
            [
                dash.html.H1("Salary Exploration", className="text-center"),
                dash.html.P("Visualize salary information from Payscale", className="text-center"),
                dash.html.Hr(),
                dash.dcc.Dropdown(explorations, newest, id="dropdown"),
            ],
            className="container",
        ),
        className="jumbotron",
    )


if __name__ == "__main__":
    create_app().run(debug=True)
