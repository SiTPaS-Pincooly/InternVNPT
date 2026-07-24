/* global use, db */
// MongoDB Playground practice file.
// This version is organized so you can learn, edit, and rerun it safely.

use('mongodbVSCodePlaygroundDB');

const sales = db.getCollection('sales');

// Reset the collection so the playground is repeatable.
sales.deleteMany({});

// Sample data set used by all examples below.
sales.insertMany([
  { item: 'abc', price: 10, quantity: 2, date: new Date('2014-03-01T08:00:00Z') },
  { item: 'jkl', price: 20, quantity: 1, date: new Date('2014-03-01T09:00:00Z') },
  { item: 'xyz', price: 5, quantity: 10, date: new Date('2014-03-15T09:00:00Z') },
  { item: 'xyz', price: 5, quantity: 20, date: new Date('2014-04-04T11:21:39.736Z') },
  { item: 'abc', price: 10, quantity: 10, date: new Date('2014-04-04T21:23:13.331Z') },
  { item: 'def', price: 7.5, quantity: 5, date: new Date('2015-06-04T05:08:13Z') },
  { item: 'def', price: 7.5, quantity: 10, date: new Date('2015-09-10T08:43:00Z') },
  { item: 'abc', price: 10, quantity: 5, date: new Date('2016-02-06T20:20:13Z') },
]);

// 1) Read data
// Find all documents for a specific item.
const abcSales = sales.find({ item: 'abc' }).toArray();
console.log('abc sales:', abcSales);

// Count documents for a date range.
const salesOnApril4th = sales.countDocuments({
  date: { $gte: new Date('2014-04-04'), $lt: new Date('2014-04-05') },
});
console.log(`There were ${salesOnApril4th} sales on April 4th, 2014.`);

// Find and sort the most recent sales.
const recentSales = sales.find({}).sort({ date: -1 }).limit(3).toArray();
console.log('Most recent sales:', recentSales);

// 2) Aggregation
// Total revenue per product in 2014.
const revenueByItem = sales.aggregate([
  { $match: { date: { $gte: new Date('2014-01-01'), $lt: new Date('2015-01-01') } } },
  {
    $group: {
      _id: '$item',
      totalRevenue: { $sum: { $multiply: ['$price', '$quantity'] } },
      totalUnits: { $sum: '$quantity' },
    },
  },
  { $sort: { totalRevenue: -1 } },
]).toArray();

console.log('Revenue by item in 2014:', revenueByItem);

// 3) Update data
// Increase the price of one document.
const updateResult = sales.updateOne(
  { item: 'xyz', quantity: 10 },
  { $set: { price: 6 } }
);
console.log('Update result:', updateResult);

// 4) Delete data
// Remove one older record to practice delete operations.
const deleteResult = sales.deleteOne({ item: 'def', quantity: 5 });
console.log('Delete result:', deleteResult);

// 5) Practice problems
// Try solving these yourself by editing the queries below:
// - Problem 1: Find all sales where quantity is at least 10.
console.log("Sales with quantity >= 10:", sales.find({ quantity: { $gte: 10 } }).toArray());

// - Problem 2: Show only item and total value for each document.
console.log("Items and total values:", sales.aggregate([
  {
    $project: {
      _id: 0,
      item: 1,
      totalValue: { $multiply: ['$price', '$quantity'] },
    },
  },
]).toArray());

// - Problem 3: Group sales by item and compute the average price.
console.log("Average price by item:", sales.aggregate([
  { $group: { _id: '$item', averagePrice: { $avg: '$price' } } },
]).toArray());

// - Problem 4: Find the top 2 sales by total value (price * quantity).
console.log("Top 2 sales by total value:", sales.aggregate([
  { $addFields: { totalValue: { $multiply: ['$price', '$quantity'] } } },
  { $sort: { totalValue: -1 } },
  { $limit: 2 },
]).toArray());

// - Problem 5: Delete all documents from 2016.
console.log("Deleting all documents from 2016:", sales.deleteMany({ date: { $gte: new Date('2016-01-01'), $lt: new Date('2017-01-01') } }));

// Problem 1 answer:
// sales.find({ quantity: { $gte: 10 } }).toArray();

// Problem 2 answer:
// sales.aggregate([
//   {
//     $project: {
//       _id: 0,
//       item: 1,
//       totalValue: { $multiply: ['$price', '$quantity'] },
//     },
//   },
// ]).toArray();

// Problem 3 answer:
// sales.aggregate([
//   { $group: { _id: '$item', averagePrice: { $avg: '$price' } } },
// ]).toArray();

// Problem 4 answer:
// sales.aggregate([
//   { $addFields: { totalValue: { $multiply: ['$price', '$quantity'] } } },
//   { $sort: { totalValue: -1 } },
//   { $limit: 2 },
// ]).toArray();

// Problem 5 answer:
// sales.deleteMany({ date: { $gte: new Date('2016-01-01'), $lt: new Date('2017-01-01') } });
