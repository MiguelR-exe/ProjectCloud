const mongoose = require('mongoose');

const gameSchema = new mongoose.Schema({
  title: { type: String, required: true },
  genre: { type: String, required: true },
  platform: String,
  tags: [String],
  metadata: {
    developer: String,
    release_year: Number,
    rating: Number
  },
  created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Game', gameSchema);
