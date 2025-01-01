import express from 'express';
import _ from 'lodash'

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(port, () => {
  var objects = [{ 'a': 1 }, { 'a': 2 }];

// in 3.10.1
_.pluck(objects, 'a'); // ➜ [1, 2]

  console.log(`Server listening on port ${port}`);
});
