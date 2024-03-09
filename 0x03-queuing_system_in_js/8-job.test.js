import createPushNotificationsJobs from "./8-job";
const { expect } = require("chai");

describe("createPushNotificationsJobs", () => {
  const queue = require("kue").createQueue();

  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it("display an error message if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs({ job: 1 }, queue)).to.throw(
      "Jobs is not an array"
    );
  });

  it("create one new job to the queue", () => {
    const list = [
      {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
      },
    ];
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[0].data.phoneNumber).to.equal("4153518780");
    expect(queue.testMode.jobs[0].data.message).to.equal(
      "This is the code 1234 to verify your account"
    );
    expect(queue.testMode.jobs.length).to.equal(1);
  });

  it("create two new jobs to the queue", () => {
    const list = [
      {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
      },
      {
        phoneNumber: "4154518780",
        message: "This is the code 2234 to verify your account",
      },
    ];
    createPushNotificationsJobs(list, queue);
    expect(queue.testMode.jobs[1].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[1].data.phoneNumber).to.equal("4154518780");
    expect(queue.testMode.jobs[1].data.message).to.equal(
      "This is the code 2234 to verify your account"
    );
    expect(queue.testMode.jobs.length).to.equal(2);
  });
});
