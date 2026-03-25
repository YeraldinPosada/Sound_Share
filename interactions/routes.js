const express = require("express");
const router = express.Router();

const Like = require("./models/like");
const Favorite = require("./models/favorite");

require('dotenv').config();

const TOKEN_SECRETO = process.env.TOKEN_SECRETO;


function requireToken(req, res, next) {
    const token = req.headers["authorization"];

    if (token !== TOKEN_SECRETO) {
        return res.status(403).json({ error: "No autorizado" });
    }
    next();
}


//Likes

router.post("/likes", requireToken, async (req, res) => {
    const like = new Like(req.body);
    await like.save();

    res.json({
        message: "Like created",
        like
    });
});

router.get("/likes", requireToken, async (req, res) => {
    const likes = await Like.find();
    res.json(likes);
});

router.get("/likes/:id", requireToken, async (req, res) => {
    const like = await Like.findById(req.params.id);
    res.json(like);
});

router.put("/likes/:id", requireToken, async (req, res) => {
    const like = await Like.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true }
    );
    res.json(like);
});

router.delete("/likes/:id", requireToken, async (req, res) => {
    await Like.findByIdAndDelete(req.params.id);

    res.json({
        message: "Like deleted"
    });
});

// Likes por canción
router.post("/likes/song", requireToken, async (req, res) => {
    const { song_id } = req.body;

    const likes = await Like.find({ song_id });
    res.json(likes);
});

//Favorites

router.post("/favorites", requireToken, async (req, res) => {
    const favorite = new Favorite(req.body);
    await favorite.save();

    res.json({
        message: "Favorite created",
        favorite
    });
});

router.get("/favorites", requireToken, async (req, res) => {
    const favorites = await Favorite.find();
    res.json(favorites);
});

router.get("/favorites/:id", requireToken, async (req, res) => {
    const favorite = await Favorite.findById(req.params.id);
    res.json(favorite);
});

router.put("/favorites/:id", requireToken, async (req, res) => {
    const favorite = await Favorite.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true }
    );
    res.json(favorite);
});

router.delete("/favorites/:id", requireToken, async (req, res) => {
    await Favorite.findByIdAndDelete(req.params.id);

    res.json({
        message: "Favorite deleted"
    });
});

// Favoritos por usuario
router.post("/favorites/user", requireToken, async (req, res) => {
    const { user_id } = req.body;

    const favorites = await Favorite.find({ user_id });
    res.json(favorites);
});

module.exports = router;