class BarGraph():
	def __init__(self):
		print("Bargraph initialized")
		self._data = []
		self._max_data_count = 10
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
		new_value = 20
		self._data.insert(0, new_value) 

	def draw(self, context):
		self._update()
		context.set_source_rgba(0.0,1.0,0.0,1.0)
		
		base = self.bounds['y'] + self.bounds['h']
		line_width = (self.bounds['x'] - (self.bar_spacing * self._max_data_count - 1)) # / self._max_data_count
		print(str(line_width))

		increment = line_width + self.bar_spacing		

		context.set_line_width(line_width)
		start = self.bounds['x'] + line_width / 2

		print("start: "+str(start)+", width: "+str(line_width)+", base: "+str(base)+", inc="+str(increment))

		for index, value in enumerate(self._data):
			x = start + index * increment
			h = value / self.max_data_value * self.bounds['h']
			context.move_to(x, base)
			context.line_to(x, base - h)
			print(str(index)+": "+str(h))

		context.stroke()
			
		#context.rectangle(10,10,200,200)
		#context.fill()
		#print('+')
