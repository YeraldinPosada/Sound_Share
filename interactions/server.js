const express = require("express")
const dotenv = require("dotenv")
const conectarDB = require("./db")

dotenv.config()

const app = express()

app.use(express.json())

conectarDB()

app.use("/api", require("./routes"))

app.listen(3000, () => {
    console.log("Servidor corriendo en puerto 3000")
})

