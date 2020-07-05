const { CommandoClient, SQLiteProvider} = require('discord.js-commando');
const path = require('path');
const { token } = require('./config.json');
const sqlite = require('sqlite');
const sqlite3 = require('sqlite3');

const client = new CommandoClient({
    commandPrefix: '?',
    owner: '253290704384557057',
});

client.registry
    .registerDefaultTypes()
    .registerGroups([
        ['group1', 'Our first command group'],
        ['group2', 'Our second command group']
    ])
    .registerDefaultGroups()
    .registerDefaultCommands({
        unknownCommand: false
    })
    .registerCommandsIn(path.join(__dirname, 'commands'));

client.on('ready', () => {
    console.log('Logged in');
    client.user.setActivity('game');
});

sqlite.open( { filename: path.join(__dirname, 'settings.sqlite3'), driver: sqlite3.Database } ).then(db => {
    client.setProvider(new SQLiteProvider(db));
}).catch(console.error);

client.login(token);