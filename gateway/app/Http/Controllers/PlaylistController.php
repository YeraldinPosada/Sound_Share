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

    // playlists del usuario autenticado
    public function index(){
        $user = Auth::user();

        $response = Http::withHeaders($this->headers())
            ->post(env("PLAYLIST_SERVICE")."/user", [
                "user_id" => $user->id
            ]);

        return response()->json($response->json(), $response->status());
    }

    //Crear playlist (con o sin canciones)
    public function store(Request $request){
        $user = Auth::user();

        $response = Http::withHeaders($this->headers())
            ->post(env("PLAYLIST_SERVICE"), [
                "name"=> $request->name,
                "user_id" => $user->id,
                "songs" => $request->songs ?? [] // opcional
            ]);

        return response()->json($response->json(), $response->status());
    }

    //Actualizar nombre o canciones
    public function update(Request $request, $id){
        $response = Http::withHeaders($this->headers())
            ->put(env("PLAYLIST_SERVICE")."/".$id, [
                "name" => $request->name,
                "songs" => $request->songs // opcional
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function destroy($id){
        $response = Http::withHeaders($this->headers())
            ->delete(env("PLAYLIST_SERVICE")."/".$id);

        return response()->json(null, $response->status());
    }

    //Agregar canción a playlist
    public function addSong(Request $request, $playlist_id){
        $response = Http::withHeaders($this->headers())
            ->post(env("PLAYLIST_SERVICE")."/".$playlist_id."/songs", [
                "song_id" => $request->song_id
            ]);

        return response()->json($response->json(), $response->status());
    }

    // Quitar canción de playlist
    public function removeSong($playlist_id, $song_id){
        $response = Http::withHeaders($this->headers())
            ->delete(env("PLAYLIST_SERVICE")."/".$playlist_id."/songs/".$song_id);

        return response()->json($response->json(), $response->status());
    }

    // Playlist completa (con info de canciones)
    public function showFull($id){

        // 1. Obtener playlist
        $playlist = Http::withHeaders($this->headers())
            ->get(env("PLAYLIST_SERVICE")."/".$id);

        if($playlist->failed()){
            return response()->json([
                "error" => "Playlist no encontrada"
            ], 404);
        }

        $playlistData = $playlist->json();

        $songsFull = [];

        // 2. Traer info completa de cada canción
        if(isset($playlistData["songs"])){
            foreach($playlistData["songs"] as $song_id){

                $song = Http::withHeaders($this->headers())
                    ->get(env("SONG_SERVICE")."/".$song_id);

                if(!$song->failed()){
                    $songsFull[] = $song->json();
                }
            }
        }

        // 3. Reemplazar IDs por objetos
        $playlistData["songs"] = $songsFull;

        return response()->json($playlistData);
    }
}