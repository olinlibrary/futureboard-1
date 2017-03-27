/*
To use, install casperjs (npm install -g casperjs) and run:
casperjs scrape.js <your_username> <your_password>

You should use a unique password for carpe!!!
*/

var casper = require('casper').create();
var base_url = 'https://lists.olin.edu/mailman/private/carpediem/';
var fs = require('fs');

casper.start(base_url);

casper.then(function() {
	this.fill('form', {
		'username': casper.cli.args[0],
		'password': casper.cli.args[1]
	}, true);
});

casper.then(function() {
	this.echo("Made it to auth'd page, scraping... you should see links soon...");
	links = this.getElementsAttribute('[href*=".txt.gz"]', 'href');
	this.each(links, function(self, link) {
		// Format of link is <Year-Month.txt.gz>		
		var linkInfo = link.split('.')[0].split('-');
		var month = linkInfo[1].toLowerCase();
		var year = linkInfo[0];

		self.thenOpen(base_url + link, function(page) {
			this.echo(link);
			fs.write('data/' + month + '-' + year + '.txt' , this.getPageContent(), 'w');
		});
	});
});

casper.run();
