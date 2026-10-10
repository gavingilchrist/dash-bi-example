from dashblox.run import set_trigger
from utils import solve_digits


@set_trigger('nextfocus.data')
def find_solutions(self):
    """
    Calculate and report back solutions.
    """
    if not(z:=self.app_state['nextfocus.data']).empty and z.iloc[0,0] == 'READY':
        soln_nyt, soln_nerdle = solve_digits([*self.app_state['starting_numbers.data']['num']], 
                                             [*self.app_state['target_number.data']['num']])
        self.app_state['solution_nyt.data'] = soln_nyt
        self.app_state['solution_nerdle.data'] = soln_nerdle
        self.populate_solutions_table()        
        

@set_trigger('format_select.value')
def switch_format(self):
    """
    Respond to user toggling between solutions formats.
    """
    if not self.app_state['solution_nyt.data'].empty:
        self.populate_solutions_table()
        
        
def populate_solutions_table(self):
    """
    Populate solutions table with rows in selected format.
    """
    if self.app_state['format_select.value'] == 'NYT Digits':
        self.app_state['solutions_table.data'] = self.app_state['solution_nyt.data'].copy()
    else:
        self.app_state['solutions_table.data'] = self.app_state['solution_nerdle.data'].copy()
