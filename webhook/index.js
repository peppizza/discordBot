/* eslint-disable no-console */

const express = require("express");
const simpleGit = require("simple-git");

const app = express();
const git = simpleGit();
const PORT = 4567;

app.use(express.json());

app.post("/payload", async (req, res) => {
  res.send();
  if (req.body.ref === "refs/heads/master") {
    await git.pull("origin", "master");
  }
});

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
