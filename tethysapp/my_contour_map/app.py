from tethys_sdk.base import TethysAppBase


class MyContourMap(TethysAppBase):
    """
    Tethys app class for My Contour Map.
    """

    name = 'My Contour Map'
    description = ''
    package = 'my_contour_map'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'my-contour-map'
    color = '#c23616'
    tags = ''
    enable_feedback = False
    feedback_emails = []