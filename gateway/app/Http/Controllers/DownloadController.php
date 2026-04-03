<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class DownloadController extends Controller
{
    private function getHeaders()
    {
        return [
            'Authorization' => env("TOKEN"),
            'Content-Type' => 'application/json'
        ];
    }

    private function validateSong($song_id){
        if (!$song_id) {
            return response()->json([
                "error" => "song_id es requerido"
            ], 400);
        }

        $response = Http::withHeaders($this->getHeaders())
            ->get(env("SONG_SERVICE") . "/" . $song_id);

        if ($response->failed()) {
            return response()->json([
                "error" => "La canción no existe"
            ], 404);
        }

        return null;
    }

    // Crear descarga
    public function store(Request $request)
    {                  
        $error = $this->validateSong($request->song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->post(env("DOWNLOAD_SERVICE"), [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
        }

    // Obtener todas las descargas
    public function index()
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("DOWNLOAD_SERVICE"));

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    // Obtener descargas por usuario
    public function getByUser($user_id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("DOWNLOAD_SERVICE") . "/user/" . $user_id);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    // Obtener descargas por canción
    public function getBySong($song_id)
    {   
        $error = $this->validateSong($song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->get(env("DOWNLOAD_SERVICE") . "/song/" . $song_id);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }
}
