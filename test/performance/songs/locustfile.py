from locust import HttpUser, task, between  # type: ignore
import random
import gevent

TEST_EMAIL    = "Susyy@gmaill.com"
TEST_PASSWORD = "1234"

SAMPLE_SONG_IDS = [5, 4, 3]

_login_semaphore = gevent.lock.Semaphore(10)


class SongUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self._login()
        self._created_song_ids = [] 

    def _login(self):
        with _login_semaphore:
            for intento in range(5):
                try:
                    r = self.client.post(
                        "/api/login",
                        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
                        name="[Auth] Login"
                    )
                    if r.status_code == 200:
                        data = r.json()
                        self.token = data.get("token") or data.get("access_token")
                        return
                    print(f"[Login] Intento {intento+1} falló: {r.status_code}")
                except Exception as e:
                    print(f"[Login] Excepción intento {intento+1}: {e}")
                gevent.sleep(2 ** intento)

    def _headers(self):
        if not self.token:
            self._login()
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _extract_id(self, data):
        """Extrae el ID de distintas estructuras de respuesta."""
        return (
            data.get("id") or
            data.get("data", {}).get("id") or
            data.get("song", {}).get("id")
        )


    @task(5)
    def listar_canciones(self):
        with self.client.get(
            "/api/songs",
            catch_response=True,
            name="[Songs] Listar"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")


    @task(3)
    def crear_cancion(self):
        headers = self._headers()
        if not headers:
            return

        payload = {
            "title": f"Canción test {random.randint(1000, 9999)}",
            "artist": "Locust Artist",
            "album": "Load Test Album",
            "duration": random.randint(120, 300)
        }
        with self.client.post(
            "/api/songs",
            json=payload,
            headers=headers,
            catch_response=True,
            name="[Songs] Crear"
        ) as r:
            if r.status_code in (200, 201):
                song_id = self._extract_id(r.json())
                if song_id:
                    self._created_song_ids.append(song_id)
                r.success()
            else:
                r.failure(f"Error {r.status_code} - {r.text[:80]}")


    @task(2)
    def actualizar_cancion(self):
        headers = self._headers()
        if not headers:
            return

        song_id = (
            random.choice(self._created_song_ids)
            if self._created_song_ids
            else random.choice(SAMPLE_SONG_IDS)
        )

        with self.client.put(
            f"/api/songs/{song_id}",
            json={"title": f"Canción actualizada {random.randint(100, 999)}"},
            headers=headers,
            catch_response=True,
            name="[Songs] Actualizar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")


    @task(1)
    def eliminar_cancion(self):
        headers = self._headers()
        if not headers:
            return

        if not self._created_song_ids:
            return

        song_id = self._created_song_ids.pop()

        with self.client.delete(
            f"/api/songs/{song_id}",
            headers=headers,
            catch_response=True,
            name="[Songs] Eliminar"
        ) as r:
            r.success() if r.status_code in (200, 204) else r.failure(f"Error {r.status_code}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )