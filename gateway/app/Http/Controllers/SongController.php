<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Auth;

class SongController extends Controller
{
        public function show_songs(){
        $response = Http::withHeaders([
        'Authorization' => env("TOKEN"),
        ])->get(env("SONG_SERVICE"));
        return [
        'status' => $response->status(),
        'body' => $response->body(),
        ];
    }

    public function create_song(Request $request){
        $response = Http:: withHeaders([
        'Authorization' => env("TOKEN"),
        ])->post(env("SONG_SERVICE"),[
            "name"=> $request->name,
            "price" => $request->price,
            "color"=> $request->color,
            "stock"=> $request->stock
        ]);
        return [
        'status' => $response->status(),
        'body' => $response->body(),
        ];
        
    }

    public function update_song(Request $request, $id){
    $response = Http::withHeaders([
        'Authorization' => env("TOKEN"),
    ])->put(env("SONG_SERVICE")."/".$id, [
        "name" => $request->name,
        "price" => $request->price,
        "color" => $request->color,
        "stock" => $request->stock
    ]);

    return [
        'status' => $response->status(),
        'body' => $response->body(),
    ];

    } 
    public function delete_song($id){

    $response = Http::withHeaders([
        'Authorization' => env("TOKEN"),
    ])->delete(env("SONG_SERVICE")."/".$id);

    return [
        'status' => $response->status(),
        'body' => $response->body(),
    ];

}
}
