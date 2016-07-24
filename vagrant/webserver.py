from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header("Content-type", 'text/html')
					self.end_headers()

					output = ""
					output +="<html><body>"
					output +="<h1>"
					output +=myRestaurantQuery.name
					output +="</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/rest/%s/edit'>" % restaurantIDPath
					output += "<input name='newRestName' type='text' placeholder=%s>" % myRestaurantQuery.name
					output += "<input type='submit' value='Rename'></form>"
					output += "</body></html>"
					self.wfile.write(output)
			
			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header("Content-type", 'text/html')
					self.end_headers()

					output = ""
					output +="<html><body>"
					output +="<h1>Hey there! Do you want to actually delete restaurant called %s from your database?" % myRestaurantQuery.name
					output +="</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action='/rest/%s/delete'>" % restaurantIDPath
					# output += "<input name='newRestName' type='text' placeholder=%s>" % myRestaurantQuery.name
					output += "<input type='submit' value='Yes! Delete this restaurant'></form>"
					output += "</body></html>"
					self.wfile.write(output)


			if self.path.endswith("/rest"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header("Content-type", 'text/html')
				self.end_headers()

				output = ""
				output +="<html><body>"

				output += "<a href = '/rest/new'>Create New Restaurant</a></br>"
				for restaurant in restaurants:
					output += restaurant.name
					output += "</br>"
					output += "<a href= '/rest/%s/edit'>Edit</a>" % restaurant.id
					output += "</br>"
					output += "<a href= '/rest/%s/delete'>Delete</a>" % restaurant.id
					output += "</br>"

				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/rest/new"):
				self.send_response(200)
				self.send_header("Content-type", 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Enter Name of your New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/rest/new'>"
				output += "<input name='newRestName' type='text' placeholder='Enter New Restaurant name here...'>"
				output += "<input type='submit' value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return


			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header("Content-type", 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>HELLO!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What should I say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header("Content-type", 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>HOLACHEF IS DOOMED FROM THE START!<a href = '/hello'>Go Back to Hello Page</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What should I say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return	
		except IOError:
			self.send_error(404, "File is not available %s" % self.path)
		
	def do_POST(self):
		try:
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields = cgi.parse_multipart(self.rfile, pdict)									
					messagecontent = fields.get('newRestName')
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					myRestaurantQuery.name = messagecontent[0]
					session.add(myRestaurantQuery)
					session.commit()
				self.send_response(301)
				self.send_header("Content-type", 'text/html')
				self.send_header('Location', '/rest')
				self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				# if ctype == "multipart/form-data":
				# 	fields = cgi.parse_multipart(self.rfile, pdict)									
				# 	messagecontent = fields.get('newRestName')
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					# myRestaurantQuery.name = messagecontent[0]
					session.delete(myRestaurantQuery)
					session.commit()
				self.send_response(301)
				self.send_header("Content-type", 'text/html')
				self.send_header('Location', '/rest')
				self.end_headers()

			if self.path.endswith("/rest/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == "multipart/form-data":
					fields = cgi.parse_multipart(self.rfile, pdict)									
					messagecontent = fields.get('newRestName')

				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()
				self.send_response(301)
				self.send_header("Content-type", 'text/html')
				self.send_header('Location', '/rest')
				self.end_headers()


			# self.send_response(301)
			# self.end_headers()

			# ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			# if ctype == "multipart/form-data":
			# 	fields = cgi.parse_multipart(self.rfile, pdict)
			# 	messagecontent = fields.get('message')
			# 	output = ""
			# 	output += "<html><body>"
			# 	output += "<h2>How about this which is running in POST function?</h2>"
			# 	output += "<h1> %s </h1>" % messagecontent[0]

			# 	output += "<form method='POST' enctype='multipart/form-data' action='/hello2'><h2> Printing from POST: What should I say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			# 	output += "</body></html>"
			# 	self.wfile.write(output)
			# 	print output

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web Server up and running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, shutting down server ... dot dot dot ..."
		server.socket.close()


if __name__ == '__main__':
	main()