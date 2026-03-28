<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class downloads_service extends Model
{
    protected $fillable = [
        'song_id',
        'user_id'
    ];
}
