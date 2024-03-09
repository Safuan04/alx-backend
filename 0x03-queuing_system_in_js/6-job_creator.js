const kue = require("kue");

const obj = {
  phoneNumber: "4153518780",
  message: "This is the code to verify your account",
};

const queue = kue.createQueue();

const job = queue.create("push_notification_code", obj).save((err) => {
  if (err) {
    console.log("Notification job failed");
  } else {
    console.log(`Notification job created ${job.id}`);
    job.on("complete", () => {
      console.log("Notification job completed");
    });
  }
});
