from dashblox.run import set_trigger
import os
import dotenv
import pandas as pd


@set_trigger('ON_ENTRY')
def data_prep(self):
    """
    Extract and prepare source data, dropdown selector on arriving at page.
    """
    self.source_data.add('state_locs', read=read_state_locs)
    options = self.source_data['state_locs']['state_name'].tolist()
    self.app_state['state_select.options'] = options


def read_state_locs():
    """
    Download (if needed) and read in state coordinate dataset.
    """
    if not os.path.isfile('./data/statelatlong.csv'):
        if 'KAGGLE_API_TOKEN' not in os.environ:
            dotenv.load_dotenv()
        import kaggle
        kaggle.api.dataset_download_files('washimahmed/usa-latlong-for-state-abbreviations',
                                          './data', force=True, unzip=True)
    
    state_locs = (pd.read_csv('./data/statelatlong.csv')
                  .rename(columns={'State': 'state_code', 
                                   'Latitude': 'lat', 
                                   'Longitude': 'long', 
                                   'City': 'state_name'})
                  .sort_values(by='state_name')
                  .reset_index(drop=True))
    # (Fix Washington error)
    state_locs.loc[state_locs['state_code'] == 'WA', 
                   ['lat', 'long']] = [[47.554837, -120.607316]]
    
    return state_locs