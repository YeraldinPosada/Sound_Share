<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Auth;

class PlaylistController extends Controller
{
    private function headers(){
        return [
            'Authorization' => env("TOKEN")
        ];
    }

    // Trae TODAS las playlists
    public function index(){
        $response = Http::withHeaders($this->headers())
            ->get(env("PLAYLIST_SERVICE"));

        return response()->json($response->json(), $response->status());
    }

    // Crear playlist
    public function store(Request $request){
        $user = Auth::user();

        $response = Http::withHeaders($this->headers())
            ->post(env("PLAYLIST_SERVICE"), [
                "name"    => $request->name,
                "user_id" => $user->id,
                "songs"   => $request->songs ?? []
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Actualizar playlist
    public function update(Request $request, $id){
        $user = Auth::user();

        $response = Http::withHeaders($this->headers())
            ->put(env("PLAYLIST_SERVICE")."/".$id, [
                "name"    => $request->name,
                "user_id" => $user->id,
                "songs"   => $request->songs ?? []
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Eliminar playlist
    public function destroy($id){
        $response = Http::withHeaders($this->headers())
            ->delete(env("PLAYLIST_SERVICE")."/".$id);

        return response()->json(null, $response->status());
    }

    // Agregar canción — ahora con title y artist (PUT como Flask)
    public function addSong(Request $request, $playlist_id){
        $response = Http::withHeaders($this->headers())
            ->put(env("PLAYLIST_SERVICE")."/".$playlist_id."/songs", [
                "title"  => $request->title,
                "artist" => $request->artist
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Quitar canción por índice (como Flask)
    public function removeSong($playlist_id, $index){
        $response = Http::withHeaders($this->headers())
            ->delete(env("PLAYLIST_SERVICE")."/".$playlist_id."/songs/".$index);

        return response()->json($response->json(), $response->status());
    }

    // Playlist por ID
    public function show($id){
        $response = Http::withHeaders($this->headers())
            ->get(env("PLAYLIST_SERVICE")."/".$id);

        if($response->failed()){
            return response()->json(["error" => "Playlist no encontrada"], 404);
        }

        return response()->json($response->json());
    }
}