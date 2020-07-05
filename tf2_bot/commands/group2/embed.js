const { Command } = require('discord.js-commando');
const { MessageEmbed } = require('discord.js');

module.exports = class EmbedCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'embed',
            group: 'group2',
            memberName: 'embed',
            description: 'Embeds the text you provide',
            examples: ['embed Embeds are cool'],
            args: [
                {
                    key: 'text',
                    prompt: 'What text would you like the bot to embed',
                    type: 'string'
                }
            ]
        });
    }

    run(msg, { text }) {
        const embed = new MessageEmbed()
            .setDescription(text)
            .setAuthor(msg.author.username, msg.author.displayAvatarURL)
            .setColor(0x00AE86)
            .setTimestamp();
        return msg.embed(embed);
    }
}