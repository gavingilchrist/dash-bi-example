from dashblox.run import set_trigger


@set_trigger('window_dimensions.data')
def update_layout_from_size(self):
    """
    Update contents of display_dimensions component when display size change detected.
    """
    wdims = self.app_state['window_dimensions.data']
    if wdims is not None:
        d = wdims.iloc[0].to_dict()
        device_type = 'Desktop' if d['width'] > 992 else 'Mobile/Tablet'
        dtxt = f"Current Window: {d['width']}px width × {d['height']}px height ({device_type})"
        self.app_state['display_dimensions.children'] = dtxt