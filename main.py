from subprocess import run, TimeoutExpired

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

BATTERY_RAW_SOC = "/sys/class/power_supply/battery/batt_read_raw_soc"


class BatteryPrecisionApp(App):
    def build(self):
        self.title = "SMARTCHARGR"
        Window.clearcolor = (0.035, 0.065, 0.10, 1)

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(14),
        )

        title = Label(
            text="SMARTCHARGR",
            font_size=sp(24),
            bold=True,
            color=(0.35, 0.85, 1, 1),
            size_hint_y=None,
            height=dp(52),
        )
        self.value_label = Label(
            text="--.--%",
            font_size=sp(58),
            bold=True,
            color=(0.92, 0.98, 1, 1),
        )
        self.state_label = Label(
            text="Checking root access...",
            font_size=sp(15),
            color=(0.55, 0.72, 0.82, 1),
            size_hint_y=None,
            height=dp(48),
        )
        self.note_label = Label(
            text="Live reading from Samsung fuel-gauge sysfs",
            font_size=sp(12),
            color=(0.45, 0.60, 0.70, 1),
            size_hint_y=None,
            height=dp(42),
        )

        root.add_widget(title)
        root.add_widget(self.value_label)
        root.add_widget(self.state_label)
        root.add_widget(self.note_label)

        Clock.schedule_interval(self.refresh_reading, 1.0)
        self.refresh_reading(0)
        return root

    def read_raw_soc(self):
        try:
            result = run(
                ["su", "-c", f"cat {BATTERY_RAW_SOC}"],
                capture_output=True,
                text=True,
                timeout=4,
                check=False,
            )
        except FileNotFoundError:
            return None, "su command not found"
        except TimeoutExpired:
            return None, "Root request timed out"
        except Exception as exc:
            return None, str(exc)

        if result.returncode != 0:
            message = result.stderr.strip() or "Root access denied"
            return None, message

        try:
            raw = int(result.stdout.strip())
        except (TypeError, ValueError):
            return None, "Invalid fuel-gauge value"

        return raw, None

    def refresh_reading(self, _dt):
        raw, error = self.read_raw_soc()
        if error:
            self.value_label.text = "--.--%"
            self.state_label.text = f"ROOT / SENSOR: {error}"
            return

        # Samsung batt_read_raw_soc has been observed at 100 units per 1%.
        # Formatting to 2 decimals does not imply 0.01% measurement accuracy.
        percent = raw / 100.0
        self.value_label.text = f"{percent:.2f}%"
        self.state_label.text = f"Fuel-gauge raw value: {raw}"


if __name__ == "__main__":
    BatteryPrecisionApp().run()
