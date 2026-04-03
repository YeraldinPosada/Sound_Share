<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class LyricsController extends Controller
{
    private function getHeaders()
    {
        return [
            'Authorization' => env("TOKEN"),
            'Content-Type' => 'application/json'
        ];
    }

    public function store(Request $request)
    {                   
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
