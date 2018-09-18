from random import randint
import cairo 

NONE = 0
TOP = 1
BOTTOM = 2
BOTH = 3

class BarGraph():
	#############################################################
	#args:
	#  (int) x: x coord of the top left of the widget, default = 0
	#  (int) y: y coord of the top left of the widget, default = 0
	#  (int) w: width of the widget, default = 200
	#  (int) h: height of the widget, default = 60
	#  (int) data_points: how many data points to display, default = 10
	#  (float) max_data_value: largest value the graph will display, default = 100
	#			   if == None then we will calc on the fly
	#  (boolean) draw_to_right: animate bars left to right, default = True
        #  (boolean) draw_upwards: bars grow upwards, default = True
	#  (int) line_caps: how to round the ends of the bars, default = NONE
	#			NONE,TOP,BOTTOM,BOTH
	#  (float) fade_start: where does the graph start fading out, default = 0.75
	#			as percentage of the bar (0.0-1.0)
	#  (float) bar_spacing: how big is the gap between bars, default = 0.2
	#			as percentage of the bars width (0.0-1.0)
	#############################################################
	def __init__(self, args):
		self._data = []

		try:
			self.x = args['x']
		except:
			self.x = 0
	
		try:
			self.y = args['y']
		except:
			self.y = 0

		try:
			self.w = args['w']
		except:
			self.w = 200

		try:
			self.h = args['h']
		except:
			self.h = 60

		try:
			assert( args['data_points']) > 0
			self.data_points = args['data_points']
		except:                     	
			self.data_points = 20
     		
		
		try:	
			assert args['max_data_value'] == None or args['max_data_value'] > 0
			if args['max_data_value'] == None:
				self.calc_max_data_value = True
				self.max_data_value = 0 
			else:
				self.calc_max_data_value = False
				self.max_data_value = args['max_data_value']
		except:
			self.calc_max_data_value = False
			self.max_data_value = 100
		
		
		try:
			self.draw_upwards = args['draw_upwards']
		except:
			self.draw_upwards = True


		try:
			self.draw_to_right = args['draw_to_right']
		except:
			self.draw_to_right = True

		try: 
			assert (args['line_caps'] == NONE or
				args['line_caps'] == TOP or
				args['line_caps'] == BOTTOM or
				args['line_caps'] == BOTH)
			self.line_caps = args['line_caps']
		except:
			self.line_caps = NONE

		try:
			assert (args['fade_start'] >= 0 and
				args['fade_start'] <= 1.0)
			self.fade_start  = args['fade_start']
		except:
			self.fade_start = 0.75

		try:
			assert (args['bar_spacing'] >= 0)
			self.bar_spacing = args['bar_spacing']
		except:
			self.bar_spacing = 0.2

		try:
			assert (args['border_width'] >= 0)
			self.border_width = args['border_width']
		except: 
			self.border_width = 0

		try:
			self.border_color = args['border_color']
		except:
			self.border_color = [0.0,0.0,0.0,0.0]

		try:	
			self.pattern_colors = args['pattern_colors']
		except:
			self.pattern_colors = [	[0.0,0.0,1.0,0.0,1.0],
						[0.5,1.0,1.0,0.0,1.0],
						[1.0,1.0,0.0,0.0,1.0]]

		self.data_callback = args['data_callback']

		print("Bargraph initialized:")
		print("  x: "+str(self.x))
		print("  y: "+str(self.y))
		print("  w: "+str(self.w))
		print("  h: "+str(self.h))
		print("  data_points: "+str(self.data_points))
		print("  max_data_value: "+str(self.max_data_value))
		print("  calc_max_value: "+str(self.calc_max_data_value))
		print("  draw_right: "+str(self.draw_to_right))
		print("  draw_up: "+str(self.draw_upwards))
		print("  line_caps: "+str(self.line_caps))
		print("  fade_start: "+str(self.fade_start))
		print("  bar_spacing: "+str(self.bar_spacing))
		print("  pattern_colors: "+str(self.pattern_colors))
		print("  border_width: "+str(self.border_width))
		print("  border_color: "+str(self.border_color))
	
	def _update(self):
		if len(self._data) >= self.data_points:
			value = self._data.pop(-1)
			if self.calc_max_data_value and value >= self.max_data_value:
				self.max_data_value = self._calculate_max_data_value()

		new_value = self.data_callback() #randint(0,100)
		self._data.insert(0, new_value) 

		if new_value > self.max_data_value:
			self.max_data_value = new_value			


	def _calculate_max_data_value(self):
		max = 0
		for value in self._data:
			if value > max: max = value

		return max


	def _get_source(self, context):
		pattern = cairo.LinearGradient(0.5, 0.0, 0.5, 1.0)

		for color in self.pattern_colors:
			pattern.add_color_stop_rgba(color[0],color[1],color[2],color[3],color[4])	

		mask = cairo.LinearGradient(0.0, 0.5, 1.0, 0.5)

		mask.add_color_stop_rgba(0.0,1.0,1.0,1.0,1.0)
		mask.add_color_stop_rgba(self.fade_start,1.0,1.0,1.0,1.0)
		mask.add_color_stop_rgba(1.0,1.0,1.0,1.0,0.0)

		context.push_group()
		context.set_source(pattern)
		context.mask(mask)
		return context.pop_group()


	def _calc_bar_width(self):		
		return 1.0 / (self.data_points +  (self.data_points - 1) * self.bar_spacing)


	def _setup_context(self, context):		
		# enable line caps
		if not self.line_caps == NONE:
			context.set_line_cap(cairo.LINE_CAP_ROUND)

		# move origin to the top left of the widget
		context.translate(self.x,self.y)

		# normalize coordinate system to the widget area
		context.scale(self.w,self.h)

		# if bars grow upwards we flip and translate y axis
		if self.draw_upwards:
			context.scale(1.0,-1.0)
			context.translate(0.0,-1.0)
		
		# if animating to the left flip and translate x axis
		if not self.draw_to_right:
			context.scale(-1.0,1.0)
			context.translate(-1.0,0.0)
		
		# confine drawing to the widget		
		#context.rectangle(0.0,0.0,1.0,1.0)
		#context.clip()		

		line_w = self._calc_bar_width()
		
		# shift base of graph up to show line cap and base
		if self.line_caps == BOTTOM or self.line_caps == BOTH:
			context.translate(0.0, (line_w /2.0))

		# adjust scale so graph is normalized but will not clip line caps
		if self.line_caps == BOTTOM or self.line_caps == TOP:
			context.scale(1.0, 1.0 - (line_w /2.0) )
		elif self.line_caps == BOTH:
			context.scale(1.0, 1.0 - line_w )

		


	def draw(self, context):
		context.save()

		# draw border
		if self.border_width > 0:
			context.set_source_rgba(self.border_color[0],
						self.border_color[1],
						self.border_color[2],
						self.border_color[3])
			context.set_line_width(self.border_width)
			context.rectangle(	self.x,
						self.y,
						self.w,
						self.h)
			context.stroke()

		self._setup_context(context)
		self._update()

		line_width = self._calc_bar_width()
		spacer = (1.0 - line_width * self.data_points) / (self.data_points -1)
		increment = line_width + spacer

		start = line_width / 2

		for index, value in enumerate(self._data):
			x = start + index * increment
			h = value / self.max_data_value
			context.move_to(x, 0)
			context.line_to(x, h)

		context.set_line_width(line_width)
		context.set_source(self._get_source(context))       	
		context.stroke()
		context.restore()
