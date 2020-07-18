import {
  CommandoClient,
  SQLiteProvider,
  FriendlyError,
} from "discord.js-commando";
import path from "path";
import { token } from "./config.json";
import sqlite from "sqlite";
import { oneLine } from "common-tags";

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

client
  .on("error", console.error)
  .on("warn", console.warn)
  .on("debug", console.log)
  .on("ready", () => {
    console.log(
      `Client ready; logged in as ${client.user?.username}#${client.user?.discriminator} (${client.user?.id})`
    );
  })
  .on("disconnect", () => console.warn("Disconnected!"))
  .on("reconnecting", () => console.warn("Reconnecting..."))
  .on("commandError", (cmd, err) => {
    if (err instanceof FriendlyError) return;
    console.error(`Error in command ${cmd.groupID}:${cmd.memberName}`, err);
  })
  .on("commandBlocked", (msg, reason) => {
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
  .on("commandStatusChange", (guild, command, enabled) => {
    console.log(oneLine`
        Command ${command.groupID}:${command.memberName}
        ${enabled ? "enabled" : "disabled"}
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

(async () => {
  const db = await sqlite.open("settings.sqlite3");
  client.setProvider(new SQLiteProvider(db));
})();

client.login(token);
