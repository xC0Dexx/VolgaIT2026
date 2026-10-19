from views.base_view import BrowserView

class AdvertisementView(BrowserView):
    ad = '#pum-1272'

    def wait_for_ad(self):
        return self.visible(self.ad)

    def dismiss(self):
        self.click(self.ad + ' .pum-close')
        self.wait_closed(self.ad)
