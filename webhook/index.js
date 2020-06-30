const express = require('express');
const bodyParser = require('body-parser');
const simpleGit = require('simple-git');

const app = express();
const git = simpleGit();
const PORT = 4567;

app.use(bodyParser());

app.post('/payload', async (req, res) => {
	console.log(req.body);
	res.send('Got data!');
	await git.pull(() => console.log('pulling data'));
});

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
