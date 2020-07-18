import { Command, CommandoMessage, CommandoClient } from "discord.js-commando";

module.exports = class ReplyCommand extends Command {
  constructor(client: CommandoClient) {
    super(client, {
      name: "reply",
      group: "group1",
      memberName: "reply",
      description: "Replies with a message",
      examples: ["reply"],
    });
  }

  async run(msg: CommandoMessage) {
    const message = await msg.say("Hi");
    return message.edit("Bye");
  }
};
