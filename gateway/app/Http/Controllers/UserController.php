<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        $users = User::all();
        return response()->json($users);
    }

    public function create()
    {
        //
    }

    public function register(Request $request)
    {
        $user = new User();
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->question = $request->question;
        $user->resquestion = $request->resquestion;
        $user->save();

        return response()->json("Usuario creado");
    }

    public function login(Request $request)
    {
        $user = User::where('email', $request->email)->first();

        if(!$user || !password_verify($request->password, $user->password)){
            return response()->json(['Acceso denegado' => 'Credenciales invalidas']);
        }

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'access_token' => $token,
            'token_type' => 'Bearer'
        ]);
    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();
        return response()->json(["Message" => 'Logged out']);
    }

        public function password_reset(Request $request)
    {
        $user = User::where('email', $request->email)->first();

        if(!$user || $user->resquestion != $request->resquestion){
            return response()->json(["message" => "Respuesta incorrecta"]);
        }

        $user->password = $request->password;
        $user->save();

        return response()->json(["message" => "Contraseña actualizada"]);
    }


}