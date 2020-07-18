import { Command, CommandoClient, CommandoMessage } from "discord.js-commando";

module.exports = class SayCommand extends Command {
  constructor(client: CommandoClient) {
    super(client, {
      name: "say",
      aliases: ["copycat", "repeat", "echo", "parrot"],
      group: "group2",
      memberName: "say",
      description: "Replies with the text you provide",
      examples: ["say Hi there!"],
      throttling: {
        usages: 2,
        duration: 10,
      },
      guildOnly: true,
      args: [
        {
          key: "text",
          prompt: "What text would you like the bot to say?",
          type: "string",
          validate: (text: string) => {
            if (text.length < 201) return true;
            return "Message content is above 200 characters";
          },
        },
      ],
    });
  }

  run(msg: CommandoMessage, { text }: { text: string }) {
    msg.delete();
    return msg.say(text);
  }
};
