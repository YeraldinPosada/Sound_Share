const request = require("supertest")
const mongoose = require("mongoose")
const { MongoMemoryServer } = require("mongodb-memory-server")

const app = require("../app")
const Like = require("../models/like")
const Favorite = require("../models/favorite")

const TOKEN = "1234"

function auth() {
    return { authorization: TOKEN }
}

let mongod

// ---------------------------------------------------------------
// Configuración: base de datos en memoria
// ---------------------------------------------------------------

beforeAll(async () => {
    mongod = await MongoMemoryServer.create()
    await mongoose.connect(mongod.getUri())
})

afterAll(async () => {
    await mongoose.disconnect()
    await mongod.stop()
})

beforeEach(async () => {
    // Limpiar colecciones antes de cada test
    await Like.deleteMany({})
    await Favorite.deleteMany({})
})

// ---------------------------------------------------------------
// TEST 1 — Crear like exitosamente
// ---------------------------------------------------------------

describe("POST /api/likes", () => {
    test("crea un like y lo retorna", async () => {
        const res = await request(app)
            .post("/api/likes")
            .set(auth())
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(200)
        expect(res.body.message).toBe("Like created")
        expect(res.body.like.user_id).toBe(1)
        expect(res.body.like.song_id).toBe(10)

        const stored = await Like.findOne({ user_id: 1, song_id: 10 })
        expect(stored).not.toBeNull()
    })

    test("retorna 403 si no se envía token", async () => {
        const res = await request(app)
            .post("/api/likes")
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(403)
    })
})

// ---------------------------------------------------------------
// TEST 2 — Obtener likes por canción
// ---------------------------------------------------------------

describe("GET /api/likes/:song_id", () => {
    test("retorna lista vacía si la canción no tiene likes", async () => {
        const res = await request(app)
            .get("/api/likes/99")
            .set(auth())

        expect(res.statusCode).toBe(200)
        expect(res.body).toEqual([])
    })

    test("retorna solo los likes de la canción consultada", async () => {
        await Like.create({ user_id: 1, song_id: 10 })
        await Like.create({ user_id: 2, song_id: 10 })
        await Like.create({ user_id: 3, song_id: 20 }) // otra canción

        const res = await request(app)
            .get("/api/likes/10")
            .set(auth())

        expect(res.statusCode).toBe(200)
        expect(res.body).toHaveLength(2)
        res.body.forEach(like => {
            expect(like.song_id).toBe(10)
        })
    })
})

// ---------------------------------------------------------------
// TEST 3 — Eliminar like
// ---------------------------------------------------------------

describe("DELETE /api/likes", () => {
    test("elimina un like existente", async () => {
        await Like.create({ user_id: 1, song_id: 10 })

        const res = await request(app)
            .delete("/api/likes")
            .set(auth())
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(200)
        expect(res.body.message).toBe("Like deleted")

        const stored = await Like.findOne({ user_id: 1, song_id: 10 })
        expect(stored).toBeNull()
    })

    test("retorna 404 si el like no existe", async () => {
        const res = await request(app)
            .delete("/api/likes")
            .set(auth())
            .send({ user_id: 99, song_id: 99 })

        expect(res.statusCode).toBe(404)
        expect(res.body.error).toBe("Like not found")
    })
})

// ---------------------------------------------------------------
// TEST 4 — Crear favorito
// ---------------------------------------------------------------

describe("POST /api/favorites", () => {
    test("crea un favorito y lo retorna", async () => {
        const res = await request(app)
            .post("/api/favorites")
            .set(auth())
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(200)
        expect(res.body.message).toBe("Favorite created")
        expect(res.body.favorite.user_id).toBe(1)
        expect(res.body.favorite.song_id).toBe(10)

        const stored = await Favorite.findOne({ user_id: 1, song_id: 10 })
        expect(stored).not.toBeNull()
    })

    test("retorna 403 si no se envía token", async () => {
        const res = await request(app)
            .post("/api/favorites")
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(403)
    })
})

// ---------------------------------------------------------------
// TEST 5 — Obtener y eliminar favoritos
// ---------------------------------------------------------------

describe("GET /api/favorites/:user_id", () => {
    test("retorna solo los favoritos del usuario consultado", async () => {
        await Favorite.create({ user_id: 1, song_id: 10 })
        await Favorite.create({ user_id: 1, song_id: 20 })
        await Favorite.create({ user_id: 2, song_id: 30 }) // otro usuario

        const res = await request(app)
            .get("/api/favorites/1")
            .set(auth())

        expect(res.statusCode).toBe(200)
        expect(res.body).toHaveLength(2)
        res.body.forEach(fav => {
            expect(fav.user_id).toBe(1)
        })
    })
})

describe("DELETE /api/favorites", () => {
    test("elimina un favorito existente", async () => {
        await Favorite.create({ user_id: 1, song_id: 10 })

        const res = await request(app)
            .delete("/api/favorites")
            .set(auth())
            .send({ user_id: 1, song_id: 10 })

        expect(res.statusCode).toBe(200)
        expect(res.body.message).toBe("Favorite deleted")

        const stored = await Favorite.findOne({ user_id: 1, song_id: 10 })
        expect(stored).toBeNull()
    })

    test("retorna 404 si el favorito no existe", async () => {
        const res = await request(app)
            .delete("/api/favorites")
            .set(auth())
            .send({ user_id: 99, song_id: 99 })

        expect(res.statusCode).toBe(404)
        expect(res.body.error).toBe("Favorite not found")
    })
})