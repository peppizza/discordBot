const { Command } = require('discord.js-commando');

module.exports = class ReplyCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'reply',
            group: 'group1',
            memberName: 'reply',
            description: 'Replies with a message',
            examples: ['reply']
        });
    }

    async run(msg) {
        const message = await msg.say('Hi, I\'m awake');
        return message.edit('I want to die');
    }
};