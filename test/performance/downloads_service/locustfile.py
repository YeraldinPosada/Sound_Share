"""
Sound_Share - Pruebas de rendimiento
====================================================
Todas las peticiones pasan por el API Gateway (puerto 8000).
Cómo correr: locust 
"""

from locust import HttpUser, task, between # type: ignore
import random

TEST_EMAIL    = "Susyy@gmaill.com"
TEST_PASSWORD = "1234"

SAMPLE_SONG_IDS = [1, 4, 3]
SAMPLE_USER_IDS = [1]



class DownloadsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self._login()

    def _login(self):
        response = self.client.post(
            "/api/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            name="[Auth] Login"
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token") or data.get("access_token")

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(5)
    def listar_descargas(self):
        with self.client.get(
            "/api/downloads",
            headers=self._headers(),
            catch_response=True,
            name="[Downloads] Listar descargas"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")

    @task(3)
    def descargas_por_usuario(self):
        user_id = random.choice(SAMPLE_USER_IDS)
        with self.client.get(
            f"/api/downloads/user/{user_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Downloads] Por usuario"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(3)
    def descargas_por_cancion(self):
        song_id = random.choice(SAMPLE_SONG_IDS)
        with self.client.get(
            f"/api/downloads/song/{song_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Downloads] Por canción"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(2)
    def crear_descarga(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS)
        }
        with self.client.post(
            "/api/downloads",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Downloads] Crear descarga"
        ) as r:
            if r.status_code in (200, 201):
                r.success()
            else:
                r.failure(f"Error {r.status_code} — {r.text[:80]}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )