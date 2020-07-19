const {
  CommandoClient,
  SQLiteProvider,
  FriendlyError,
} = require("discord.js-commando");
const path = require("path");
const sqlite = require("sqlite");
const sqlite3 = require("sqlite3");
const { oneLine } = require("common-tags");
const { token } = require("./config.json");

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
  .registerDefaultCommands({
    unknownCommand: false,
  })
  .registerCommandsIn(path.join(__dirname, "commands"));

client
  .on("error", console.error)
  .on("warn", console.warn)
  .on("debug", console.log)
  .on("ready", () => {
    console.log(
      `Client ready; logged in as ${client.user.username}${client.user.discriminator} (${client.user.id})`
    );
  })
  .on("disconnect", () => console.warn("Disconnected!"))
  .on("reconnecting", () => console.warn("Reconnecting..."))
  .on("commandError", (cmd, err) => {
    if (err instanceof FriendlyError) return;
    console.error(`Error in command ${cmd.groupID}:${cmd.memberName}`, err);
  })
  .on("commandBlock", (msg, reason) => {
    console.log(oneLine`
      Command ${
        msg.command ? `${msg.command.groupID}:${msg.command.memberName}` : ""
      }
      blocked; ${reason}
    `);
  })
  .on("commandPrefixChange", (guild, prefix) => {
    console.log(oneLine`
      Prefix ${
        prefix === "" ? "removed" : `changed to ${prefix || "the default"}`
      }
      ${guild ? `in guild ${guild.name} (${guild.id})` : "globally"}
    `);
  })
  .on("groupStatusChange", (guild, group, enabled) => {
    console.log(oneLine`
      Group ${group.id}
      ${enabled ? "enabled" : "disabled"}
      ${guild ? `in guild ${guild.name} (${guild.id})` : "globally"}
    `);
  });

sqlite
  .open({
    filename: path.join(__dirname, "settings.sqlite3"),
    driver: sqlite3.Database,
  })
  .then((db) => {
    client.setProvider(new SQLiteProvider(db));
  })
  .catch(console.error);

client.login(token);
