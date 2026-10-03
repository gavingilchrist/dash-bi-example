from dashblox.run import set_trigger


@set_trigger('starting_numbers_input.value')
def validate_starting_numbers(self):
    """
    Check input starting numbers, save in Store.
    """
    rawnums = self.app_state['starting_numbers_input.value']
    nums, nums_txt = nums_from_text(rawnums)
    
    self.app_state['starting_numbers.data'] = nums
    self.app_state['starting_numbers_input.value'] = nums_txt
    
    if nums:
        nextfocus = (f'{self.cmpfx}target_number_input'
                     if self.app_state['target_number.data'].empty
                     else 'READY')
        self.app_state['nextfocus.data'] = [{'nf': nextfocus}]


@set_trigger('target_number_input.value')
def validate_target_number(self):
    """
    Check input target number, save in Store.
    """
    rawnums = self.app_state['target_number_input.value']
    nums, nums_txt = nums_from_text(rawnums)

    tgt = nums if len(nums)==1 else []
    if tgt==[]:  nums_txt = ''
    self.app_state['target_number.data'] = tgt
    self.app_state['target_number_input.value'] = nums_txt
    
    if nums:
        nextfocus = (f'{self.cmpfx}starting_numbers_input'
                     if self.app_state['starting_numbers.data'].empty
                     else 'READY')
        self.app_state['nextfocus.data'] = [{'nf': nextfocus}]

        
def nums_from_text(rawnums):
    """
    Extract numbers (integers) from input text, treating all non-numeric
    characters as delimiters.  Return as DF records and space-delimited string.
    """
    nums = [{'num': int(j)} 
            for j in ''.join([[' ',i][47<ord(i)<58] 
                              for i in (rawnums or [])]).split()
            if j]
    return nums, ' '.join([str(i['num']) for i in nums])
    

@set_trigger('nextfocus.data', clientside=True)
def shift_focus():
    """
    Effect change in focus required after entering an input.
    """
    return {'js': shift_focus_js,
            'input': 'nextfocus.data',
            'output': 'dummy_store.data'}
    
    
shift_focus_js = """
function(nfjson) {
    const nextFocus = nfjson[0]['nf']
    if (nextFocus !== 'READY') {
        const nextInput = document.getElementById(nextFocus);
        if (nextInput) {
            nextInput.focus();
        }
    } else {
        document.activeElement.blur();
    }
    return dash_clientside.no_update;
}
"""
