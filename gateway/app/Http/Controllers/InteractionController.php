<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class InteractionController extends Controller
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

    // LIKES
    public function createLike(Request $request)
    {
        $error = $this->validateSong($request->song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->post(env("INTERACTIONS_SERVICE") . "/likes", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), (int) $response->status());
    }

    public function getLikesBySong($song_id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("INTERACTIONS_SERVICE") . "/likes/" . $song_id);

        return response()->json($response->json(), (int) $response->status());
    }

    public function deleteLike(Request $request)
    {
        $error = $this->validateSong($request->song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("INTERACTIONS_SERVICE") . "/likes", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), (int) $response->status());
    }

    // FAVORITES
    public function createFavorite(Request $request)
    {
        $error = $this->validateSong($request->song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->post(env("INTERACTIONS_SERVICE") . "/favorites", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), (int) $response->status());
    }

    public function getFavoritesByUser($user_id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("INTERACTIONS_SERVICE") . "/favorites/" . $user_id);

        return response()->json($response->json(), (int) $response->status());
    }

    public function deleteFavorite(Request $request)
    {
        $error = $this->validateSong($request->song_id);
        if ($error) return $error;

        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("INTERACTIONS_SERVICE") . "/favorites", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), (int) $response->status());
    }
}