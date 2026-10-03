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
        html.H6(children='Enter starting numbers:',
                style={'position': 'absolute',
                       'top': '8px',
                       'left': '0px',
                       'font-family': ['Arial', 'sans-serif']}),
        dcc.Input(id='starting_numbers_input',
                  type='text',
                  placeholder='e.g. 4,5,7,21,22,25',
                  debounce=True,
                  autoFocus=True,
                  autoComplete='off',
                  style={'position': 'absolute',
                         'top': '0px',
                         'left': '180px',
                         'width': 'min(calc(100% - 140px), 512px)',
                         '--Dash-Fill-Interactive-Strong': '#02808A'}),
        html.H6(children='Enter target number:',
                style={'position': 'absolute',
                       'top': '68px',
                       'left': '0px',
                       'font-family': ['Arial', 'sans-serif']}),
        dcc.Input(id='target_number_input',
                  type='text',
                  placeholder='e.g. 470',
                  debounce=True,
                  autoComplete='off',
                  style={'position': 'absolute',
                         'top': '60px',
                         'left': '180px',
                         'width': 'min(calc(100% - 140px), 512px)',
                         '--Dash-Fill-Interactive-Strong': '#02808A'}),
        html.H6(children='Solutions:',
                style={'position': 'absolute',
                       'top': '128px',
                       'left': '0px',
                       'font-family': ['Arial', 'sans-serif']}),
        html.Div(id='output_panel', 
                 children='Testing, testing',
                 style={'position': 'absolute',
                        'top': '168px',
                        'left': '0px',
                        'height': '512px',
                        'width': 'min(100%, 800px)',
                        'backgroundColor': '#EEEEEE',
                        'fontSize': 24}),
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
