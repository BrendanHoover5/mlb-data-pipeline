--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Homebrew)
-- Dumped by pg_dump version 14.15 (Homebrew)

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
-- Name: game_boxscore_raw; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.game_boxscore_raw (
    game_id bigint NOT NULL,
    boxscore_json jsonb,
    collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.game_boxscore_raw OWNER TO brendanhoover;

--
-- Name: games; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.games (
    game_id bigint NOT NULL,
    game_date date,
    home_team text,
    away_team text,
    home_score integer,
    away_score integer,
    winner text,
    status text,
    game_datetime timestamp without time zone,
    season integer,
    home_team_id integer,
    away_team_id integer,
    home_probable_pitcher text,
    away_probable_pitcher text,
    venue_id integer,
    venue_name text,
    doubleheader text,
    game_num integer,
    home_pitcher_id integer,
    away_pitcher_id integer
);


ALTER TABLE public.games OWNER TO brendanhoover;

--
-- Name: model_training_rows; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.model_training_rows (
    game_id bigint NOT NULL,
    game_date date NOT NULL,
    home_team_id integer NOT NULL,
    away_team_id integer NOT NULL,
    home_win integer NOT NULL,
    home_team_games_played_before integer,
    away_team_games_played_before integer,
    home_team_win_pct_before double precision,
    away_team_win_pct_before double precision,
    home_team_last_10_wins integer,
    away_team_last_10_wins integer,
    home_team_runs_per_game_before double precision,
    away_team_runs_per_game_before double precision,
    home_team_runs_allowed_per_game_before double precision,
    away_team_runs_allowed_per_game_before double precision,
    home_team_home_win_pct_before double precision,
    away_team_away_win_pct_before double precision
);


ALTER TABLE public.model_training_rows OWNER TO brendanhoover;

--
-- Name: pitchers; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.pitchers (
    pitcher_id integer NOT NULL,
    pitcher_name text
);


ALTER TABLE public.pitchers OWNER TO brendanhoover;

--
-- Name: pitchers_pitcher_id_seq; Type: SEQUENCE; Schema: public; Owner: brendanhoover
--

CREATE SEQUENCE public.pitchers_pitcher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pitchers_pitcher_id_seq OWNER TO brendanhoover;

--
-- Name: pitchers_pitcher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: brendanhoover
--

ALTER SEQUENCE public.pitchers_pitcher_id_seq OWNED BY public.pitchers.pitcher_id;


--
-- Name: player_batting_game_stats; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.player_batting_game_stats (
    game_id bigint NOT NULL,
    player_id integer NOT NULL,
    mlb_player_id integer NOT NULL,
    team_id integer NOT NULL,
    opponent_team_id integer NOT NULL,
    is_home boolean NOT NULL,
    batting_order integer,
    "position" text,
    at_bats integer,
    runs integer,
    hits integer,
    rbi integer,
    walks integer,
    strikeouts integer,
    home_runs integer,
    doubles integer,
    triples integer,
    stolen_bases integer,
    left_on_base integer,
    avg_after_game text,
    obp_after_game text,
    slg_after_game text,
    ops_after_game text
);


ALTER TABLE public.player_batting_game_stats OWNER TO brendanhoover;

--
-- Name: player_pitching_game_stats; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.player_pitching_game_stats (
    game_id bigint NOT NULL,
    player_id integer NOT NULL,
    mlb_player_id integer NOT NULL,
    team_id integer NOT NULL,
    opponent_team_id integer NOT NULL,
    is_home boolean NOT NULL,
    innings_pitched text,
    hits_allowed integer,
    runs_allowed integer,
    earned_runs integer,
    walks integer,
    strikeouts integer,
    home_runs_allowed integer,
    pitches_thrown integer,
    strikes integer,
    era_after_game text
);


ALTER TABLE public.player_pitching_game_stats OWNER TO brendanhoover;

--
-- Name: players; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.players (
    player_id integer NOT NULL,
    mlb_player_id integer NOT NULL,
    full_name text,
    boxscore_name text
);


ALTER TABLE public.players OWNER TO brendanhoover;

--
-- Name: players_player_id_seq; Type: SEQUENCE; Schema: public; Owner: brendanhoover
--

CREATE SEQUENCE public.players_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.players_player_id_seq OWNER TO brendanhoover;

--
-- Name: players_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: brendanhoover
--

ALTER SEQUENCE public.players_player_id_seq OWNED BY public.players.player_id;


--
-- Name: team_game_stats; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.team_game_stats (
    game_id bigint NOT NULL,
    team_id integer NOT NULL,
    opponent_team_id integer NOT NULL,
    is_home boolean NOT NULL,
    runs integer,
    hits integer,
    at_bats integer,
    walks integer,
    strikeouts integer,
    home_runs integer,
    doubles integer,
    triples integer,
    rbi integer,
    left_on_base integer,
    pitching_innings text,
    pitching_hits_allowed integer,
    pitching_runs_allowed integer,
    pitching_earned_runs integer,
    pitching_walks integer,
    pitching_strikeouts integer,
    pitching_home_runs_allowed integer,
    pitches_thrown integer,
    strikes integer
);


ALTER TABLE public.team_game_stats OWNER TO brendanhoover;

--
-- Name: teams; Type: TABLE; Schema: public; Owner: brendanhoover
--

CREATE TABLE public.teams (
    team_id integer NOT NULL,
    team_name text,
    team_abbr text,
    mlb_team_id integer
);


ALTER TABLE public.teams OWNER TO brendanhoover;

--
-- Name: teams_team_id_seq; Type: SEQUENCE; Schema: public; Owner: brendanhoover
--

CREATE SEQUENCE public.teams_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teams_team_id_seq OWNER TO brendanhoover;

--
-- Name: teams_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: brendanhoover
--

ALTER SEQUENCE public.teams_team_id_seq OWNED BY public.teams.team_id;


--
-- Name: pitchers pitcher_id; Type: DEFAULT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.pitchers ALTER COLUMN pitcher_id SET DEFAULT nextval('public.pitchers_pitcher_id_seq'::regclass);


--
-- Name: players player_id; Type: DEFAULT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.players ALTER COLUMN player_id SET DEFAULT nextval('public.players_player_id_seq'::regclass);


--
-- Name: teams team_id; Type: DEFAULT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.teams ALTER COLUMN team_id SET DEFAULT nextval('public.teams_team_id_seq'::regclass);


--
-- Name: game_boxscore_raw game_boxscore_raw_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.game_boxscore_raw
    ADD CONSTRAINT game_boxscore_raw_pkey PRIMARY KEY (game_id);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_id);


--
-- Name: model_training_rows model_training_rows_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.model_training_rows
    ADD CONSTRAINT model_training_rows_pkey PRIMARY KEY (game_id);


--
-- Name: pitchers pitchers_pitcher_name_key; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.pitchers
    ADD CONSTRAINT pitchers_pitcher_name_key UNIQUE (pitcher_name);


--
-- Name: pitchers pitchers_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.pitchers
    ADD CONSTRAINT pitchers_pkey PRIMARY KEY (pitcher_id);


--
-- Name: player_batting_game_stats player_batting_game_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_batting_game_stats
    ADD CONSTRAINT player_batting_game_stats_pkey PRIMARY KEY (game_id, mlb_player_id);


--
-- Name: player_pitching_game_stats player_pitching_game_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_pitching_game_stats
    ADD CONSTRAINT player_pitching_game_stats_pkey PRIMARY KEY (game_id, mlb_player_id);


--
-- Name: players players_mlb_player_id_key; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_mlb_player_id_key UNIQUE (mlb_player_id);


--
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);


--
-- Name: team_game_stats team_game_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.team_game_stats
    ADD CONSTRAINT team_game_stats_pkey PRIMARY KEY (game_id, team_id);


--
-- Name: teams teams_mlb_team_id_key; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_mlb_team_id_key UNIQUE (mlb_team_id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);


--
-- Name: teams teams_team_abbr_key; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_team_abbr_key UNIQUE (team_abbr);


--
-- Name: teams teams_team_name_key; Type: CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_team_name_key UNIQUE (team_name);


--
-- Name: idx_games_game_date; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_games_game_date ON public.games USING btree (game_date);


--
-- Name: idx_player_batting_player_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_player_batting_player_id ON public.player_batting_game_stats USING btree (player_id);


--
-- Name: idx_player_batting_team_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_player_batting_team_id ON public.player_batting_game_stats USING btree (team_id);


--
-- Name: idx_player_pitching_player_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_player_pitching_player_id ON public.player_pitching_game_stats USING btree (player_id);


--
-- Name: idx_player_pitching_team_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_player_pitching_team_id ON public.player_pitching_game_stats USING btree (team_id);


--
-- Name: idx_team_game_stats_game_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_team_game_stats_game_id ON public.team_game_stats USING btree (game_id);


--
-- Name: idx_team_game_stats_team_id; Type: INDEX; Schema: public; Owner: brendanhoover
--

CREATE INDEX idx_team_game_stats_team_id ON public.team_game_stats USING btree (team_id);


--
-- Name: player_batting_game_stats fk_player_batting_player; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_batting_game_stats
    ADD CONSTRAINT fk_player_batting_player FOREIGN KEY (player_id) REFERENCES public.players(player_id);


--
-- Name: player_pitching_game_stats fk_player_pitching_player; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_pitching_game_stats
    ADD CONSTRAINT fk_player_pitching_player FOREIGN KEY (player_id) REFERENCES public.players(player_id);


--
-- Name: team_game_stats fk_team_game_stats_opponent_team; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.team_game_stats
    ADD CONSTRAINT fk_team_game_stats_opponent_team FOREIGN KEY (opponent_team_id) REFERENCES public.teams(mlb_team_id);


--
-- Name: team_game_stats fk_team_game_stats_team; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.team_game_stats
    ADD CONSTRAINT fk_team_game_stats_team FOREIGN KEY (team_id) REFERENCES public.teams(mlb_team_id);


--
-- Name: game_boxscore_raw game_boxscore_raw_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.game_boxscore_raw
    ADD CONSTRAINT game_boxscore_raw_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: model_training_rows model_training_rows_away_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.model_training_rows
    ADD CONSTRAINT model_training_rows_away_team_id_fkey FOREIGN KEY (away_team_id) REFERENCES public.teams(mlb_team_id);


--
-- Name: model_training_rows model_training_rows_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.model_training_rows
    ADD CONSTRAINT model_training_rows_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: model_training_rows model_training_rows_home_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.model_training_rows
    ADD CONSTRAINT model_training_rows_home_team_id_fkey FOREIGN KEY (home_team_id) REFERENCES public.teams(mlb_team_id);


--
-- Name: player_batting_game_stats player_batting_game_stats_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_batting_game_stats
    ADD CONSTRAINT player_batting_game_stats_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: player_pitching_game_stats player_pitching_game_stats_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.player_pitching_game_stats
    ADD CONSTRAINT player_pitching_game_stats_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- Name: team_game_stats team_game_stats_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brendanhoover
--

ALTER TABLE ONLY public.team_game_stats
    ADD CONSTRAINT team_game_stats_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- PostgreSQL database dump complete
--

