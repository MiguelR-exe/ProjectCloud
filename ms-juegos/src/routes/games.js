const express = require('express');
const router = express.Router();
const Game = require('../models/game');

// GET todos los juegos
router.get('/', async (req, res) => {
  const { page = 1, limit = 20, genre } = req.query;
  const filter = genre ? { genre } : {};
  const games = await Game.find(filter)
    .skip((page - 1) * limit)
    .limit(Number(limit));
  res.json(games);
});

// GET juego por ID
router.get('/:id', async (req, res) => {
  try {
    const game = await Game.findById(req.params.id);
    if (!game) return res.status(404).json({ error: 'Juego no encontrado' });
    res.json(game);
  } catch (e) {
    res.status(400).json({ error: 'ID inválido' });
  }
});

// POST crear juego
router.post('/', async (req, res) => {
  const game = new Game(req.body);
  await game.save();
  res.status(201).json(game);
});

// GET géneros disponibles
router.get('/stats/genres', async (req, res) => {
  const result = await Game.aggregate([
    { $group: { _id: '$genre', count: { $sum: 1 } } },
    { $sort: { count: -1 } }
  ]);
  res.json(result);
});

module.exports = router;
