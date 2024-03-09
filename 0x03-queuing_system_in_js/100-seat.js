import { promisify } from "util";
const express = require("express");

const redisClient = require("redis").createClient();
const queue = require("kue").createQueue();

const asyncSet = promisify(redisClient.set).bind(redisClient);
const asyncGet = promisify(redisClient.get).bind(redisClient);
let reservationEnabled = true;

const reserveSeat = async (number) => {
  try {
    await asyncSet("available_seats", number);
  } catch (err) {
    console.error(err);
  }
};

const getCurrentAvailableSeats = async () => {
  try {
    const availableSeats = await asyncGet("available_seats");
    return availableSeats;
  } catch (err) {
    console.error(err);
  }
};

const app = express();
const port = 1245;

app.get("/available_seats", async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.status(200).json({ numberOfAvailableSeats: availableSeats });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    return res.status(401).json({ status: "Reservation are blocked" });
  }
  const job = queue.create("reserve_seat");
  job
    .save((err) => {
      if (err) {
        return res.status(401).json({ status: "Reservation failed" });
      } else {
        return res.status(200).json({ status: "Reservation in process" });
      }
    })
    .on("complete", () => {
      console.log(`Seat reservation job #${job.id} completed`);
    })
    .on("failed", (err) => {
      console.log(`Seat reservation job #${job.id} failed: ${err}`);
    });
});

app.get("/process", async (req, res) => {
  queue.process("reserve_seat", async (job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      if (availableSeats == 0) {
        reservationEnabled = false;
        return done(new Error("Not enough seats available"));
      } else {
        await reserveSeat(availableSeats - 1);
        done();
      }
    } catch (err) {
      console.error(err);
    }
  });
  res.status(200).json({ status: "Queue processing" });
});

app.listen(port, async () => {
  await reserveSeat(50);
});
