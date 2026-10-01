from dash import dcc, html
import dash_bootstrap_components as dbc
from dashblox.components import table


closest_states_table_cols = [
    ('state_code', {'label': 'Abbrev.', 'width': 80}),
    ('state_name', {'label': 'State', 'width': 160}),
    ('dist', {'label': 'Distance', 'width': 80, 'num_fmt': 'number-0'}),
]


layout = html.Div(
    [
        html.H6(children='State:',
                style={'position': 'absolute',
                       'top': '8px',
                       'left': '0px',
                       'font-family': ['Arial', 'sans-serif']}),
        dcc.Dropdown(id='state_select',
                     multi=False,
                     placeholder='Select State',
                     style={'position': 'absolute',
                            'top': '0px',
                            'left': '48px',
                            'width': 'min(calc(100% - 48px), 512px)',
                            'color': '#131417',
                            '--Dash-Fill-Interactive-Strong': '#02808A'}),
        table('closest_states_table',
              closest_states_table_cols,
              style={'top': '60px',
                     'left': '0px',
                     'bottom': '0px'},
              body_cell_style={'text-overflow': 'ellipsis'}),
        html.Div(id='display_dimensions', 
                 children='Testing, testing',
                 style={'position': 'absolute',
                        'top': '400px',
                        'fontSize': 24, 
                        'fontWeight': 'bold'}),
    ],
    style={'position': 'absolute',
           'top': '0px',
           'bottom': '0px',
           'left': '0px',
           'right': '0px',
           'text-align': 'left',
           'background-color': '#FFFFFF',
    }
)
