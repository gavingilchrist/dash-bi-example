from dashblox.run import set_trigger


@set_trigger('_window_dimensions.data')
def update_layout_from_size(self):
    """
    Adjust layout where needed to account for screen size.
    """
    if not (wdims:=self.app_state['_window_dimensions.data']).empty:
        if int(wdims.loc[0,'width'][:-2]) < 432:
            self.app_state['format_select.inline'] = False
            ttop = {'top': '212px'}
        else:
            self.app_state['format_select.inline'] = True
            ttop = {'top': '180px'}
        self.app_state['solutions_table_div.style']\
            = {**self.app_state['solutions_table_div.style'], 
               **ttop}    
    