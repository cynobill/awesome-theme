import cairo
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk	
from gi.repository import Gdk	
from gi.repository import GLib

import BarGraph
import psutil

def get_cpu():
	return psutil.cpu_percent()

class TransparentWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)

		self.connect("destroy", Gtk.main_quit)
		self.connect("draw", self.draw)
		
		screen = self.get_screen()
		visual = screen.get_rgba_visual()
		if visual and screen.is_composited():
			self.set_visual(visual)

		self.__create_widgets()

                #set timer to redraw ui
		GLib.timeout_add(1000, self.__draw_timer)

		self.set_app_paintable(True)
		self.show_all()

	def __draw_timer(self):
		self.queue_draw()
		return True

	def __create_widgets(self):
		self.widgets = []
		self.widgets.append(BarGraph.BarGraph({	'x': 30,
							'y': 100,
							'h': 60,
							'w': 500,
							'data_points': 50,
							'max_data_value': 100,
							'draw_upwards': True,
							'draw_to_right': True,
							'line_caps': BarGraph.BOTH,
							'fade_start': 0.75,
							'bar_spacing': 0.25,
							'pattern_colors': [[0.0,0.0,1.0,1.0,1.0],
									   [0.5,1.0,1.0,0.0,1.0],
									   [1.0,1.0,0.0,1.0,1.0]],
							'border_width': 1,
							'border_color': [1.0,1.0,0.0,1.0],
							'data_callback': get_cpu}))	

	def draw(self, widget, context):
		context.set_source_rgba(0.0,0.0,0.0,0.9)
		context.set_operator(cairo.OPERATOR_SOURCE)
		context.paint()
		context.set_operator(cairo.OPERATOR_OVER)

		for widget in self.widgets:
			widget.draw(context)

TransparentWindow()
Gtk.main()		 
