from locust import HttpUser, task, between  # type: ignore
import random, time

TEST_EMAIL    = "Susyy@gmaill.com"
TEST_PASSWORD = "1234"

SAMPLE_SONG_IDS   = [1, 5, 4]
SAMPLE_LYRICS_IDS = [2, 20, 24]


class LyricsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self._login()

    def _login(self):
        r = self.client.post(
            "/api/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            name="[Auth] Login"
        )
        if r.status_code == 200:
            data = r.json()
            self.token = data.get("token") or data.get("access_token")

    def _headers(self):
        if not self.token:
            self._login()
        return {"Authorization": f"Bearer {self.token}"}

    @task(5)
    def listar_lyrics(self):
        with self.client.get(
            "/api/lyrics",
            headers=self._headers(),
            catch_response=True,
            name="[Lyrics] Listar"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")

    @task(4)
    def obtener_lyric(self):
        lyric_id = random.choice(SAMPLE_LYRICS_IDS)
        with self.client.get(
            f"/api/lyrics/{lyric_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Lyrics] Obtener"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(2)
    def crear_lyric(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS),
            "content": f"Letra de prueba {random.randint(1000, 9999)}"
        }
        with self.client.post(
            "/api/lyrics",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Lyrics] Crear"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code} - {r.text[:80]}")
    @task(2)
    def editar_lyric(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS),
            "content": "Letra inicial"
        }
        r = self.client.post("/api/lyrics", json=payload, headers=self._headers(), name="[Lyrics] Crear para editar")

        if r.status_code not in (200, 201):
            return

        data = r.json()
        lyric_id = data.get("id") or data.get("data", {}).get("id")

        if not lyric_id:
            return

        time.sleep(0.5)  # ← le da tiempo a la BD a confirmar el insert

        with self.client.put(
            f"/api/lyrics/{lyric_id}",
            json={"content": f"Letra actualizada {random.randint(100, 999)}"},
            headers=self._headers(),
            catch_response=True,
            name="[Lyrics] Editar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    def eliminar_lyric(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS),
            "content": "Lyric temporal para eliminar"
        }
        with self.client.post(
            "/api/lyrics",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Lyrics] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                lyric_id = data.get("id") or data.get("data", {}).get("id")
                r.success()
                if lyric_id:
                    self.client.delete(
                        f"/api/lyrics/{lyric_id}",
                        headers=self._headers(),
                        name="[Lyrics] Eliminar"
                    )
            else:
                r.failure(f"Error al crear: {r.status_code}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )