''' Implements functionality for creating repo specific readme files from metadata
'''
import logging
from yaml import load
from jinja2 import Environment, PackageLoader
import os
import codecs

from .book import Book

def readme(book_repo):
	''' Accepts a GITenberg book repository name and creates a readme from metadata'''

	if isinstance(book_repo, Book):
		readme_maker = Readme(book_repo.local_path) #use the formatting in book class
		message = readme_maker.createReadme()
		logging.debug(message)

	else:
		readme_maker = Readme(book_repo)
		message = readme_maker.createReadme()
		logging.info(message)


class Readme(object):
	''' An object for creating readme files from repository metadata '''

	def __init__(self, repo_path):

		self.repo_path = repo_path
		package_loader = PackageLoader('gitenberg', 'templates')
		self.env = Environment(loader=package_loader)
		self.metadata = self.getYAML(os.path.join(self.repo_path, 'metadata.yaml'))

	def getYAML (self, yaml=None):
		''' returns a dictionary from a yaml file '''

		#make sure a path exists to the repository
		if os.path.exists(yaml):
			#load the yaml; let open deal with errors
			with open(yaml, 'r') as iFile:
				return load(iFile.read())

		#No repository
		else:
			raise IOError("Cannot locate {0}".format(yaml))

	def createReadme(self):
		''' Create new readme file '''

		template = self.env.get_template('README.rst.j2')

		readme_text = template.render(
				author=self.metadata['creator']['author']['agent_name'],
				title=self.metadata['title'],
				bookid=self.metadata['identifiers']['gutenberg']
			)

		readme_path = os.path.join(self.repo_path, 'README.rst')

		with codecs.open(readme_path, 'w', 'utf-8') as readme_file:
			readme_file.write(readme_text)