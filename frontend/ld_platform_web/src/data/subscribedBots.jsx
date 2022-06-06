import moment from "moment-timezone";

export default [
  {
    invoiceNumber: 300500,
    status: "Paid",
    subscription: "Platinum Subscription Plan",
    issueDate: moment().subtract(1, "days").format("DD MMM YYYY"),
    dueDate: moment().subtract(1, "days").add(1, "month").format("DD MMM YYYY")
  },
  {
    invoiceNumber: 300499,
    status: "Paid",
    subscription: "Platinum Subscription Plan",
    issueDate: moment().subtract(2, "days").format("DD MMM YYYY"),
    dueDate: moment().subtract(2, "days").add(1, "month").format("DD MMM YYYY")
  },
  {
    invoiceNumber: 300498,
    status: "Paid",
    subscription: "Platinum Subscription Plan",
    issueDate: moment().subtract(2, "days").format("DD MMM YYYY"),
    dueDate: moment().subtract(2, "days").add(1, "month").format("DD MMM YYYY")
  },
  {
    invoiceNumber: 300497,
    status: "Paid",
    subscription: "Flexible Subscription Plan",
    issueDate: moment().subtract(3, "days").format("DD MMM YYYY"),
    dueDate: moment().subtract(3, "days").add(1, "month").format("DD MMM YYYY")
  },
  {
    invoiceNumber: 300496,
    status: "Due",
    subscription: "Gold Subscription Plan",
    issueDate: moment()
      .subtract(1, "day")
      .subtract(1, "month")
      .format("DD MMM YYYY"),
    dueDate: moment().subtract(1, "day").format("DD MMM YYYY")
  }
];
