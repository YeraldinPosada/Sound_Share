const mongoose = require('mongoose');

const likeSchema = new mongoose.Schema({
    user_id: { type: Number, required: true },
    song_id: { type: Number, required: true },
    created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Like', likeSchema);