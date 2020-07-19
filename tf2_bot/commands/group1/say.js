const { Command } = require("discord.js-commando");

module.exports = class SayCommand extends Command {
  constructor(client) {
    super(client, {
      name: "say",
      description: "says something",
      group: "group1",
      memberName: "say",
    });
  }

  run(msg) {
    return msg.say("Hello");
  }
};
