module.exports = {
    name: 'role',
    description: 'Set a users role',
    args: true,
    usage: '<user> <role>',
    execute(message, args) {
        message.channel.send('no');
    }
}