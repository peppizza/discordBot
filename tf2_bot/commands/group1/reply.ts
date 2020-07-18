import { Command, CommandoMessage, CommandoClient } from "discord.js-commando";

export class ReplyCommand extends Command {
  constructor(client: CommandoClient) {
    super(client, {
      name: "reply",
      group: "group1",
      memberName: "reply",
      description: "Replies with a message",
      examples: ["reply"],
    });
  }

  run(msg: CommandoMessage) {
    return msg.say("Hello");
  }
}
