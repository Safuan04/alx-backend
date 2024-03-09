import { createClient } from "redis";
import { print } from "redis";

const client = createClient()
  .on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  )
  .on("connect", () => console.log("Redis client connected to the server"));

client.subscribe("holberton school channel");

client.on("message", (channel, message) => {
  if (message == "KILL_SERVER") {
    client.unsubscribe(channel);
    client.quit();
  } else {
    console.log(message);
  }
});
