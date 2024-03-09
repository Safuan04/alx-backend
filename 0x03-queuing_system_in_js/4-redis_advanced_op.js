import { createClient } from "redis";
import { print } from "redis";

const client = createClient()
  .on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  )
  .on("connect", () => console.log("Redis client connected to the server"));

const key = "HolbertonSchools";

const obj = {
  Portland: 50,
  Seattle: 80,
  "New York": 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

const keys = Object.keys(obj);
keys.forEach(field => {
  const val = obj[field];
  client.hset(key, field, val, (err, res) => {
    if (err) {
      console.error(err);
    } else {
      print(`Reply: ${res}`);
    }
  });
});

client.hgetall(key, (err, res) => {
  if (err) {
    console.err(err);
  } else {
    console.log(res);
  }
});
