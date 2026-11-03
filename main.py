from subprocess import run, TimeoutExpired

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from jnius import autoclass

BATTERY_RAW_SOC = "/sys/class/power_supply/battery/batt_read_raw_soc"
OVERLAY_REQUEST_CODE = 734

PythonActivity = autoclass("org.kivy.android.PythonActivity")
Settings = autoclass("android.provider.Settings")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")
WindowManager = autoclass("android.view.WindowManager")
WindowLayoutParams = autoclass("android.view.WindowManager$LayoutParams")
PixelFormat = autoclass("android.graphics.PixelFormat")
Gravity = autoclass("android.view.Gravity")
TextView = autoclass("android.widget.TextView")
Color = autoclass("android.graphics.Color")


class BatteryPrecisionApp(App):
    def build(self):
        self.title = "SMARTCHARGR"
        self.activity = PythonActivity.mActivity
        self.window_manager = self.activity.getSystemService(
            autoclass("android.content.Context").WINDOW_SERVICE
        )
        self.overlay_view = None
        self.overlay_params = None
        self.overlay_enabled = False

        Window.clearcolor = (0.035, 0.065, 0.10, 1)
        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(12))

        root.add_widget(Label(
            text="SMARTCHARGR", font_size=sp(24), bold=True,
            color=(0.35, 0.85, 1, 1), size_hint_y=None, height=dp(52)
        ))
        self.value_label = Label(
            text="--.--%", font_size=sp(58), bold=True,
            color=(0.92, 0.98, 1, 1)
        )
        root.add_widget(self.value_label)

        self.state_label = Label(
            text="Checking root access...", font_size=sp(14),
            color=(0.55, 0.72, 0.82, 1), size_hint_y=None, height=dp(48)
        )
        root.add_widget(self.state_label)

        self.overlay_button = Button(
            text="ENABLE FLOATING OVERLAY",
            size_hint_y=None, height=dp(54),
            background_normal="", background_color=(0.05, 0.48, 0.68, 1)
        )
        self.overlay_button.bind(on_release=self.toggle_overlay)
        root.add_widget(self.overlay_button)

        root.add_widget(Label(
            text="Overlay preview • Fast-charge detection is not enabled yet",
            font_size=sp(12), color=(0.55, 0.70, 0.78, 1),
            size_hint_y=None, height=dp(44)
        ))

        Clock.schedule_interval(self.refresh_reading, 1.0)
        self.refresh_reading(0)
        return root

    def read_raw_soc(self):
        try:
            result = run(
                ["su", "-c", f"cat {BATTERY_RAW_SOC}"],
                capture_output=True, text=True, timeout=4, check=False
            )
        except FileNotFoundError:
            return None, "su command not found"
        except TimeoutExpired:
            return None, "Root request timed out"
        except Exception as exc:
            return None, str(exc)

        if result.returncode != 0:
            return None, result.stderr.strip() or "Root access denied"
        try:
            return int(result.stdout.strip()), None
        except (TypeError, ValueError):
            return None, "Invalid fuel-gauge value"

    def refresh_reading(self, _dt):
        raw, error = self.read_raw_soc()
        if error:
            self.value_label.text = "--.--%"
            self.state_label.text = f"ROOT / SENSOR: {error}"
            if self.overlay_view is not None:
                self.overlay_view.setText("SMARTCHARGR  •  --.--%")
            return

        # Two decimal places are formatting; observed hardware steps were 0.10%.
        percent = raw / 100.0
        display = f"{percent:.2f}%"
        self.value_label.text = display
        self.state_label.text = f"Fuel-gauge raw value: {raw}"
        if self.overlay_view is not None:
            self.overlay_view.setText(f"⚡  {display}")

    def has_overlay_permission(self):
        return bool(Settings.canDrawOverlays(self.activity))

    def toggle_overlay(self, *_):
        if self.overlay_view is not None:
            self.remove_overlay()
            return
        if not self.has_overlay_permission():
            intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            intent.setData(Uri.parse("package:" + self.activity.getPackageName()))
            self.activity.startActivityForResult(intent, OVERLAY_REQUEST_CODE)
            self.state_label.text = "Allow SMARTCHARGR to display over other apps"
            return
        self.create_overlay()

    def create_overlay(self):
        try:
            self.overlay_view = TextView(self.activity)
            self.overlay_view.setText("⚡  --.--%")
            self.overlay_view.setTextSize(2, 18)
            self.overlay_view.setTextColor(Color.WHITE)
            self.overlay_view.setPadding(24, 14, 24, 14)
            self.overlay_view.setBackgroundColor(Color.rgb(10, 55, 78))

            width = WindowLayoutParams.WRAP_CONTENT
            height = WindowLayoutParams.WRAP_CONTENT
            overlay_type = WindowLayoutParams.TYPE_APPLICATION_OVERLAY
            flags = (
                WindowLayoutParams.FLAG_NOT_FOCUSABLE
                | WindowLayoutParams.FLAG_NOT_TOUCH_MODAL
                | WindowLayoutParams.FLAG_LAYOUT_IN_SCREEN
            )
            self.overlay_params = WindowLayoutParams(
                width, height, overlay_type, flags, PixelFormat.TRANSLUCENT
            )
            self.overlay_params.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL
            self.overlay_params.y = int(dp(36))
            self.window_manager.addView(self.overlay_view, self.overlay_params)
            self.overlay_button.text = "HIDE FLOATING OVERLAY"
            self.overlay_enabled = True
            self.state_label.text = "Floating overlay is active"
        except Exception as exc:
            self.overlay_view = None
            self.state_label.text = f"Overlay error: {exc}"

    def remove_overlay(self):
        try:
            if self.overlay_view is not None:
                self.window_manager.removeView(self.overlay_view)
        except Exception:
            pass
        self.overlay_view = None
        self.overlay_params = None
        self.overlay_enabled = False
        self.overlay_button.text = "ENABLE FLOATING OVERLAY"
        self.state_label.text = "Floating overlay is off"

    def on_resume(self):
        if self.overlay_view is None and self.has_overlay_permission():
            self.overlay_button.text = "ENABLE FLOATING OVERLAY"

    def on_stop(self):
        # Avoid leaving a detached overlay behind when Android stops the app.
        self.remove_overlay()


if __name__ == "__main__":
    BatteryPrecisionApp().run()
