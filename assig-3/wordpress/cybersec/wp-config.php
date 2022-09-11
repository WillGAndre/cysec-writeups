<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'cyb1' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', '' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '}tC/Ln4QO*eg5RBmeim*wuL~fS=TxoD*joLwYBaJsUXZ5qYn=YSm5.F8QyG7+0$o' );
define( 'SECURE_AUTH_KEY',  'BlQXkIQEkZq;6=bI9kkkAR_o{[Bc9n~HOHfTlktf3qKp`Ps0L=v>PIRQG W#$1(=' );
define( 'LOGGED_IN_KEY',    '(+-O}nm`MzjjLE7#5V6m*|4Y|:Y]43wFnAEUt.Z0bg?!Uz)y*3S}R1{ZNv|jbCCo' );
define( 'NONCE_KEY',        'zc;^<;Ou*`Hre6S9AE@1mBfk}N7!0d|sLY/E@IpjBgCNn}dB1:HXInHEr,o^ds@v' );
define( 'AUTH_SALT',        'YB9AlE|*VWpo}Bxy?{+e#H0}B d1>1=|K6NH:hq351nImu#s*2?DnsK4c_lmY_a/' );
define( 'SECURE_AUTH_SALT', 'h-4;d`l.F`7uJ. y`.}D<yrUgS!:Lmd9gS*U2_&!UElF}Xz[!$xICS_.vKVn!uDx' );
define( 'LOGGED_IN_SALT',   'R]z>>ZT:#pd,h<7uGXaxo6K<48tk!_e<%r!8W&:khY]21!9y@SP#~YpTPYG4>S.j' );
define( 'NONCE_SALT',       '%usRVYqOi%,0cL2a!E*0!Gx;A%OLz65AuFMoZsz+|09@LqpczCVnRoS/#pmb]%Um' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
