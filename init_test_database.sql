CREATE DATABASE bit_schema_test;
\c bit_schema_test;
CREATE SCHEMA IF NOT EXISTS bitschema;
CREATE SCHEMA IF NOT EXISTS test_schema;
CREATE SCHEMA IF NOT EXISTS test_schema_2;
ALTER DATABASE bit_schema_test SET search_path TO bitschema,public;