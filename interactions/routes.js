const express = require("express");
const router = express.Router();

const Like = require("./models/like");
const Favorite = require("./models/favorite");

require("dotenv").config();

const TOKEN_SECRETO = process.env.TOKEN_SECRETO;


function requireToken(req, res, next) {
    const token = req.headers["authorization"];

    if (token !== TOKEN_SECRETO) {
        return res.status(403).json({ error: "Unauthorized" });
    }
    next();
}

//likes
router.post("/likes", requireToken, async (req, res) => {
    const { user_id, song_id } = req.body;

    const like = new Like({ user_id, song_id });
    await like.save();

    res.json({
        message: "Like created",
        like
    });
});


router.get("/likes/:song_id", requireToken, async (req, res) => {
    const likes = await Like.find({ song_id: req.params.song_id });

    res.json(likes);
});

router.delete("/likes", requireToken, async (req, res) => {
    const { user_id, song_id } = req.body;

    const deleted = await Like.findOneAndDelete({ user_id, song_id });

    if (!deleted) {
        return res.status(404).json({ error: "Like not found" });
    }

    res.json({
        message: "Like deleted"
    });
});

//favorites
router.post("/favorites", requireToken, async (req, res) => {
    const { user_id, song_id } = req.body;

    const favorite = new Favorite({ user_id, song_id });
    await favorite.save();

    res.json({
        message: "Favorite created",
        favorite
    });
});

router.get("/favorites/:user_id", requireToken, async (req, res) => {
    const favorites = await Favorite.find({ user_id: req.params.user_id });

    res.json(favorites);
});

router.delete("/favorites", requireToken, async (req, res) => {
    const { user_id, song_id } = req.body;

    const deleted = await Favorite.findOneAndDelete({ user_id, song_id });

    if (!deleted) {
        return res.status(404).json({ error: "Favorite not found" });
    }

    res.json({
        message: "Favorite deleted"
    });
});

module.exports = router;