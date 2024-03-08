import { createClient } from 'redis';
const util = require('util');

const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log(`Redis client connected to the server`))

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error(err);
    }
    else {
      console.log(`Reply: ${reply}`);
    }
  });
}

const getAsync = util.promisify(client.get).bind(client)

async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName)
    console.log(reply)
  } catch (err) {
    console.error(err)
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
