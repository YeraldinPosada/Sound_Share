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
    public function createLike(Request $request)
    {
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
        $response = Http::withHeaders($this->getHeaders())
            ->delete(env("INTERACTIONS_SERVICE") . "/favorites", [
                'user_id' => $request->user()->id,
                'song_id' => $request->song_id
            ]);

        return response()->json($response->json(), (int) $response->status());
    }
}