# Laravel / Eloquent Conventions

Follow these so the user can scaffold Eloquent models with zero manual overrides. When in
doubt, match what `php artisan make:model -m` would expect.

## Naming
- **Tables:** plural, snake_case — `users`, `order_items`, `blog_posts`.
- **Primary key:** `id`, auto-incrementing big integer — `$table->id();`.
- **Foreign keys:** `<singular_related>_id` — `user_id`, `product_id`.
- **Columns:** snake_case.
- **Pivot (many-to-many) tables:** singular models, alphabetical, snake_case — `role_user`
  (not `user_role`), with `->foreignId()` for each side.
- **Timestamps:** add `$table->timestamps();` (`created_at`, `updated_at`) to every entity
  table. Add `$table->softDeletes();` only where soft deletion is wanted.

## Types (map dirty legacy types → correct ones)
- Money/amounts → `$table->decimal('amount', 12, 2);` (never float).
- Booleans → `$table->boolean('is_active');` (canonicalize `Y/N`, `0/1`, `'true'`).
- Dates/times → `date`, `dateTime`, or `timestamp` — never store as `VARCHAR`.
- Categoricals → a **lookup table** with an FK (preferred, extensible) or `$table->enum()`
  for small fixed sets. Prefer lookup tables for anything the business may extend.
- Text → `string` (set a real length) for short, `text`/`longText` for large; stop the
  `VARCHAR(255)`-everything habit.
- JSON that is genuinely document-shaped → `$table->json('meta');`. CSV-in-a-cell → break
  into rows/related table instead.

## Relationships & integrity
- Every relationship gets an enforced FK:
  `$table->foreignId('user_id')->constrained()->cascadeOnDelete();`
  (or `->nullOnDelete()` / `->restrictOnDelete()` per business rule).
- Add indexes for FK columns (Laravel adds them for `constrained()`), and composite/unique
  indexes where the audit showed uniqueness should be enforced:
  `$table->unique(['email']);`

## Migration file shape
```php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->foreignId('customer_id')->constrained()->cascadeOnDelete();
            $table->decimal('total', 12, 2);
            $table->string('status');           // or FK to statuses lookup
            $table->timestamps();
        });
    }
    public function down(): void {
        Schema::dropIfExists('orders');
    }
};
```

## 12-factor alignment (why this matters)
The point of the clean schema is a backend that obeys 12-factor: config (DB creds) comes
from the environment (`.env`/`config/database.php`), the schema is versioned in migrations
(treat schema as code, reproducible across dev/stage/prod), and data integrity is enforced
in the DB rather than hoped for in application code. Keep migrations ordered and idempotent
so any environment can be built from scratch.
