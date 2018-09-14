import cairo
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk	
from gi.repository import Gdk	
from gi.repository import GLib

import BarGraph

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
		self.widgets.append(BarGraph.BarGraph())	

	def draw(self, widget, context):
		context.set_source_rgba(0.0,0.0,0.0,0.9)
		context.set_operator(cairo.OPERATOR_SOURCE)
		context.paint()
		context.set_operator(cairo.OPERATOR_OVER)

		for widget in self.widgets:
			widget.draw(context)

TransparentWindow()
Gtk.main()		 
