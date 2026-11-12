<?php
// Faz 13 - PHPStan teshisi. Hicbir seyi degistirmez, yalnizca okur.
echo "PHP: ", PHP_VERSION, " (", PHP_OS_FAMILY, ")\n";
echo "ini: ", php_ini_loaded_file(), "\n";
foreach (['opcache.enable', 'opcache.enable_cli', 'opcache.save_comments', 'memory_limit'] as $k) {
    echo str_pad($k, 24), var_export(ini_get($k), true), "\n";
}
echo "eklentiler: ", implode(', ', get_loaded_extensions()), "\n\n";

$src = "<?php\n/** @return array<int> */\nfunction f() {}\n";
$types = array_map(fn ($t) => $t->getTokenName(), PhpToken::tokenize($src));
echo "1) Tokenizer docblock'u goruyor mu? ", in_array('T_DOC_COMMENT', $types, true) ? "EVET" : "HAYIR  <-- SORUN", "\n";

/** @return int */
function teshis_fonksiyonu() { return 1; }
$doc = (new ReflectionFunction('teshis_fonksiyonu'))->getDocComment();
echo "2) Reflection docblock'u goruyor mu? ", $doc !== false ? "EVET" : "HAYIR  <-- SORUN", "\n";

require __DIR__ . '/../davetkart-backend-php-laravel/vendor/autoload.php';
$doc = (new ReflectionClass(\Illuminate\Database\Schema\ColumnDefinition::class))->getDocComment();
echo "3) Vendor sinifinin docblock'u: ", ($doc !== false && str_contains($doc, '@method')) ? "EVET" : "HAYIR  <-- SORUN", "\n";

$parser = (new \PhpParser\ParserFactory())->createForHostVersion();
$ast = $parser->parse($src);
echo "4) PHP-Parser docblock'u goruyor mu? ", $ast[0]->getDocComment() !== null ? "EVET" : "HAYIR  <-- SORUN", "\n";
