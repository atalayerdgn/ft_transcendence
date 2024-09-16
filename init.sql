-- Veritabanı oluşturma (Zaten varsa hata vermez)
CREATE DATABASE usermanagement_db;
CREATE DATABASE game_db;

-- Kullanıcı oluşturma (Zaten varsa hata vermez)
CREATE USER postgres WITH PASSWORD '1234';

-- Kullanıcıya gerekli izinleri verme
GRANT ALL PRIVILEGES ON DATABASE usermanagement_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE game_db TO postgres;


-- PostgreSQL'de dil desteği ekleme (opsiyonel, bazı durumlarda gerekebilir)
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
