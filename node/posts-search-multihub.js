/*

EXAMPLE: Fetch posts from multiple hubs

1. Get bearer token for a given user using Basic Auth
2. Fetch results from GET /api/v3/posts/search with "mine" in Hubs header

*/

// setup
const axios = require('axios');
const prettify = require('pretty-var-export');
const api = axios.create({
	baseURL: 'https://sharpr.com/api',
});

// variables you can update
const email = process.env.SHARPR_EMAIL;
const basicAuthBase64 = process.env.SHARPR_AUTH;
const searchTerm = 'Marketing';

// run
main().catch(err => {
	console.log(`${err.stack}`);
	console.log('Response Headers: ' + prettify(err.response.headers));
});

async function main() {
	const { data: jwt } = await api.get('/v2/auth/bearer', {
		headers: {
			Authorization: `Basic ${basicAuthBase64}`,
		},
		params: { email },
	});
	const { data: posts } = await api.get('/v3/posts/search', {
		headers: {
			Authorization: `Bearer ${jwt.token}`,
			Hubs: 'mine',
		},
		params: { term: searchTerm, limit: 1 },
	});
	console.log('Found post:');
	console.log(prettify(posts));
}
