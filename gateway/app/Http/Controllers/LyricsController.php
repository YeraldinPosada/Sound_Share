<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class LyricsController extends Controller
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

    public function store(Request $request)
    {                   

        $error = $this->validateSong($request->song_id);
        if ($error) return $error;
        
        $response = Http::withHeaders($this->getHeaders())
            ->post(env("LYRICS_SERVICE"), [
                'song_id' => $request->song_id,
                'content' => $request->content
            ]);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    public function index()
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("LYRICS_SERVICE"));

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    public function show($id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("LYRICS_SERVICE") . "/" . $id);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    public function update(Request $request, $id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->put(env("LYRICS_SERVICE") . "/" . $id, [
                'content' => $request->content
            ]);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }

    public function destroy($id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("LYRICS_SERVICE") . "/" . $id);

        return response()->json(
            $response->json(),
            (int) $response->status()
        );
    }
}
