<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Tests\TestCase;

class UserTest extends TestCase
{
    use RefreshDatabase;

    // ---------------------------------------------------------------
    // TEST 1 — Registro exitoso
    // ---------------------------------------------------------------

    public function test_usuario_puede_registrarse_con_todos_los_campos(): void
    {
        $response = $this->postJson('/api/register', [
            'name'        => 'Yeraldin Posada',
            'email'       => 'yeraldin@gmail.com',
            'password'    => 'Secret123!',
            'question'    => '¿Nombre de tu mascota?',
            'resquestion' => 'Firulais',
        ]);

        $response->assertStatus(200)
                 ->assertJson(["mensaje" => "Usuario creado"]);

        $this->assertDatabaseHas('users', [
            'email' => 'yeraldin@gmail.com',
            'name'  => 'Yeraldin Posada',
        ]);
    }

    // ---------------------------------------------------------------
    // TEST 2 — Login exitoso retorna token
    // ---------------------------------------------------------------

    public function test_usuario_puede_iniciar_sesion_y_recibe_token(): void
    {
        // Crear usuario directamente en BD con password hasheado
        User::factory()->create([
            'email'       => 'yeraldin@gmail.com',
            'password'    => Hash::make('Secret123!'),
            'question'    => '¿Nombre de tu mascota?',
            'resquestion' => 'Firulais',
        ]);

        $response = $this->postJson('/api/login', [
            'email'    => 'yeraldin@gmail.com',
            'password' => 'Secret123!',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure([
                     'access_token',
                     'token_type',
                 ]);

        $this->assertNotEmpty($response->json('access_token'));
        $this->assertEquals('Bearer', $response->json('token_type'));
    }

    // ---------------------------------------------------------------
    // TEST 3 — Login falla con credenciales incorrectas
    // ---------------------------------------------------------------

    public function test_login_falla_con_password_incorrecta(): void
    {
        User::factory()->create([
            'email'    => 'yeraldin@gmail.com',
            'password' => Hash::make('Secret123!'),
        ]);

        $response = $this->postJson('/api/login', [
            'email'    => 'yeraldin@gmail.com',
            'password' => 'password_incorrecto',
        ]);

        // El controlador retorna 200 con mensaje de acceso denegado
        $response->assertStatus(200)
                 ->assertJsonFragment(['Acceso denegado' => 'Credenciales invalidas']);
    }
    // ---------------------------------------------------------------
    // TEST 4 — Logout invalida el token
    // ---------------------------------------------------------------

    public function test_usuario_autenticado_puede_cerrar_sesion(): void
    {
        User::factory()->create([
            'email'    => 'yeraldin@gmail.com',
            'password' => Hash::make('Secret123!'),
        ]);

        // Primero hacemos login para obtener el token
        $token = $this->postJson('/api/login', [
            'email'    => 'yeraldin@gmail.com',
            'password' => 'Secret123!',
        ])->json('access_token');

        // Luego hacemos logout con ese token
        $response = $this->withHeader('Authorization', "Bearer {$token}")
                        ->postJson('/api/logout');

        $response->assertStatus(200)
                ->assertJson(['Message' => 'Logged out']);

        // Verificar que el token fue eliminado de la BD
        $this->assertDatabaseCount('personal_access_tokens', 0);
    }

    // ---------------------------------------------------------------
    // TEST 5 — Recuperación de contraseña
    // ---------------------------------------------------------------

    public function test_password_reset_exitoso_con_respuesta_correcta(): void
    {
        User::factory()->create([
            'email'       => 'yeraldin@gmail.com',
            'password'    => Hash::make('Secret123!'),
            'question'    => '¿Nombre de tu mascota?',
            'resquestion' => 'Firulais',
        ]);

        $response = $this->postJson('/api/password_reset', [
            'email'       => 'yeraldin@gmail.com',
            'resquestion' => 'Firulais',
            'password'    => 'NuevoPassword123!',
        ]);

        $response->assertStatus(200)
                ->assertJson(['message' => 'Contraseña actualizada']);

        // Verificar que la nueva contraseña funciona para login
        $loginResponse = $this->postJson('/api/login', [
            'email'    => 'yeraldin@gmail.com',
            'password' => 'NuevoPassword123!',
        ]);

        $loginResponse->assertStatus(200)
                    ->assertJsonStructure(['access_token']);
    }

    public function test_password_reset_falla_con_respuesta_incorrecta(): void
    {
        User::factory()->create([
            'email'       => 'yeraldin@gmail.com',
            'password'    => Hash::make('Secret123!'),
            'question'    => '¿Nombre de tu mascota?',
            'resquestion' => 'Firulais',
        ]);

        $response = $this->postJson('/api/password_reset', [
            'email'       => 'yeraldin@gmail.com',
            'resquestion' => 'RespuestaIncorrecta',
            'password'    => 'NuevoPassword123!',
        ]);

        $response->assertStatus(200)
                ->assertJson(['message' => 'Respuesta incorrecta']);

        // La contraseña original no debe haber cambiado
        $loginResponse = $this->postJson('/api/login', [
            'email'    => 'yeraldin@gmail.com',
            'password' => 'Secret123!',
        ]);

        $loginResponse->assertStatus(200)
                    ->assertJsonStructure(['access_token']);
    }
}