from dashblox.run import set_trigger


@set_trigger('nextfocus.data')
def find_solutions(self):
    """
    Calculate and report back solutions.
    """
    nums = self.app_state['starting_numbers.data']
    tgt = self.app_state['target_number.data']
    
    if (z:=self.app_state['nextfocus.data']).shape[0] and z.iloc[0,0] == 'READY':
        self.app_state['output_panel.children'] = 'Ready to solve'
