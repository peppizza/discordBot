import { CommandoClient } from "discord.js-commando";
import * as path from "path";
import * as config from "./config.json";

const client = new CommandoClient({
  commandPrefix: "?",
  owner: "253290704384557057",
});

client.registry
  .registerDefaultTypes()
  .registerGroups([
    ["group1", "Our first command group"],
    ["group2", "Our second command group"],
  ])
  .registerDefaultGroups()
  .registerDefaultCommands()
  .registerCommandsIn(path.join(__dirname, "commands"));

client.on("ready", () => {
  console.log("Logged in!");
  client?.user?.setActivity("game");
});

client.login(config.token);
