import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

dotenv.config();
const app = express();


const express = require('express');
const fetch = require('node-fetch');

require('dotenv').config();

app.use(express.static('public'));

app.get('/data', async (req, res) => {
  const url = `https://io.adafruit.com/api/v2/${process.env.AIO_USERNAME}/feeds/${process.env.FEED_NAME}/data?limit=1`;
  const response = await fetch(url, {
    headers: { 'X-AIO-Key': process.env.AIO_KEY },
  });
  const data = await response.json();
  res.json(data);
});

app.listen(3000, () => console.log('Server running on port 3000'));
