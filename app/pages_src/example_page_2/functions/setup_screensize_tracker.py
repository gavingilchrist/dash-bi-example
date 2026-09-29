from dashblox.run import set_trigger
from dashblox.run.app_layout import GET_WINDOW_DIMS_JS


@set_trigger('ON_ENTRY', clientside=True)
def setup_screensize_tracker():
    """
    Add client-side event listener to report back on any changes to screen size
    """
    return {'js': GET_WINDOW_DIMS_JS,
            'input': ['ON_ENTRY'],
            'output': 'dummy_store.data'}
