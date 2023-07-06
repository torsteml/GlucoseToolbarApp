from pydexcom import Dexcom
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3


def get_authenticated_client():
    return Dexcom(os.getenv("DEXCOM_USERNAME", default=None), os.getenv("DEXCOM_PASSWORD", default=None), ous=True)


class GlucoseToolbarApp():

    def __init__(self):
        self.bg = None
        self.dexcom_client = get_authenticated_client()

        self.indicator = AppIndicator3.Indicator.new(
            "glucose",
            "path to icon",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = Gtk.Menu()

        self.display_glucose()
        menu_item = Gtk.MenuItem(label=self.title)
        menu_item.connect("activate", self.update_glucose)
        menu.append(menu_item)
        exit_item = Gtk.MenuItem(label="Exit")
        exit_item.connect("activate", self.on_exit_clicked)
        menu.append(exit_item)
        menu.show_all()

        return menu

    def on_exit_clicked(self, widget):
        Gtk.main_quit()

    def update_glucose(self, widget):
        self.bg = self.dexcom_client.get_current_glucose_reading()


    def display_glucose(self):
        if self.bg is not None:
            if self.bg.mmol_l < 14 or self.bg.mmol_l > 3:
                self.title = f"{self.bg.mmol_l} {self.bg.trend_arrow}"
            if self.bg.mmol_l >= 14 or self.bg.mmol_l <= 3:
                self.title = f"{self.bg.mmol_l} {self.bg.trend_arrow}"
        else:
            self.title = f"Unable to fetch glucose"


if __name__ == '__main__':
    app = GlucoseToolbarApp()
    Gtk.main()
