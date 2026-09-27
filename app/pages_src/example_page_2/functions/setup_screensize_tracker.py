from dashblox.run import set_trigger


@set_trigger('ON_ENTRY', clientside=True)
def setup_screensize_tracker():
    """
    Add client-side event listener to report back on any changes to screen size
    """
    return {'js': JAVASCRIPT_TXT,
            'input': ['ON_ENTRY'],
            'output': 'dummy_store.data'}


JAVASCRIPT_TXT = """
    function(init) {
        // Function to push the window size into Dash's component system
        function updateSize() {
            const width = window.innerWidth || document.documentElement.clientWidth;
            const height = window.innerHeight || document.documentElement.clientHeight;
            
            // Setting a custom property or directly modifying a Dash store element
            // We use a custom event or directly set the value if hooked into an output
            dash_clientside.set_props("window_dimensions", {data: [{width: width, height: height}]});
        }

        // Add the listener for real-time resizing
        window.addEventListener('resize', updateSize);
        
        // Trigger once immediately on page load
        updateSize();
        
        return dash.no_update;
    }
    """
