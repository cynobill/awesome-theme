import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def draw(da,ctx): 
  print(".") 

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)

drawing_area = Gtk.DrawingArea()
win.add(drawing_area)
drawing_area.connect("draw", draw)

win.show_all()
Gtk.main()


