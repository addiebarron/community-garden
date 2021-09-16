app.get(input, function () {
  conn.query(input, function () {});
});

console.log("1");
setTimeout(function () {
  console.log("hi");
}, 1000);
console.log("2");

app.get = function (input, callback) {
  // do stuff with input
  callback();
};
