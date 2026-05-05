const app = require("./app")
const conectarDB = require("./db")

conectarDB()

app.listen(3000, () => {
    console.log("Servidor corriendo en puerto 3000")
})