import { User } from "discord.js";
import { Command, CommandoClient, CommandoMessage } from "discord.js-commando";

module.exports = class DMCommand extends Command {
  constructor(client: CommandoClient) {
    super(client, {
      name: "dm",
      group: "group2",
      memberName: "dm",
      description: "Sends a message to the user you mention",
      examples: ["dm @User Hi There!"],
      args: [
        {
          key: "user",
          prompt: "Which user do you want to send the DM to?",
          type: "user",
        },
        {
          key: "content",
          prompt: "What would you like the content of the message to be?",
          type: "string",
        },
      ],
    });
  }

  run(
    msg: CommandoMessage,
    { user, content }: { user: User; content: string }
  ) {
    return user.send(content);
  }
};
