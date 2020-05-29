module.exports = {
    name: 'kick',
    description: 'Kicks a user from the server',
    guildOnly: true,
    args: true,
    usage: '<user>',
    execute(command, args) {
        if (!command.mentions.users.size) {
            return command.reply('You need to mention a user in order to kick them');
        }

        command.channel.send(`You wanted to kick ${command.mentions.users.first()}`);
    }
}