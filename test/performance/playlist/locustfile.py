from locust import HttpUser, task, between
import random
import gevent  

TEST_EMAIL    = "Susyy@gmaill.com"
TEST_PASSWORD = "1234"

SAMPLE_SONG_IDS     = [1, 5, 4]
SAMPLE_PLAYLIST_IDS = ["XYpJAg8hwhyM4cZRsW9Y", "zkMjtSSegPg1squYIxEZ", "0MII0tfzROA6n3Xegvac"]

# Semáforo global: máx 10 logins simultáneos al arrancar
_login_semaphore = gevent.lock.Semaphore(10)


class PlaylistUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self._login()

    def _login(self):
        # CAMBIO 1: semáforo para no inundar /api/login con 100 requests a la vez
        with _login_semaphore:
            for intento in range(5):  # más reintentos
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
                    else:
                        print(f"[Login] Intento {intento+1} falló: {r.status_code}")
                except Exception as e:
                    print(f"[Login] Excepción intento {intento+1}: {e}")

                gevent.sleep(2 ** intento)

    def _headers(self):
        if not self.token:
            self._login()
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def _create_playlist(self, name_prefix="Playlist"):
        """Helper centralizado para crear playlists y retornar el ID."""
        r = self.client.post(
            "/api/playlists",
            json={"name": f"{name_prefix} {random.randint(1000, 9999)}", "description": ""},
            headers=self._headers(),
            name="[Playlist] Crear"
        )
        if r.status_code not in (200, 201):
            return None
        data = r.json()
        return data.get("id") or data.get("data", {}).get("id")


    @task(5)
    def listar_playlists(self):
        headers = self._headers()
        if not headers:
            return
        with self.client.get(
            "/api/playlists",
            headers=headers,
            catch_response=True,
            name="[Playlist] Listar"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")

    @task(4)
    def obtener_playlist(self):
        headers = self._headers()
        if not headers:
            return
        playlist_id = random.choice(SAMPLE_PLAYLIST_IDS)
        with self.client.get(
            f"/api/playlists/{playlist_id}",
            headers=headers,
            catch_response=True,
            name="[Playlist] Obtener"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(2)
    def crear_playlist(self):
        headers = self._headers()
        if not headers:
            return
        with self.client.post(
            "/api/playlists",
            json={"name": f"Playlist de prueba {random.randint(1000, 9999)}", "description": "Locust"},
            headers=headers,
            catch_response=True,
            name="[Playlist] Crear"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code} - {r.text[:80]}")

    @task(2)
    def editar_playlist(self):
        headers = self._headers()
        if not headers:
            return
        playlist_id = self._create_playlist("Playlist para editar")
        if not playlist_id:
            return

        gevent.sleep(0.3)  

        with self.client.put(
            f"/api/playlists/{playlist_id}",
            json={"name": f"Playlist actualizada {random.randint(100, 999)}"},
            headers=headers,
            catch_response=True,
            name="[Playlist] Editar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(1)
    def eliminar_playlist(self):
        headers = self._headers()
        if not headers:
            return
        playlist_id = self._create_playlist("Playlist temporal")
        if not playlist_id:
            return
        self.client.delete(
            f"/api/playlists/{playlist_id}",
            headers=headers,
            name="[Playlist] Eliminar"
        )


    @task(3)
    def agregar_cancion(self):
        headers = self._headers()
        if not headers:
            return
        playlist_id = self._create_playlist("Playlist canciones")
        if not playlist_id:
            return

        gevent.sleep(0.3)

        with self.client.put(
            f"/api/playlists/{playlist_id}/songs",
            json={"song_id": random.choice(SAMPLE_SONG_IDS)},
            headers=headers,
            catch_response=True,
            name="[Playlist] Agregar canción"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(1)
    def eliminar_cancion(self):
        headers = self._headers()
        if not headers:
            return
        playlist_id = self._create_playlist("Playlist quitar canción")
        if not playlist_id:
            return

        r2 = self.client.put(
            f"/api/playlists/{playlist_id}/songs",
            json={"song_id": random.choice(SAMPLE_SONG_IDS)},
            headers=headers,
            name="[Playlist] Agregar canción para quitar"
        )
        if r2.status_code not in (200, 201):
            return

        gevent.sleep(0.3)

        with self.client.delete(
            f"/api/playlists/{playlist_id}/songs/0",
            headers=headers,
            catch_response=True,
            name="[Playlist] Quitar canción"
        ) as r:
            r.success() if r.status_code in (200, 204) else r.failure(f"Error {r.status_code}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )