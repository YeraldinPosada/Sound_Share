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

    // LIKES

    // Crear like
    public function createLike(Request $request)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->post(env("INTERACTIONS_URL") . "/likes", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Obtener likes por canción
    public function getLikesBySong($song_id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("INTERACTIONS_URL") . "/likes/" . $song_id);

        return response()->json($response->json(), $response->status());
    }

    // Eliminar like
    public function deleteLike(Request $request)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("INTERACTIONS_URL") . "/likes", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), $response->status());
    }

    //FAVORITES

    // Crear favorito
    public function createFavorite(Request $request)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->post(env("INTERACTIONS_URL") . "/favorites", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Obtener favoritos por usuario
    public function getFavoritesByUser($user_id)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->get(env("INTERACTIONS_URL") . "/favorites/" . $user_id);

        return response()->json($response->json(), $response->status());
    }

    // Eliminar favorito
    public function deleteFavorite(Request $request)
    {
        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("INTERACTIONS_URL") . "/favorites", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), $response->status());
    }
}