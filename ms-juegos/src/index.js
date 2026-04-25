const express = require('express');
const mongoose = require('mongoose');
const { faker } = require('@faker-js/faker');
const Game = require('./models/game');
const gamesRouter = require('./routes/games');

const app = express();
app.use(express.json());

const MONGO_URL = process.env.MONGO_URL || 'mongodb://mongo:27017/juegos_db';

mongoose.connect(MONGO_URL).then(async () => {
  console.log('MongoDB conectado');
  // Seed data
  const count = await Game.countDocuments();
  if (count < 20000) {
    const genres = ['FPS', 'RPG', 'MOBA', 'Battle Royale', 'Sports', 'Strategy', 'Puzzle'];
    const platforms = ['PC', 'PS5', 'Xbox', 'Mobile', 'Switch'];
    const batch = [];
    for (let i = 0; i < 20000; i++) {
      batch.push({
        title: faker.company.name() + ' ' + faker.word.noun(),
        genre: genres[Math.floor(Math.random() * genres.length)],
        platform: platforms[Math.floor(Math.random() * platforms.length)],
        tags: [faker.word.adjective(), faker.word.noun()],
        metadata: {
          developer: faker.company.name(),
          release_year: faker.number.int({ min: 2010, max: 2024 }),
          rating: faker.number.float({ min: 1, max: 5, precision: 0.1 })
        }
      });
    }
    await Game.insertMany(batch);
    console.log('✅ 20,000 juegos insertados');
  }
});

app.use('/api/games', gamesRouter);
app.get('/health', (req, res) => res.json({ status: 'ok', service: 'ms-juegos' }));

app.listen(8002, () => console.log('MS Juegos corriendo en puerto 8002'));
