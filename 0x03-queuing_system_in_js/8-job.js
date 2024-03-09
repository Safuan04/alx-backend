const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error("Jobs is not an array");
  }
  jobs.forEach((jobObj) => {
    const job = queue.create("push_notification_code_3", jobObj);
    job
      .on("complete", () => {
        console.log(`Notification job #${job.id} completed`);
      })
      .on("failed", (err) => {
        console.log(`Notification job #${job.id} failed: ${err}`);
      })
      .on("progress", (progress, data) => {
        console.log(`Notification job #${job.id} ${progress}% complete`);
      })
      .save((err) => {
        if (!err) {
          console.log(`Notification job created: ${job.id}`);
        }
      });
  });
};

module.exports = createPushNotificationsJobs;
