--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-1.pgdg20.04+1)

-- Started on 2021-01-19 17:55:50 +03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2990 (class 1262 OID 26985)
-- Name: yandex_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE yandex_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C.UTF-8' LC_CTYPE = 'C.UTF-8';


ALTER DATABASE yandex_db OWNER TO postgres;

\connect yandex_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 27015)
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 27023)
-- Name: movie_actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_actors (
    movie_id text NOT NULL,
    actor_id integer
);


ALTER TABLE public.movie_actors OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 27029)
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id text NOT NULL,
    genre text,
    director text,
    writer text,
    title text,
    plot text,
    ratings text,
    imdb_rating text,
    writers text
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 27037)
-- Name: rating_agency; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating_agency (
    id text,
    name text
);


ALTER TABLE public.rating_agency OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 27043)
-- Name: writers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.writers (
    id text NOT NULL,
    name text
);


ALTER TABLE public.writers OWNER TO postgres;

--
-- TOC entry 2854 (class 2606 OID 27022)
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- TOC entry 2856 (class 2606 OID 27036)
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2858 (class 2606 OID 27050)
-- Name: writers writers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.writers
    ADD CONSTRAINT writers_pkey PRIMARY KEY (id);


-- Completed on 2021-01-19 17:55:50 +03

--
-- PostgreSQL database dump complete
--

