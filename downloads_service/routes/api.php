<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');


Route::middleware('auth.token')->group(function () {
    Route::post('/downloads', [DownloadController::class, 'store']);
    Route::get('/downloads', [DownloadController::class, 'index']);
    Route::get('/downloads/user/{user_id}', [DownloadController::class, 'getByUser']);
    Route::get('/downloads/song/{song_id}', [DownloadController::class, 'getBySong']);
});