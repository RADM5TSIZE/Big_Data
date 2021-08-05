const dns = require('dns').promises;
const os = require('os')
const express = require('express')
const { addAsync } = require('@awaitjs/express');
const app = addAsync(express());
const mysqlx = require('@mysql/xdevapi');
const MemcachePlus = require('memcache-plus');
const inefficient = require('inefficient');

//Connect to the memcached instances
let memcached = null
let memcachedServers = []

//Database configuration
const dbConfig = {
	user: 'root',
	password: 'mysecretpw',
	host: 'my-app-mysql-service',
	port: 33060,
	schema: 'sportsdb'
};

//Get list of memcached servers from DNS
async function getMemcachedServersFromDns() {
	try {
		let queryResult = await dns.lookup('my-memcached-service', { all: true })
		let servers = queryResult.map(el => el.address + ":11211")

		//Only create a new object if the server list has changed
		if (memcachedServers.sort().toString() !== servers.sort().toString()) {
			console.log("Updated memcached server list to ", servers)
			memcachedServers = servers
			//Disconnect an existing client
			if (memcached)
				await memcached.disconnect()
			memcached = new MemcachePlus(memcachedServers);
		}
	} catch (e) {
		console.log("Error resolving memcached", e);
	}
}

//Initially try to connect to the memcached servers, then each 5s update the list
getMemcachedServersFromDns()
setInterval(() => getMemcachedServersFromDns(), 5000)

//Get data from cache if a cache exists yet
async function getFromCache(key) {
	if (!memcached) {
		console.log(`No memcached instance available, memcachedServers = ${memcachedServers}`)
		return null;
	}
	return await memcached.get(key);
}

//Get data from database
async function getFromDatabase(userid) {
	let query = 'SELECT birth_date from persons WHERE person_key = ? LIMIT 1';
	let session = await mysqlx.getSession(dbConfig);

	console.log("Executing query " + query)
	let res = await session.sql(query).bind([userid]).execute()
	let row = res.fetchOne()

	if (row) {
		console.log("Query result = ", row)
		return row[0];
	} else {
		return null;
	}
}

//Send HTML response to client
function send_response(response, data) {
	response.send(`<h1>Hello k8s</h1> 
			<ul>
				<li>Host ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
				<li>Memcached Servers: ${memcachedServers}</li>
				<li>Result: <b>${data}</b></li>
			</ul>
			<h3> Test </h3>`
);
}

// Redirect / to person with ID l.mlb.com - p.7491
app.get('/', function (request, response) {
	response.writeHead(302, { 'Location': 'person/l.mlb.com-p.7491' })
	response.end();
})

// Get data about a single person
app.getAsync('/person/:id', async function (request, response) {
	let userid = request.params["id"]
	let key = 'user_' + userid
	let cachedata = await getFromCache(key)


	if (cachedata) {
		console.log(`Cache hit for key=${key}, cachedata = ${cachedata}`)
		send_response(response, cachedata + " (cache hit)");
	} else {
		console.log(`Cache miss for key=${key}, querying database`)
		let data = await getFromDatabase(userid)
		if (data) {
			console.log(`Got data=${data}, storing in cache`)
			if (memcached)
				await memcached.set(key, data, 30 /* seconds */);
			send_response(response, data + " (cache miss)");
		} else {
			send_response(response, "No data found");
		}
	}
})

// Add stress test endpoint, cf. https://github.com/bermi/inefficient
app.get('/stress', inefficient);

// Set port to start the app on
app.set('port', (process.env.PORT || 8080))

// Start the application
app.listen(app.get('port'), function () {
	console.log("Node app is running at localhost:" + app.get('port'))
})
