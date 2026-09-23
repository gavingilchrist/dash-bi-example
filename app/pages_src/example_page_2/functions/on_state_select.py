from dashblox.run import set_trigger
from utils import haversine


@set_trigger('state_select.value')
def populate_results_table(self):
    """
    Return data for results table - 10 closest states to selected state
    """
    selection = self.app_state['state_select.value']
    if selection is not None:
        state_latlong = self.source_data['state_locs']
        xtab = (state_latlong[['lat', 'long']]
                    .merge(state_latlong.query(f"state_name == '{selection}'")
                               [['lat', 'long']], 
                           how='cross'))
        state_latlong['dist'] = xtab.apply(lambda x: haversine(*x), axis=1)
        results = (state_latlong
                       .sort_values(by='dist')
                       .reset_index(drop=True))[1:11]
        self.app_state['closest_states_table.data'] = results
