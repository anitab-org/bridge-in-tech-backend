CREATE DATABASE bit_schema;
\c bit_schema;
CREATE SCHEMA IF NOT EXISTS bitschema;
CREATE SCHEMA IF NOT EXISTS bitschemastest;
ALTER DATABASE bit_schema SET search_path TO bitschema,public;