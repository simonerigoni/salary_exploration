# Dash Salary Exploration application
#
# python dash_salary_exploration.py


import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


import salary_exploration


EXTERNAL_STYLESHEETS = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    },
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp',
        'crossorigin': 'anonymous'
    }
]


def _create_app():
    ''' 
    Creates dash application

    Parameters:
        None
        
    Returns:
        app (dash.Dash): Dash application
    '''

    app = dash.Dash(__name__, external_stylesheets = EXTERNAL_STYLESHEETS)

    df = salary_exploration.get_country_job_salary_transformed()

    fig = px.bar(df, x = 'Job', y = 'Euro Salary', color = 'Country', barmode = 'group')

    app.layout = dash.html.Div(
        [
            dbc.Nav(
                [
                    dash.html.Div(
                        [
                            dash.html.Div(
                                [
                                    dash.html.A('Salary Exploration', href='/', className = 'navbar-brand' )
                                ], className = 'navbar-header')
                            , dash.html.Div(
                                [
                                    dash.html.Ul(
                                        [
                                            dash.html.Li(dash.html.A('Github', href='https://github.com/simonerigoni/salary_exploration'))
                                            , dash.html.Li(dash.html.A('Payscale', href='https://www.payscale.com/'))
                                        ], className = 'nav navbar-nav')
                                ], className = 'collapse navbar-collapse')
                        ], className = 'container')
                ], className = 'navbar navbar-inverse navbar-fixed-top')
            , dash.html.Div(
                [
                    dash.html.Div(
                        [
                            dash.html.H1('Salary Exploration', className='text-center')
                            , dash.html.P('Visualize salary information from Payscale', className='text-center')
                            , dash.html.Hr()
                            , dash.dcc.Graph(
                                id = 'salary-country-graph',
                                figure = fig
                            )
                        ] , className = 'container')
                ], className = 'jumbotron')
            , dash.html.Div(id = 'results')
        ], className = 'container')

    return app


if __name__ == '__main__':
    app = _create_app()
    app.run_server(debug = True)
else:
    pass
