from pydexcom import Dexcom
import rumps
import os


def get_authenticated_client():
    return Dexcom(os.getenv("DEXCOM_USERNAME", default=None), os.getenv("DEXCOM_PASSWORD", default=None), ous=True)


class GlucoseToolbarApp(rumps.App):

    def __init__(self):
        super(GlucoseToolbarApp, self).__init__(name="GlucoseToolbarApp")

        self.bg = None
        self.dexcom_client = get_authenticated_client()

    @rumps.clicked("Force update")
    @rumps.timer(60)
    def update_glucose(self, sender):
        self.bg = self.dexcom_client.get_current_glucose_reading()

    @rumps.timer(1)
    def display_glucose(self, sender):
        if self.bg is not None:
            if self.bg.mmol_l < 14 or self.bg.mmol_l > 3:
                self.title = f"{self.bg.mmol_l} {self.bg.trend_arrow}"
            if self.bg.mmol_l >= 14 or self.bg.mmol_l <= 3:
                self.title = f"{self.bg.mmol_l} {self.bg.trend_arrow}"
        else:
            self.title = f"Unable to fetch glucose"


if __name__ == '__main__':
    GlucoseToolbarApp().run()
