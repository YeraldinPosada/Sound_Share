<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;
use App\Http\Controllers\SongController;



Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

#Rutas para la Autentificación de usuarios
Route::post('/register', [UserController::class, 'register']);
Route::post('/login', [UserController::class, 'login']);
Route::post('/logout', [UserController::class, 'logout'])->middleware('auth:sanctum');
Route::post('/password_reset', [UserController::class, 'password_reset']);


//Endpoints de Songs
Route::get('/songs', [SongController::class, 'show_songs']);
Route::post('/songs', [SongController::class, 'create_song']);
Route::put('/songs/{id}', [SongController::class, 'update_song']);
Route::delete('/songs/{id}', [SongController::class, 'delete_song']);