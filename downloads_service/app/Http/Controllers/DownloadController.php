<?php

namespace App\Http\Controllers;
use App\Models\Download;
use Illuminate\Http\Request;


class DownloadController extends Controller
{
    public function store(Request $request)
    {
        $download = Download::create([
            'song_id' => $request->song_id,
            'user_id' => $request->user_id
        ]);

        return response()->json($download, 201);
    }

    public function index()
    {
        return response()->json(Download::all());
    }

    public function getByUser($user_id)
    {
        return response()->json(
            Download::where('user_id', $user_id)->get()
        );
    }

    public function getBySong($song_id)
    {
        return response()->json(
            Download::where('song_id', $song_id)->get()
        );
    }
}