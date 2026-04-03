from locust import HttpUser, task, between # type: ignore
import random
import time

TEST_EMAIL    = "Susyy@gmaill.com"
TEST_PASSWORD = "1234"

SAMPLE_SONG_IDS = [5, 4, 3]
SAMPLE_USER_IDS = [2]


class InteractionUser(HttpUser):
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
    def obtener_likes(self):
        song_id = random.choice(SAMPLE_SONG_IDS)
        with self.client.get(
            f"/api/likes/{song_id}",
            catch_response=True,
            name="[Likes] Obtener por canción"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(4)
    def obtener_favoritos(self):
        user_id = random.choice(SAMPLE_USER_IDS)
        with self.client.get(
            f"/api/favorites/{user_id}",
            catch_response=True,
            name="[Favorites] Obtener por usuario"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(3)
    def crear_like(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS)
        }
        with self.client.post(
            "/api/likes",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Likes] Crear"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(2)
    def eliminar_like(self):
        song_id = random.choice(SAMPLE_SONG_IDS)

        self.client.post(
            "/api/likes",
            json={"song_id": song_id},
            headers=self._headers()
        )
        time.sleep(0.2)
        with self.client.delete(
            "/api/likes",
            data={"song_id": song_id},  # ⚠️ usa data, no json
            headers=self._headers(),
            catch_response=True,
            name="[Likes] Crear + Eliminar"
        ) as r:
            r.success() if r.status_code in (200, 204) else r.failure(f"Error {r.status_code}")

    @task(3)
    def crear_favorito(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS)
        }
        with self.client.post(
            "/api/favorites",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Favorites] Crear"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(2)
    def eliminar_favorito(self):
        payload = {
            "song_id": random.choice(SAMPLE_SONG_IDS)
        }
        with self.client.delete(
            "/api/favorites",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Favorites] Eliminar"
        ) as r:
            r.success() if r.status_code in (200, 204) else r.failure(f"Error {r.status_code}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )