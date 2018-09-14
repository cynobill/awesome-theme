from random import randint
import cairo 

class BarGraph():
	def __init__(self):
		print("Bargraph initialized")
		self._data = []
		self._source = None

		self._max_data_count = 5
		self.max_data_value = 100
		self.bounds = {
			'x': 50,
			'y': 50,
			'w': 300,
			'h': 80
		}
		self.bar_spacing = 5
		
	def _update(self):
		if len(self._data) >= self._max_data_count:
			self._data.pop(-1)
		new_value = randint(0,100)
		self._data.insert(0, new_value) 
	
	def _get_source(self):
		if self._source == None:
			self._source = cairo.LinearGradient(self.bounds['x'],
							self.bounds['y']+self.bounds['h'],
							self.bounds['x'],							 self.bounds['y'])

		self._source.add_color_stop_rgba(0.0,0.0,1.0,0.0,1.0)
		self._source.add_color_stop_rgba(1.0,1.0,0.0,0.0,1.0)
		return self._source

	def draw(self, context):
		self._update()
		src = self._get_source()
		
		context.set_source_rgba(0.0,1.0,0.0,1.0)
		context.set_source(src)
		
		base = self.bounds['y'] + self.bounds['h']
		line_width = (self.bounds['w'] - (self.bar_spacing * (self._max_data_count - 1)))  / self._max_data_count

		increment = line_width + self.bar_spacing		

		context.set_line_width(line_width)
		start = self.bounds['x'] + line_width / 2

		for index, value in enumerate(self._data):
			x = start + index * increment
			h = value / self.max_data_value * self.bounds['h']
			context.move_to(x, base)
			context.line_to(x, base - h)

		context.stroke()
		
		context.set_source_rgba(0.0,0.0,1.0,1.0)	
		context.set_line_width(1)
		context.rectangle(self.bounds['x'],
				  self.bounds['y'],
				  self.bounds['w'],
				  self.bounds['h'])
		context.stroke()
		#print('+')
