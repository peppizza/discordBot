import { Command, CommandoClient, CommandoMessage } from "discord.js-commando";

module.exports = class SayCommand extends Command {
  constructor(client: CommandoClient) {
    super(client, {
      name: "say",
      group: "group2",
      memberName: "say",
      description: "Replies with the text you provide",
      examples: ["say Hi there!"],
      args: [
        {
          key: "text",
          prompt: "What text would you like the bot to say?",
          type: "string",
        },
      ],
    });
  }

  run(msg: CommandoMessage, { text }: { text: string }) {
    return msg.say(text);
  }
};
