const mongoose = require('mongoose');

const favoriteSchema = new mongoose.Schema({
    user_id: { type: Number, required: true },
    song_id: { type: Number, required: true }
});

module.exports = mongoose.model('Favorite', favoriteSchema);